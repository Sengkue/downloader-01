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
        # Set options for yt-dlp based on format type
        ydl_opts = {
            'format': 'bestaudio' if format_type == 'audio' else 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video/audio information and download
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send file to the user
        response = send_file(filename, as_attachment=True)

        # Delete the file after sending
        os.remove(filename)

        return response

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Create downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
