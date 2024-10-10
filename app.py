from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Folder to save the downloaded video
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_file = ydl.prepare_filename(info_dict)
        
        return jsonify({"status": "success", "file": video_file, "title": video_title})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download_file/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
