import os
from flask import Flask, request, render_template, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    format_choice = request.form.get('format_choice')

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio' if format_choice == 'mp4' else 'bestaudio/best',
        }

        if format_choice == 'mp3':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

            if format_choice == 'mp3':
                mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
                return send_file(mp3_filename, as_attachment=True)

            return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=f"Error downloading the video: {str(e)}")

if __name__ == '__main__':
    # Get the PORT from the environment variable and default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
