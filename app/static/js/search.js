function showSuggestions() {
    var input = document.getElementById("searchInput").value;
    var suggestionsContainer = document.getElementById("suggestions");

    // Clear previous suggestions
    suggestionsContainer.innerHTML = '';

    // Show suggestions only if there is input
    if (input.length > 0) {
        // Make an AJAX request to the Flask route to get suggestions
        fetch('/get_suggestions?search_term=' + input)
            .then(response => response.json())
            .then(data => {
                // Display suggestions
                data.forEach(function (suggestion) {
                    var suggestionElement = document.createElement("div");
                    suggestionElement.classList.add("suggestion");
                    suggestionElement.textContent = suggestion;

                    suggestionElement.onclick = function () {
                        navigateToProfile(suggestion); // Call a function to navigate to the profile
                    };

                    suggestionsContainer.appendChild(suggestionElement);
                });

                // Show suggestions container
                suggestionsContainer.style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
    } else {
        suggestionsContainer.style.display = 'none';
    }    
}

// Function to navigate to the profile
function navigateToProfile(username) {
    // Modify this function to navigate to the desired URL
    window.location.href = '/profile/' + username;
}

function hideSuggestions() {
    var suggestionsContainer = document.getElementById("suggestions");
    suggestionsContainer.style.display = 'none';
}

function performSearch() {
    var searchTerm = document.getElementById("searchInput").value;
    alert("Searching for: " + searchTerm);
}


    
    
