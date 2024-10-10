// JavaScript to handle pasting the URL
const pasteButton = document.getElementById('paste-button');
const videoUrlInput = document.getElementById('video-url');

// Check if Clipboard API is available and supported
if (navigator.clipboard && navigator.clipboard.readText) {
    pasteButton.addEventListener('click', function() {
        navigator.clipboard.readText()
            .then(text => {
                videoUrlInput.value = text;
            })
            .catch(err => {
                console.error('Failed to read clipboard contents: ', err);
                alert('Failed to paste from clipboard. Please try again.');
            });
    });
} else {
    // If Clipboard API is not supported, disable the paste button and notify the user
    pasteButton.disabled = true;
    alert("Clipboard functionality is not supported in this environment. Please paste the link manually.");
}
