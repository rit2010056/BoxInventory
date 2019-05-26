from rest_framework.authtoken import views
from django.conf.urls import url

urlpatterns = [
    url(r'^api-token-auth/', views.obtain_auth_token)
]