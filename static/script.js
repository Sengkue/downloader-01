document.addEventListener("DOMContentLoaded", function () {
    const videoUrlInput = document.getElementById("video-url");
    const pasteButton = document.getElementById("paste-button");
    const clearButton = document.getElementById("clear-button");

    pasteButton.addEventListener("click", () => {
        navigator.clipboard.readText()
            .then(text => {
                videoUrlInput.value = text;
                clearButton.style.display = 'inline-block'; // Show clear button when text is pasted
            })
            .catch(err => {
                console.error('Failed to read clipboard contents: ', err);
            });
    });

    clearButton.addEventListener("click", () => {
        videoUrlInput.value = '';
        clearButton.style.display = 'none'; // Hide clear button when input is cleared
    });

    // Show/hide clear button based on input
    videoUrlInput.addEventListener("input", () => {
        clearButton.style.display = videoUrlInput.value ? 'inline-block' : 'none';
    });
});
