from django.urls import path
from arzon_app.API.views import SearchProductView

urlpatterns = [
    path('search-product/', SearchProductView.as_view(), name='search-product'),
]