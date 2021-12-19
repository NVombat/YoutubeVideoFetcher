from .views import FetchVidData, GetStoredData
from django.urls import path

urlpatterns = [
    path("fetchvids", FetchVidData.as_view()),
    path("getdata", GetStoredData.as_view()),
]
