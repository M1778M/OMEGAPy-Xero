document.getElementById('api-key-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    const apiKeyInput = document.getElementById('api-key');
    const apiKey = apiKeyInput.value;
    const messageElement = document.getElementById('message');

    // Simulate checking the API key
    if (validateApiKey(apiKey)) {
        messageElement.style.color = "#4caf50"; // Green for success
        messageElement.textContent = "API Key accepted! Proceeding...";
    } else {
        messageElement.style.color = "#ff5722"; // Red for error
        messageElement.textContent = "Invalid API Key. Please try again.";
    }

    // Clear the input field after submission
    apiKeyInput.value = '';
});

function validateApiKey(apiKey) {
    // For demonstration purposes, we will accept any non-empty string.
    // In a real application, you would check your API key against a database or service.
    return apiKey.trim() !== '';
}