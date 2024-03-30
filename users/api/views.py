from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.cache import patch_vary_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import User
from .serializers import UserSerializer
from ..cache import CustomUserCacheBackend

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# class CustomUserCacheAPIView(APIView):
#     # @method_decorator(cache_page(60 * 15), name="dispatch")
#     def get(self, request):
#         # Generate cache key based on user id
#         cache_key = f'user_{request.user.id}_cache'
#
#         # Attempt to fetch cached data
#         cached_data = cache.get(cache_key)
#
#         if cached_data is not None:
#             return Response(cached_data)
#
#         # If cache miss, fetch data from database
#         user = User.objects.get(pk=request.user.id)
#         serializer_context = {
#             'request': request,
#         }
#         serializer = UserSerializer(user, context=serializer_context)
#         data = serializer.data
#
#         # Set data into cache with a key that varies by user
#         cache.set(cache_key, data)
#
#         # Patch response headers to vary by user
#         patch_vary_headers(response, ['Authorization'])
#
#         return Response(data)


class UserListView(APIView):
    cache_backend = CustomUserCacheBackend()

    def get(self, request):
        cache_key = self.cache_backend.get_cache_key(request)
        cached_data = self.cache_backend.get_cached_data(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        response = Response(serializer.data)
        self.cache_backend.set_cached_data(cache_key, serializer.data, timeout=None)

        patch_vary_headers(response, ['Accept-Language', 'Authorization'])

        return response
