import os
import tkinter
import customtkinter
from ffmpeg import FFmpeg
from pytubefix import YouTube
from logger_definition import logger
from format_options import FormatOptions
from utils import is_valid_youtube_url

# TODO: Merged file name bug
# TODO: Set progress to 0 after successful or error event

# TODO: List downloaded files
# TODO: Clear button
# TODO: Icon update
# TODO: Add target folder input path

temporary_video_file_name = "temporary_video.mp4"
temporary_audio_file_name = "temporary_audio.mp4"


def set_progress_data(download_percentage):
    percentage_text = str(int(download_percentage))

    progress_percentage_label.configure(text=percentage_text + "%")
    progress_percentage_label.update()

    progress_bar.set(float(download_percentage) / 100)
    progress_bar.update()

    logger.info("Progress set to: %s", download_percentage)


def _on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    download_percentage = (bytes_downloaded / total_size) * 100
    logger.info("Progress: %s", download_percentage)
    set_progress_data(download_percentage)


def _clearInput():
    link_input.delete(0, "end")


def _startDownload():
    try:
        youtube_link = link_input.get().strip()

        if not is_valid_youtube_url(youtube_link):
            finished_label.configure(
                text="Invalid YouTube URL. Please enter a valid link.", text_color="red"
            )
            logger.error("Invalid YouTube URL. Please enter a valid link.")
            return

        set_progress_data(0)
        
        download.configure(state="disabled")
        
        ytObject = YouTube(youtube_link, on_progress_callback=_on_progress)

        format_option = option_menu.get().strip()

        if format_option == "Video" or format_option == "Audio":
            video = _defineYoutubeStream(format_option, ytObject)
            title_label.configure(text=ytObject.title, text_color="white")
            finished_label.configure(text="")

            logger.info("Download has started with %s format", format_option)

            video.download()
            logger.info("Download job success")
            finished_label.configure(text="Download job success", text_color="green")
            
            download.configure(state="normal")
        else:
            temporary_video_stream = (
                ytObject.streams.filter(only_video=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
                .first()
            )
            temporary_audio_stream = (
                ytObject.streams.filter(only_audio=True, mime_type="audio/mp4")
                .order_by("abr")
                .desc()
                .first()
            )

            if not temporary_video_stream or not temporary_audio_stream:
                logger.error("Could not find suitable streams")
                return

            temporary_video_file = temporary_video_stream.download(
                filename=temporary_video_file_name
            )
            temporary_audio_file = temporary_audio_stream.download(
                filename=temporary_audio_file_name
            )

            # Example: https://www.youtube.com/watch?v=c9eGtyqz4gY
            title = ytObject.title.replace(" ", "_")
            output_file = title + ".mp4"
            if not os.path.exists(temporary_video_file) or not os.path.exists(
                temporary_audio_file
            ):
                logger.error("Video of audio file not existing for merging")
            else:
                try:
                    (
                        FFmpeg()
                        .option("y")
                        .input(temporary_video_file)
                        .input(temporary_audio_file)
                        .output(output_file, vcodec="copy", acodec="aac")
                        .execute()
                    )

                    os.remove(temporary_video_file)
                    os.remove(temporary_audio_file)
                    download.configure(state="disabled")

                except Exception as e:
                    print("FFmpeg Error:", e.stderr.decode())

            logger.info("Download job success for merged file: %s", output_file)
            download.configure(state="normal")

    except Exception as e:
        finished_label.configure(
            text="Error occurred during download.", text_color="red"
        )
        download.configure(state="normal")
        logger.exception("Error occurred during download")


def _defineYoutubeStream(format, ytObject):
    try:
        match format:
            case "Video":
                return (
                    ytObject.streams.filter(only_video=True, file_extension="mp4")
                    .order_by("bitrate")
                    .desc()
                    .first()
                )
            case "Audio":
                return (
                    ytObject.streams.filter(only_audio=True)
                    .order_by("bitrate")
                    .desc()
                    .first()
                )
    except Exception as e:
        logger.exception("Error occurred during stream settings")


def optionmenu_callback(choice):
    logger.info("Format set to: %s", choice)


# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


# App settings
app = customtkinter.CTk()
app.geometry("710x480")
app.title("Youtube Downloader")


# Title label
title_label = customtkinter.CTkLabel(app, text="Add youtube link")
title_label.pack(padx=10, pady=10)


# Option for format
option_menu = customtkinter.CTkOptionMenu(
    master=app,
    values=[color.value for color in FormatOptions],  # Extract values from Enum
    command=optionmenu_callback,  # Callback function
)

option_menu.pack(pady=20)
option_menu.set(FormatOptions.VIDEO.value)


# Create a frame for input
frame = customtkinter.CTkFrame(app)
frame.pack(pady=20, padx=20)


# Link Input
url_var = tkinter.StringVar()
prev = ""
link_input = customtkinter.CTkEntry(frame, width=300, height=50, textvariable=url_var)
link_input.pack(side="left", padx=10)


# Clear button
clear = customtkinter.CTkButton(frame, text="Clear input", command=_clearInput)
clear.pack(side="left")


# Finished download
finished_label = customtkinter.CTkLabel(app, text="")
finished_label.pack()


# Progress percentage
progress_percentage_label = customtkinter.CTkLabel(app, text="0%")
progress_percentage_label.pack()


# Download button
download = customtkinter.CTkButton(app, text="Download", command=_startDownload)
download.pack(padx=10, pady=11)


# Progress bar
progress_bar = customtkinter.CTkProgressBar(app, width=400)
progress_bar.set(0.0)
progress_bar.pack()


# Run app
app.mainloop()
