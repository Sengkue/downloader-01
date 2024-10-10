// JavaScript to handle pasting the URL
const pasteButton = document.getElementById('paste-button');
const videoUrlInput = document.getElementById('video-url');

pasteButton.addEventListener('click', function() {
    // Check if the clipboard API is supported
    navigator.clipboard.readText()
        .then(text => {
            videoUrlInput.value = text;
        })
        .catch(err => {
            console.error('Failed to read clipboard contents: ', err);
            alert('Failed to paste from clipboard. Please try again.');
        });
});
