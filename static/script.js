document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form submission
    document.getElementById('progress-container').style.display = 'block';  // Show the progress container

    const formData = new FormData(this);
    fetch('/download', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'video.mp4'; // Adjust according to your needs
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.getElementById('progress-container').style.display = 'none'; // Hide progress when done
    })
    .catch(error => {
        document.getElementById('error-message').innerText = `Error: ${error.message}`;
    });

    pollProgress();  // Start polling for progress
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
                    clearInterval(intervalId);  // Stop polling when finished
                }
            })
            .catch(err => {
                console.error("Error fetching progress: ", err);
            });
    }, 1000);  // Poll every second
}
