from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os
import time

app = Flask(__name__)

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']}")  # Debugging line

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format = request.form['format']
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio',
        'outtmpl': f'downloads/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else []
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
        if format == 'mp3':
            file_path = file_path.replace('.webm', '.mp3').replace('.mp4', '.mp3')

    @after_this_request
    def remove_file(response):
        try:
            time.sleep(1)  # Delay to ensure file is no longer in use
            os.remove(file_path)
        except Exception as error:
            print(f"Error removing file: {error}")
        return response

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
