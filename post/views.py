from rest_framework import generics

from .cache import PostModelCache
from .models import Post
from .serializers import PostSerializer


# @method_decorator(cache_page(60 * 15), name="dispatch")
# class PostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        cache_backend = PostModelCache('default', {})

        posts = cache_backend.get_posts()

        if posts is None:
            posts = Post.objects.all()
            cache_backend.set_posts(posts)

        return posts
