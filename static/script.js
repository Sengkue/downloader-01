document.getElementById('downloadForm').addEventListener('submit', function(event) {
    // Show the progress container when the download starts
    document.getElementById('progress-container').style.display = 'block';
    
    // Prevent the default form submission
    event.preventDefault();

    // Start the download process
    fetch('/download', {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target)),
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();  // Assuming a successful download returns a blob
    }).then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'video.mp4'; // Set the default file name for download
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.getElementById('progress-container').style.display = 'none'; // Hide progress after download
    }).catch(error => {
        console.error('There was an error!', error);
    });

    // Start polling for download progress
    pollProgress();
});

function pollProgress() {
    const interval = setInterval(() => {
        fetch('/progress')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'downloading') {
                    document.getElementById('progress-bar').style.width = data.progress + '%';
                    document.getElementById('progress-text').innerText = data.progress + '%';
                } else if (data.status === 'finished') {
                    document.getElementById('progress-bar').style.width = '100%';
                    document.getElementById('progress-text').innerText = '100% - Download complete!';
                    clearInterval(interval); // Stop polling
                }
            });
    }, 1000);  // Poll every second
}
