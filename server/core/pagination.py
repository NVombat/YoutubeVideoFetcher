from rest_framework import status
from django.http import response
from math import ceil

from vidfetchapis.errors import (
    KeywordNotFoundError,
    PageNotFoundError,
)

ITEMS_PER_PAGE = 2


class CustomPagination:
    def get_paginated_data(
        self, page: int, data: list, search_query: str
    ) -> response.JsonResponse:
        """
        Paginates Data & Adds Page Related Meta Data

        Args:
            page: Page Number
            data: Data To Be Paginated
            search_query: Search Query

        Returns:
            response.JsonResponse
        """
        total_docs = len(data)

        # If Page Number Does Not Exist
        if page <= 0 or page > ceil(total_docs / ITEMS_PER_PAGE):
            raise PageNotFoundError("This Page Does Not Exist")
        # If No Page Is Specified
        elif page == None:
            page = 1

        left_lim = (page - 1) * ITEMS_PER_PAGE
        right_lim = left_lim + ITEMS_PER_PAGE

        if total_docs != 0:
            return response.JsonResponse(
                {
                    "currentPage": page,
                    "hasNextPage": ITEMS_PER_PAGE * page < total_docs,
                    "hasPreviousPage": page > 1,
                    "nextPage": page + 1,
                    "previousPage": page - 1,
                    "lastPage": ceil(total_docs / ITEMS_PER_PAGE),
                    "data": data[left_lim:right_lim],
                },
                status=status.HTTP_200_OK,
            )
        else:
            raise KeywordNotFoundError(
                f"Data For {search_query} Not Found In Database - Fetching Results For {search_query}. Please Try Again In A Moment"
            )
