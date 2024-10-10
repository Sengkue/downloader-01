document.getElementById('downloadForm').addEventListener('submit', function(event) {
    // Show the progress container when the download starts
    document.getElementById('progress-container').style.display = 'block';

    // Start polling for download progress
    pollProgress();
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
                    clearInterval(intervalId);  // Stop polling once finished
                }
            })
            .catch(err => {
                console.error("Error fetching progress: ", err);
            });
    }, 1000);  // Poll every second
}
