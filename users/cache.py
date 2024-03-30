from django.core.cache import cache


# class CustomUserCacheBackend:
#     def __init__(self):
#         pass
#
#     def get_cache_key(self, request):
#         user_id = request.user.id if request.user.is_authenticated else 'anonymous'
#         headers = request.headers.get('Accept-Language', 'Authorization')
#         return f'user_{user_id}_cache_{headers}'
#
#     def get_cached_data(self, cache_key):
#         return cache.get(cache_key)
#
#     def set_cached_data(self, cache_key, data, timeout):
#         cache.set(cache_key, data, timeout)


class CustomUserCacheBackend:
    def __init__(self):
        pass

    def get_cache_key(self, request):
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        headers = request.headers.get('Accept-Language', '')
        return f'user_{user_id}_cache_{headers}'

    def get_cached_data(self, cache_key):
        return cache.get(cache_key)

    def set_cached_data(self, cache_key, data, timeout):
        cache.set(cache_key, data, timeout)
