# Save this file as app.py
from flask import Flask, request, render_template, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Global variable to track download progress
download_progress = {"status": "idle", "progress": 0, "eta": 0}

# Progress hook to track download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0)
        if total > 0:
            progress_percent = int(downloaded / total * 100)
            download_progress['status'] = 'downloading'
            download_progress['progress'] = progress_percent
            
            # Estimate time remaining (in seconds)
            if d.get('elapsed', 0) > 0:
                estimated_time = (total - downloaded) / (downloaded / d['elapsed'])
                download_progress['eta'] = int(estimated_time)
            else:
                download_progress['eta'] = 0
    elif d['status'] == 'finished':
        download_progress['status'] = 'finished'
        download_progress['progress'] = 100
        download_progress['eta'] = 0

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    format_choice = request.form.get('format_choice')

    global download_progress
    download_progress = {"status": "idle", "progress": 0, "eta": 0}  # Reset progress

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'format': 'bestvideo+bestaudio' if format_choice == 'mp4' else 'bestaudio/best',
        }

        if format_choice == 'mp3':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

            if format_choice == 'mp3':
                mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
                return send_file(mp3_filename, as_attachment=True)

            return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=f"Error downloading the video: {str(e)}")

@app.route('/progress', methods=['GET'])
def progress():
    return jsonify(download_progress)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
