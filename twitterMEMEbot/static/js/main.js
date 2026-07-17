
// Fetch memes from server
async function fetchMemes() {
    try {
        const response = await fetch('/api/memes');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        showError(`Failed to fetch memes: ${error.message}`);
        return [];
    }
}

function showError(message) {
    const errorLog = document.getElementById('errorLog');
    const errorMessage = document.getElementById('errorMessage');
    errorLog.classList.remove('d-none');
    errorMessage.textContent = message;
    setTimeout(() => {
        errorLog.classList.add('d-none');
    }, 5000);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const fetchBtn = document.getElementById('fetchAndGenerateBtn');
    fetchBtn.addEventListener('click', async () => {
        try {
            const memes = await fetchMemes();
            displayMemes(memes);
        } catch (error) {
            showError(`Operation failed: ${error.message}`);
        }
    });
});
