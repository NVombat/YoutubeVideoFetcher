from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.http import response

from .tasks import fetch_vid_data, get_paginated_data


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

        if vid_data:
            return response.JsonResponse(
                {"success_status": True},
                status=status.HTTP_200_OK,
            )
        else:
            return response.JsonResponse(
                {"error": "Error Occured While Fetching Data", "success_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetStoredData(APIView):
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

        return db_data
