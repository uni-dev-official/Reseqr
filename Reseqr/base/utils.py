import re
from urllib.parse import urlparse, parse_qs

def youtube_to_embed(url, origin="http://127.0.0.1:8000"):
    """
    Converts a YouTube URL into a safe embed URL.
    Returns None if URL is invalid.
    """

    if not url:
        return None

    video_id = None

    # youtu.be/VIDEO_ID
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]

    # youtube.com/watch?v=VIDEO_ID
    elif "youtube.com" in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        video_id = qs.get("v", [None])[0]

        # already embed format
        if "/embed/" in parsed.path:
            video_id = parsed.path.split("/embed/")[-1]

    if not video_id:
        return None

    return (
        f"https://www.youtube.com/embed/{video_id}"
        f"?enablejsapi=1&origin={origin}"
    )
