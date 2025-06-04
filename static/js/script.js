document.addEventListener('DOMContentLoaded', function() {
    console.log('RentalHunter JS Loaded');

    const searchForm = document.getElementById('searchForm');
    const searchButton = document.getElementById('searchButton');
    const searchButtonText = document.getElementById('searchButtonText');
    const searchButtonSpinner = document.getElementById('searchButtonSpinner');

    if (searchForm && searchButton) {
        searchForm.addEventListener('submit', function(event) {
            // Basic validation (though HTML 'required' handles empty location)
            const locationInput = document.getElementById('location');
            if (locationInput && locationInput.value.trim() === '') {
                // Optionally, add more sophisticated client-side validation here
                // For now, relying on 'required' attribute.
            }

            // Show spinner and disable button
            if(searchButtonText && searchButtonSpinner) {
                searchButtonText.textContent = 'Searching...';
                searchButtonSpinner.classList.remove('d-none'); // Show spinner
            }
            searchButton.disabled = true;
            
            // Optional: Clear previous results or show a loading message in results area
            const resultsArea = document.getElementById('resultsArea');
            if(resultsArea) {
                // resultsArea.innerHTML = '<p class="text-center text-muted mt-3">Loading results...</p>';
            }
        });
    }

    // Re-enable button if the page is reloaded (e.g., back button after submission)
    // This helps if the form submission was interrupted or if the user navigates back.
    window.addEventListener('pageshow', function(event) {
        if (searchButton && searchButton.disabled) {
            if(searchButtonText && searchButtonSpinner) {
                searchButtonText.textContent = 'Search Listings';
                searchButtonSpinner.classList.add('d-none'); // Hide spinner
            }
            searchButton.disabled = false;
        }
    });
});
