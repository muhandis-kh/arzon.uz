from django.urls import path
from arzon_app.API.views import SearchProductView, UserRegistrationView

urlpatterns = [
    path('search-product/', SearchProductView.as_view(), name='search-product'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]