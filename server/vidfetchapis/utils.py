def convert_data_to_storable_format(response: dict) -> dict:
    """
    Takes response data from YouTube API and converts it to
    a format which can be stored in the database - removes
    irrelevant information and stores in accessible format

    Args:
        response: Response Data from API

    Returns:
        dict
    """
    res_data = response["items"]

    video_data = {}

    for items in res_data:
        vid_data = items["snippet"]

        publish_date = vid_data["publishedAt"]
        title = vid_data["title"]
        description = vid_data["description"]
        channel = vid_data["channelTitle"]

        thumbnail_data = vid_data["thumbnails"]
        default_thumbnail = thumbnail_data["default"]
        default_url = default_thumbnail["url"]
        medium_thumbnail = thumbnail_data["medium"]
        medium_url = medium_thumbnail["url"]
        high_thumbnail = thumbnail_data["high"]
        high_url = high_thumbnail["url"]

        thumbnail_urls = {}
        thumbnail_urls["default"] = default_url
        thumbnail_urls["medium"] = medium_url
        thumbnail_urls["high"] = high_url

        data = {}
        data["title"] = title
        data["description"] = description
        data["channel"] = channel
        data["thumbnail_urls"] = thumbnail_urls

        video_data[publish_date] = data

    return video_data
