from yt_transcriber import extract_video_id


def test_extract_video_id_standard_watch():
    url = "https://www.youtube.com/watch?v=DPmtnb8NBog"
    assert extract_video_id(url) == "DPmtnb8NBog"


def test_extract_video_id_short_url():
    url = "https://youtu.be/DPmtnb8NBog"
    assert extract_video_id(url) == "DPmtnb8NBog"


def test_extract_video_id_embed():
    url = "https://www.youtube.com/embed/DPmtnb8NBog"
    assert extract_video_id(url) == "DPmtnb8NBog"


def test_extract_video_id_shorts():
    url = "https://www.youtube.com/shorts/DPmtnb8NBog"
    assert extract_video_id(url) == "DPmtnb8NBog"


def test_extract_video_id_invalid():
    assert extract_video_id("https://example.com") is None
