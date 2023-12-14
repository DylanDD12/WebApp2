function triggerFileInput() {
        document.getElementById('upload').click();
    }

    function loadImage(event) {
        const input = event.target;
        const formData = new FormData();
        formData.append('file', input.files[0]);

        // Get the username from the HTML element or another source
        const username = document.getElementById('username').value;

        // Create a new XMLHttpRequest
        const xhr = new XMLHttpRequest();

        // Open a POST request to the /upload route with the username in the URL
        xhr.open('POST', `/upload/${username}`, true);

        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Image uploaded successfully');
                // Redirect to the home page after a successful upload
                window.location.href = '/home';
            } else {
                console.error('Error uploading image');
                window.location.href = '/home/'+ username;

            }
        }

        // Send the FormData
        xhr.send(formData);
    }