from .views import FetchVidData
from django.urls import path

urlpatterns = [
    path("fetchvids", FetchVidData.as_view()),
]
