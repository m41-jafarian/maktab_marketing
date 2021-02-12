from rest_framework import routers, serializers, viewsets
# from account.models import User
# from account.serializers import UserSerializer
from accounts.models import User
from .models import Product, Category, Comment, ShopProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # user_detail = UserSerializer(source='user', read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

# class PostSerializers2(serializers.Serializer):
#     title = serializers.CharField(max_length=150)
#     first_name = serializers.CharField(max_length=150)
#     last_name = serializers.CharField(max_length=150)
#     username = serializers.CharField(max_length=150)
#
#     def validate(self, attrs):
#         return attrs
#
#     def create(self,validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
#     def update(self,instance,validated_data):
#         instance.update(**validated_data)
#         instance.save()
