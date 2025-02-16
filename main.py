import tkinter
import customtkinter
import re
from pytubefix import YouTube
from logger_definition import logger

# TODO: Make input with 3 dots for audio, video or audio and video option
# TODO: Make it to a standalone runnable

# Example: https://www.youtube.com/watch?v=c9eGtyqz4gY

def is_valid_youtube_url(url):
    youtube_regex = (
    r'(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
)
    return re.match(youtube_regex, url) is not None

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    download_percentage = (bytes_downloaded / total_size) * 100
    logger.info("Progress: %s", download_percentage)
    percentage_text = str(int(download_percentage))
    
    progress_percentage_label.configure(text=percentage_text + "%")
    progress_percentage_label.update()
    
    progress_bar.set(float(download_percentage)/100)
    progress_bar.update()
    

def startDownload():
    try:
        ytLink = link_input.get().strip()
        
        if not is_valid_youtube_url(ytLink):
            finished_label.configure(text="Invalid YouTube URL. Please enter a valid link.", text_color="red")
            logger.error("Invalid YouTube URL. Please enter a valid link.")
            return
        
        ytObject = YouTube(ytLink,  on_progress_callback=on_progress)
        video = ytObject.streams.filter(only_video=True).order_by('bitrate').desc().first()
        
        title_label.configure(text=ytObject.title, text_color="white")
        finished_label.configure(text="")
        
        video.download()
        logger.info("Download job success")
        finished_label.configure(text="Download job success", text_color="green")
    except Exception as e:
        finished_label.configure(text="Error occurred during download.", text_color="red")
        logger.exception("Error occurred during download")
    

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App settings
app = customtkinter.CTk()
app.geometry("710x480")
app.title("Youtube Downloader")

# UI
title_label = customtkinter.CTkLabel(app, text="Add youtube link")
title_label.pack(padx=10, pady=10)

# Link Input
url_var = tkinter.StringVar()
prev = ""
link_input = customtkinter.CTkEntry(app, width=300, height=50, textvariable=url_var)
link_input.pack()

# Finished download
finished_label = customtkinter.CTkLabel(app, text="")
finished_label.pack()


# Progress percentage
progress_percentage_label = customtkinter.CTkLabel(app, text="0%")
progress_percentage_label.pack()

# Progress bar
progress_bar = customtkinter.CTkProgressBar(app, width=400)
progress_bar.set(0.0)
progress_bar.pack()

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=11)

# Run app
app.mainloop()