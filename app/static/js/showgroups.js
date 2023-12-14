function showAddGroupForm() {
    var addGroupButton = document.getElementById('addGroupButton');
    var addGroupForm = document.getElementById('addGroupForm');
    
    // Hide the "Add Group" button
    addGroupButton.style.display = 'none';
    
    // Display the form
    addGroupForm.style.display = 'block';
}

function createGroup() {
    // Add logic to handle group creation here
    
    // Hide the form after submitting
    var addGroupButton = document.getElementById('addGroupButton');
    var addGroupForm = document.getElementById('addGroupForm');
    
    // Display the "Add Group" button
    addGroupButton.style.display = 'inline';
    
    // Hide the form
    addGroupForm.style.display = 'none';
}