document.addEventListener('DOMContentLoaded', () => {
    const downloadForm = document.getElementById('downloadForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');

    if (downloadForm) {
        downloadForm.onsubmit = function() {
            loadingSpinner.style.display = 'block';
            progressContainer.style.display = 'block';
            const downloadButton = document.getElementById('downloadButton');
            downloadButton.disabled = true; // Disable button to prevent multiple submissions

            // Start the progress update loop
            const updateProgress = setInterval(() => {
                fetch('/progress')
                    .then(response => response.json())
                    .then(data => {
                        if (data.percent !== undefined) {
                            const percent = data.percent.toFixed(2);
                            progressBar.style.width = percent + '%';
                            progressText.innerText = percent + '%';

                            // Stop updating when download is complete
                            if (percent >= 100) {
                                clearInterval(updateProgress);
                                loadingSpinner.style.display = 'none';
                                downloadButton.disabled = false; // Re-enable the button
                            }
                        }
                    });
            }, 1000); // Update every second
        };
    }
});
