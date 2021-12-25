from core.errorfactory import DatabaseSearchErrors, PaginationErrors


class KeywordNotFoundError(DatabaseSearchErrors):
    ...


class PageNotFoundError(PaginationErrors):
    ...
