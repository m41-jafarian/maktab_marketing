from rest_framework import routers, serializers, viewsets
# from account.models import User
# from account.serializers import UserSerializer
from .models import Post,Category,Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','slug','content','create_at','update_at','publish_time','author')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title','slug','parent')

class CommentSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source='author', read_only=True)
    post_detail = PostSerializer(source='post', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializers2(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)

    def validate(self, attrs):
        return attrs

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self,instance,validated_data):
        instance.update(**validated_data)
        instance.save()
