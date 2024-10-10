from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        # Create a temporary directory to store downloads
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        # Options to download both video and audio
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',  # convert to mp4
                'preferedformat': 'mp4',  # change as needed
            }],
        }
        
        # Download the video and audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send the file to the user
        response = send_file(filename, as_attachment=True)

        # Delete the file after sending it to the user
        @response.call_on_close
        def remove_file():
            if os.path.exists(filename):
                os.remove(filename)

        return response

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
