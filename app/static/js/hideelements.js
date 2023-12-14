function hideElements() {
    // Hide profile card elements
    var profileCard = document.getElementById("profileInfo");
    profileCard.style.display = 'none';
    var profileChildElements = profileCard.children;

    for (var i = 0; i < profileChildElements.length; i++) {
        profileChildElements[i].style.display = 'none';
    }

    // Show update card elements
    var updateCard = document.getElementById("updateInfo");
    updateCard.style.display = 'block';
    var updateChildElements = updateCard.children;

    for (var j = 0; j < updateChildElements.length; j++) {
        updateChildElements[j].style.display = 'flex';
    }
}