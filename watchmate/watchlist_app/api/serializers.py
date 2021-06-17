from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    # custom serializer field
    # this will be included as one of the fields
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'  # returns all fields
        # fields = ['id','name','description'] # only return specific
        # exclude = ['active']  # do not include as returned field

    # get_(<variable name>)
    def get_len_name(self, object):
        length = len(object.name)
        return length

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Name is too short')
        return value

    def validate(self, data):  # object level validation
        if data['name'] == data['description']:
            raise serializers.ValidationError(
                'Name and Description should not be the same')
        return data


# region "old code"

# # validator level
# def name_length(value):
#     if len(value) <= 3:
#         raise serializers.ValidationError('Name should be greater than 3')
#     return value


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     # name = serializers.CharField()
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     # field level validation (def validate_<field name>(self, value))
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError('Name is too short')
#     #     return value

#     def validate(self, data):  # object level validation
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'Name and Description should not be the same')
#         return data

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     # instance = old data, validated_data = new data
#     def update(self, instance, validated_data):

#         instance.name = validated_data.get(
#             'name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get(
#             'active', instance.active)

#         instance.save()

#         return instance

# endregion
