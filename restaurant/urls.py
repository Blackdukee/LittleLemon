from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views



urlpatterns = [
    path("menu/", views.MenuItemsView.as_view(), name="menu"),
    path("menu/<int:pk>", views.SingleMenuItemView.as_view(), name="single_menu"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
