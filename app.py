from flask import Flask, request, render_template, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)
download_progress = {"status": "", "progress": 0}  # Global variable to store progress

# Progress hook to track download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0)
        if total > 0:
            progress_percent = int(downloaded / total * 100)
            download_progress['status'] = 'downloading'
            download_progress['progress'] = progress_percent
        else:
            download_progress['progress'] = 0

    elif d['status'] == 'finished':
        download_progress['status'] = 'finished'
        download_progress['progress'] = 100

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    format_choice = request.form.get('format_choice')

    global download_progress
    download_progress = {"status": "", "progress": 0}  # Reset progress

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],  # Add progress hook
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
def get_progress():
    """Endpoint to return the current download progress"""
    return jsonify(download_progress)

if __name__ == '__main__':
    # Automatically bind to the correct port for Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # No SSL context needed for Render
