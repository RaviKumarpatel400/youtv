from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Set absolute path for the downloads folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")

# Create the downloads folder if it doesn’t exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(url, choice):
    """Download video or audio and save correctly in 'downloads' folder"""
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',  # Save in downloads folder
        'noplaylist': True,  # Avoid downloading entire playlists
    }

    if choice == "audio":
        ydl_opts["format"] = "bestaudio[ext=m4a]/bestaudio"  # Highest-quality audio (M4A)
    else:
        ydl_opts["format"] = "best[height<=1080][ext=mp4]/best"  # Best MP4 format (up to 1080p)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        file_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(filename))
        return file_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        choice = request.form["choice"]

        try:
            file_path = download_video(url, choice)
            filename = os.path.basename(file_path)
            return render_template("download.html", filename=filename)
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    """Allow user to download the file from the 'downloads' folder"""
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
