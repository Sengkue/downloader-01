document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('downloadForm');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const clearIcon = document.getElementById('clear-icon');
    const videoUrlInput = document.getElementById('video-url');

    // Log to see if elements are found
    console.log('Form:', form);
    console.log('Progress Container:', progressContainer);
    console.log('Progress Bar:', progressBar);
    console.log('Progress Text:', progressText);
    console.log('Clear Icon:', clearIcon);
    console.log('Video URL Input:', videoUrlInput);

    if (!form || !progressContainer || !progressBar || !progressText || !clearIcon || !videoUrlInput) {
        console.error('One or more elements could not be found in the DOM.');
        return; // Exit early if elements are missing
    }

    form.addEventListener('submit', function(event) {
        // Show the progress container when the download starts
        progressContainer.style.display = 'block';
        progressText.innerText = '0%';
        progressBar.style.width = '0%';

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
            progressContainer.style.display = 'none'; // Hide progress after download
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
                        progressBar.style.width = data.progress + '%';
                        progressText.innerText = data.progress + '%';
                    } else if (data.status === 'finished') {
                        progressBar.style.width = '100%';
                        progressText.innerText = '100% - Download complete!';
                        clearInterval(interval); // Stop polling
                    }
                }).catch(error => console.error('Error fetching progress:', error));
        }, 1000);  // Poll every second
    }

    window.pasteUrl = function() {
        navigator.clipboard.readText().then(text => {
            videoUrlInput.value = text;
            clearIcon.style.display = 'inline'; // Show clear icon
        });
    };

    window.clearUrl = function() {
        videoUrlInput.value = '';
        clearIcon.style.display = 'none'; // Hide clear icon
    };
});
