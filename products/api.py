from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Comment, ShopProduct
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, ShopProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopProductViewSet(ModelViewSet):
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


def post_list(request):
    if request.method == 'GET':
        posts = Product.objects.all()
        serializer = ProductSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def post_detail(request, pk):
    try:
        post = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ProductSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
