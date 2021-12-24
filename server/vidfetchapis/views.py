from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import response

from .tasks import fetch_vid_data, get_paginated_data
from core.pagination import CustomPagination

class FetchVidData(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, **kwargs) -> response.JsonResponse:
        """
        Fetching Youtube Video Data when hit with GET requests

        Args:
            request ([type])

        Returns:
            JsonResponse
        """

        print("Fetching Video Data API")

        vid_data = fetch_vid_data(request, **kwargs)

        return vid_data


class GetStoredData(APIView):
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)

    def get(self, request, **kwargs) -> response.JsonResponse:
        """
        Get Data From Database when hit with GET requests &
        return paginated responses

        Args:
            request ([type])

        Returns:
            JsonResponse
        """

        print("Getting DB Data API")

        db_data = get_paginated_data(request, **kwargs)

        return self.get_paginated_response(db_data)
