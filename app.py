from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    download_type = request.form.get('type', 'video')  # Default to video if no type is provided

    ydl_opts = {
        'format': 'best' if download_type == 'video' else 'bestaudio',
        'outtmpl': '-',  # Output to stdout (streaming)
    }

    try:
        # Use BytesIO to store the file in memory instead of on disk
        buffer = io.BytesIO()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'downloaded_video')
            
            # Download the video/audio and stream it to memory
            ydl.download([url])
            
        buffer.seek(0)  # Rewind the buffer

        # Send the file to the user without storing it permanently
        if download_type == 'video':
            return send_file(buffer, as_attachment=True, download_name=f"{video_title}.mp4", mimetype='video/mp4')
        else:
            return send_file(buffer, as_attachment=True, download_name=f"{video_title}.mp3", mimetype='audio/mp3')

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
