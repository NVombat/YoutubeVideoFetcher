from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import response

from .utils import fetch_vid_data

class FetchVidData(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, **kwargs) -> response.JsonResponse:
        """Fetching Youtube Video Data when hit with GET requests

        Args:
            request ([type])

        Returns:
            JsonResponse
        """

        print("Fetching Video Data API")

        vid_data = fetch_vid_data(request, **kwargs)

        return vid_data
