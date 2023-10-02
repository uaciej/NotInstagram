from django.urls import path
from .views import CustomObtainAuthToken


urlpatterns = [
    # ...
    path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    # ...
]
