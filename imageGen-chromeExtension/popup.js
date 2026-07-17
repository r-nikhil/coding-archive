// popup.js
document.addEventListener('DOMContentLoaded', function() {
    const apiKeyInput = document.getElementById('api-key');
    const saveApiKeyButton = document.getElementById('save-api-key');
    const textPromptInput = document.getElementById('text-prompt');
    const generateImagesButton = document.getElementById('generate-images');
    const regenerateImagesButton = document.getElementById('regenerate-images');
    const downloadImagesButton = document.getElementById('download-images');
    const imageResultsContainer = document.getElementById('image-results');

    // Load saved API key if available
    console.log(apiKeyInput.value);
    console.log(textPromptInput.value);
    chrome.storage.sync.get('apiKey', function(data) {
        apiKeyInput.value = data.apiKey || '';
        console.log('api key found');
    });

    // Save the API key
    saveApiKeyButton.addEventListener('click', function() {
        const apiKey = apiKeyInput.value;
        chrome.storage.sync.set({ 'apiKey': apiKey }, function() {
            console.log('API Key saved');
        });
    });

    // Generate images
    generateImagesButton.addEventListener('click', function() {
        const prompt = textPromptInput.value;
        generateImages(prompt);
    });

    // Regenerate images
    regenerateImagesButton.addEventListener('click', function() {
        const prompt = textPromptInput.value;
        generateImages(prompt);
    });

    // Download images
    downloadImagesButton.addEventListener('click', function() {
        downloadImages();
    });

    function generateImages(prompt) {
        // Get the saved API key
        chrome.storage.sync.get('apiKey', function(data) {
            if (data.apiKey) {
                console.log('API Key is set.');
                const apiKey = data.apiKey;
                const headers = new Headers({
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                });

                const body = JSON.stringify({
                    prompt: prompt,
                });

                fetch('https://api.openai.com/v1/images/generations', {
                    method: 'POST',
                    headers: headers,
                    body: body
                })
                .then(response => response.json())
                .then(data => {
                    displayImages(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            } else {
                console.log('API Key is not set.');
            }
        });
    }
    function showSavedIcon() {
        const savedIcon = document.getElementById('saved-icon');
        savedIcon.style.display = 'inline-block';
        setTimeout(() => {
            savedIcon.style.display = 'none';
        }, 2000); // Hide the icon after 2 seconds
    }
    
    // Modify the save API key event listener
    saveApiKeyButton.addEventListener('click', function() {
        const apiKey = apiKeyInput.value;
        chrome.storage.sync.set({ 'apiKey': apiKey }, function() {
            console.log('API Key saved');
            showSavedIcon(); // Call this function after saving the API key
        });
    });
    function displayImages(result) {
        // Clear existing images
        imageResultsContainer.innerHTML = '';
    
        // Check if data is an array and has at least one item
        if (result.data && result.data.length> 0) {
            const img = document.createElement('img');
            img.src = result.data[0].url; // Access the 'url' property of the first image object
            img.classList.add('generated-image');
            imageResultsContainer.appendChild(img);
        } else {
            console.error('Unexpected data format or no image URL:', data);
        }
    }

    function downloadImages() {
        const images = imageResultsContainer.querySelectorAll('.generated-image');
        images.forEach((img, index) => {
            // Use the 'download' attribute of the anchor tag to download the image
            const a = document.createElement('a');
            a.href = img.src;
            // Provide a default name for the image file
            a.download = `generated-image-${index}.png`; // Assuming the image is in PNG format
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
    }
});