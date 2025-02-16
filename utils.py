import re

def is_valid_youtube_url(url):
    youtube_regex = (
    r'(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
)
    return re.match(youtube_regex, url) is not None