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
    format_type = request.form['format']
    
    try:
        # Set options based on user selection
        ydl_opts = {
            'format': 'bestaudio' if format_type == 'audio' else 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        # Download the video/audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send the file to the user
        response = send_file(filename, as_attachment=True)

        # After sending the file, delete it from the server
        os.remove(filename)  # This will delete the file after sending
        return response

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Create the downloads folder if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
