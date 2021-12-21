from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.http import response
from datetime import datetime
import asyncio
import httpx

from .utils import fetch_vid_data, get_paginated_data
from core.pagination import CustomPagination
from .asyncrequests import test_request


async def http_call_async():
    for num in range(1, 5):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        url = test_request()
        r = await client.get(url=url)
        print(r.status_code)
        print(r.content)
        return r.status_code


async def main():
    start = datetime.now()

    task = asyncio.create_task(http_call_async())
    await task

    exec_time = (datetime.now() - start).seconds
    print(f"Execution Time {exec_time}s\n")


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
        # vid_data = fetch_vid_data(request, **kwargs)
        # return vid_data

        asyncio.run(main())

        return response.JsonResponse(
            {"success_status": True},
            status=status.HTTP_200_OK,
        )

    # async def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     return super().__call__(*args, **kwds)


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

        return db_data
