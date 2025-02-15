import tkinter
import customtkinter
import re
from pytubefix import YouTube
from logger_definition import logger

# TODO: Make input with 3 dots for audio, video or audio and video option

def is_valid_youtube_url(url):
    youtube_regex = (
    r'(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
)
    return re.match(youtube_regex, url) is not None

def startDownload():
    try:
        ytLink = link_input.get().strip()
        
        if not is_valid_youtube_url(ytLink):
            logger.error("Invalid YouTube URL. Please enter a valid link.")
            return
        
        ytObject = YouTube(ytLink)
        video = ytObject.streams.filter(only_video=True).order_by('bitrate').desc().first()
        video.download()
        logger.info("Download job success")
    except Exception as e:
        logger.exception("Error occurred during download")

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App settings
app = customtkinter.CTk()
app.geometry("710x480")
app.title("Youtube Downloader")

# UI
title = customtkinter.CTkLabel(app, text="Add youtube link")
title.pack(padx=10, pady=10)

# Link Input
url_var = tkinter.StringVar()
prev = ""
link_input = customtkinter.CTkEntry(app, width=300, height=50, textvariable=url_var)
link_input.pack()

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run app
app.mainloop()