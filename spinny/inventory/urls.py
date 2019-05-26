from .views import ListCreateBox, ListUserBoxes,BoxUpdateDeleteManageView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', ListCreateBox.as_view()),
    url(r'^(?P<pk>\d+)$', BoxUpdateDeleteManageView.as_view(), name="Update and delete boxes"),
    url(r'list_user_boxes',ListUserBoxes.as_view(), name="list user's boxes"),
]
