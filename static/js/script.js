document.addEventListener('DOMContentLoaded', function() {
    console.log('Rental Scanner JS Loaded');

    const searchForm = document.getElementById('searchForm');
    const searchButton = document.getElementById('searchButton');
    const searchButtonText = document.getElementById('searchButtonText');
    const searchButtonSpinner = document.getElementById('searchButtonSpinner');
    const searchIcon = document.getElementById('searchIcon');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (searchForm && searchButton) {
        searchForm.addEventListener('submit', function(event) {
            // Show overlay
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex';
            }

            // Show spinner and disable button
            if (searchButtonText) {
                searchButtonText.textContent = 'Searching...';
            }
            if (searchButtonSpinner) {
                searchButtonSpinner.classList.remove('d-none');
            }
            if (searchIcon) {
                searchIcon.classList.add('d-none');
            }
            searchButton.disabled = true;
        });
    }

    // Handle back/forward button and page load
    function resetSearchUI() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
        if (searchButton) {
            searchButton.disabled = false;
            if (searchButtonText) {
                searchButtonText.textContent = 'Search All Sources';
            }
            if (searchButtonSpinner) {
                searchButtonSpinner.classList.add('d-none');
            }
            if (searchIcon) {
                searchIcon.classList.remove('d-none');
            }
        }
    }

    window.addEventListener('pageshow', resetSearchUI);
    window.addEventListener('load', resetSearchUI);
});

// Sort listings by price
function sortListings(by) {
    const container = document.querySelector('.results-card .card-body');
    const listings = Array.from(document.querySelectorAll('.listing-card'));

    if (by === 'price') {
        listings.sort((a, b) => {
            return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
        });
    }

    listings.forEach(listing => container.appendChild(listing));
}

// Filter by source
function filterBySource(source) {
    const listings = document.querySelectorAll('.listing-card');

    listings.forEach(listing => {
        if (source === 'all' || listing.dataset.source === source) {
            listing.style.display = 'block';
        } else {
            listing.style.display = 'none';
        }
    });
}
