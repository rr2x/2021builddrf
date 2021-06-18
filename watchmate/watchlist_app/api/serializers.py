from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer2(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='stream-detail'
    )

    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
        # only used if we want to inherit from serializers.HyperlinkedModelSerializer
        # no need to create 'url HyperlinkedIdentityField
        # extra_kwargs = {
        #     'url': {'view_name': 'stream-detail'}
        # }


class StreamPlatformSerializer(serializers.ModelSerializer):
    # nested serializer
    # "watchlist" is defined on model

    # each stream platform can have multiple movies (watchlist)
    # just create a specific serializer to return specific fields
    watchlist = WatchListSerializer(many=True, read_only=True)

    # return model function value of __str__()
    # watchlist = serializers.StringRelatedField(many=True)

    # only link primarykey
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # 'watch-detail' is define on urls, this will redirect you to detail
    # watchlist = serializers.HyperlinkedRelatedField(
    #    many=True, read_only=True, view_name='watch-detail')

    class Meta:
        model = StreamPlatform
        fields = '__all__'
