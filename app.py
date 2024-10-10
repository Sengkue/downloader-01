# Save this file as app.py
from flask import Flask, request, render_template, send_file
import yt_dlp
import os  # Keep this for path handling

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    format_choice = request.form.get('format_choice')

    try:
        # Create downloads folder if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # Set options for yt-dlp
        if format_choice == 'mp4':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
        else:  # format_choice == 'mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        # Download the video/audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

            # If MP3, the file should already be converted by yt-dlp
            if format_choice == 'mp3':
                mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
                return send_file(mp3_filename, as_attachment=True)

            # Return MP4 file
            return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=f"Error downloading the video: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
