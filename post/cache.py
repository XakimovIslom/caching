from django.core.cache import cache
from django.core.cache.backends.base import BaseCache


class PostModelCache(BaseCache):
    def __init__(self, location, params):
        super().__init__(params)

    def get_posts(self):
        return cache.get('cached_posts')

    def set_posts(self, posts):
        cache.set('cached_posts', posts)
