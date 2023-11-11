from django.urls import path
from arzon_app.API.views import SearchProductView, UserRegistrationView
from arzon_app.views import index, home

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('home', home,name="home"),
    path('search-product/', SearchProductView.as_view(), name='search-product'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)