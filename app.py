from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os
import threading

app = Flask(__name__)

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']}")  # Debugging line

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as error:
        print(f"Error removing file: {error}")

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
        threading.Thread(target=delete_file, args=(file_path,)).start()
        return response

    return send_file(file_path, as_attachment=True)

@app.route('/progress/<video_id>', methods=['GET'])
def progress(video_id):
    return jsonify({'progress': download_progress.get(video_id, '0%')})

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
