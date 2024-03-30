from django.urls import path

from users.views import user_detail_view, user_redirect_view, user_update_view
from users.api import views

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    # path("", views.CustomUserCacheAPIView.as_view()),
    path("", views.UserListView.as_view()),
]
