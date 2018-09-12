from rest_framework import serializers

from InstaVision.models import InstaVisionModel, UserTokens, ImagesFile, CommentsFile


class InstaVisionSerializer(serializers.Serializer):
    images_file_name = serializers.SerializerMethodField('fetch_images_file_name')
    comments_file_name = serializers.SerializerMethodField('fetch_comments_file_name')
    images_file = serializers.SerializerMethodField('fetch_images_file_id')
    comments_file = serializers.SerializerMethodField('fetch_comments_file_id')
    key = serializers.SerializerMethodField('fetch_user_token')
    page_url = serializers.CharField(max_length=300)
    max_posts = serializers.IntegerField()
    id = serializers.IntegerField()


    def fetch_images_file_name(self,model):
        return model.images_file.images_file_name

    def fetch_comments_file_name(self,model):
        return model.comments_file.comments_file_name

    def fetch_images_file_id(self,model):
        return model.images_file.id

    def fetch_comments_file_id(self,model):
        return model.comments_file.id

    def fetch_user_token(self,model):
        return model.key.id


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return InstaVisionModel.objects.create(**validated_data)

    class Meta:
        model = InstaVisionModel






