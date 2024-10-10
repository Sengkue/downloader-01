# Save this file as app.py
from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os

app = Flask(__name__)

# Global variable to store download progress
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
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <style>
        body {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            font-family: Arial, sans-serif;
            color: #333;
            padding: 20px;
            text-align: center;
        }
        input[type="text"] {
            width: 300px;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #4facfe;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #4caf50;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        #progress-container {
            margin-top: 20px;
            background-color: #f3f3f3;
            border-radius: 25px;
            height: 25px;
            width: 100%;
            position: relative;
            display: none;
        }
        #progress-bar {
            background: linear-gradient(to right, #4caf50, #8bc34a);
            height: 100%;
            width: 0;
            border-radius: 25px;
            transition: width 0.5s ease-in-out;
        }
        #progress-text {
            position: absolute;
            width: 100%;
            text-align: center;
            line-height: 25px;
            color: black;
        }
        #eta-text {
            color: #ffcc00;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>YouTube Video Downloader</h1>
    <input type="text" id="video_url" placeholder="Paste your YouTube URL here">
    <br>
    <select id="format_choice">
        <option value="mp4">MP4</option>
        <option value="mp3">MP3</option>
    </select>
    <br>
    <button id="downloadBtn">Download</button>

    <div id="progress-container">
        <div id="progress-bar"></div>
        <span id="progress-text">0%</span>
        <span id="eta-text">Estimated time: N/A</span>
    </div>

    <script>
        document.getElementById('downloadBtn').addEventListener('click', function() {
            const videoUrl = document.getElementById('video_url').value;
            const formatChoice = document.getElementById('format_choice').value;
            
            // Show the progress container when the download starts
            document.getElementById('progress-container').style.display = 'block';

            fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `video_url=${encodeURIComponent(videoUrl)}&format_choice=${formatChoice}`
            }).then(response => {
                if (response.ok) {
                    // Start polling for download progress
                    pollProgress();
                } else {
                    alert('Error: ' + response.statusText);
                }
            });
        });

        function pollProgress() {
            const intervalId = setInterval(() => {
                fetch('/progress')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'downloading') {
                            document.getElementById('progress-bar').style.width = data.progress + '%';
                            document.getElementById('progress-text').innerText = data.progress + '%';
                            document.getElementById('eta-text').innerText = `Estimated time: ${data.eta} seconds`;
                        } else if (data.status === 'finished') {
                            document.getElementById('progress-bar').style.width = '100%';
                            document.getElementById('progress-text').innerText = '100% - Download complete!';
                            document.getElementById('eta-text').innerText = 'Estimated time: 0 seconds';
                            clearInterval(intervalId);
                        }
                    })
                    .catch(err => {
                        console.error("Error fetching progress: ", err);
                    });
            }, 1000);  // Poll every second
        }
    </script>
</body>
</html>
''')

@app.route('/download', methods=['POST'])
def download():
    global download_progress
    download_progress = {"status": "idle", "progress": 0, "eta": 0}  # Reset progress
    video_url = request.form.get('video_url')
    format_choice = request.form.get('format_choice')

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
        return {"error": str(e)}

@app.route('/progress')
def progress():
    return download_progress

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Bind to all interfaces on port 5000
