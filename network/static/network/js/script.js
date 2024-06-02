document.addEventListener('DOMContentLoaded', function () {
    // Function to get the value of a cookie by its name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to create an edit form for a post
    function createEditForm(parentElem) {
        // Get the body element of the post
        const body = parentElem.querySelector('.card-body');
        // Get the post ID from the parent element's ID
        const postId = parentElem.getAttribute('id').split('-')[1];
        // Store the original content of the post body
        const oldBodyContent = body.querySelector('.card-text').innerHTML;
        // Clear the post body to make space for the edit form
        body.innerHTML = '';
    
        // Create a form element
        const form = document.createElement('form');
        form.classList.add('mb-3');
        form.setAttribute('data-id', parentElem.getAttribute('id'));
        form.action = `/post/${postId}`;
    
        // Create a div for form elements
        const div = document.createElement('div');
        div.classList.add('form-group');
    
        // Create a label for the textarea
        const label = document.createElement('label');
        label.innerHTML = 'Edit Post';
        label.htmlFor = 'postContent';
    
        // Create a textarea for editing the post content
        const textarea = document.createElement('textarea');
        textarea.style.width = '100%';
        textarea.classList.add('custom-textarea');
        textarea.classList.add('form-control');
        textarea.id = 'postContent';
        textarea.name = 'post';
        textarea.rows = 3;
        textarea.value = oldBodyContent;
    
        // Append elements to form
        div.append(label);
        div.append(textarea);
    
        // Create a submit button
        const input = document.createElement('input');
        input.classList.add('btn');
        input.classList.add('btn-primary');
        input.value = 'Post';
        input.type = 'submit';
    
        // Append elements to form
        form.append(div);
        form.append(input);
    
        // Add submit event listener to the form
        form.onsubmit = (e) => {
            e.preventDefault();
            // Get the post ID from the form's data attribute
            const postId = e.target.getAttribute('data-id').split('-')[1];
            // Get the updated post content from the form
            const updatedPost = e.target[0].value;
    
            // Get the CSRF token from the cookie
            const csrfToken = getCookie('csrftoken');
            // Create a request object with the CSRF token in the header
            const request = new Request(
                `/post/${postId}`,
                { headers: { 'X-CSRFToken': csrfToken } }
            );
    
            // Send a PUT request to update the post content
            fetch(request, {
                method: 'PUT',
                mode: 'same-origin',
                body: JSON.stringify({
                    id: postId,
                    body: updatedPost
                }),
            }).then(() => {
                // Update the post content dynamically
                //this does not work in darkmode 
                //replacePostContent(postId, body, updatedPost);
                //therefore we are going with this to ensure compability
                window.location.reload();
            });
        };
    
        // Append form to post body
        body.append(form);
    }
    // Function to replace the post content with updated content
    function replacePostContent(postId, parent, updatedPost) {
        // Clear the parent element
        parent.innerHTML = '';
    
        // Create a div for the post content
        const postContent = document.createElement('div');
        postContent.classList.add('card-body');
    
        // Create a pre element for displaying post content
        const postBody = document.createElement('pre');
        postBody.classList.add('card-text');
    
        // Apply the style to match the original HTML
        postBody.style.fontFamily = "Roboto, sans-serif";
        postBody.style.fontSize = "16px"; // Set font size
    
        postBody.textContent = updatedPost;
    
        // Append the post body to the post content div
        postContent.appendChild(postBody);
    
        // Append the post content to the parent element
        parent.appendChild(postContent);
    
        // Restore the existing buttons (like, comment, edit)
        const cardFooter = parent.closest('.card').querySelector('.card-footer');
        const likeButton = cardFooter.querySelector('.like-link');
        const editButton = cardFooter.querySelector('.edit-link');
    
        // Add event listeners to the existing buttons
        likeButton.addEventListener('click', handleLike);
        editButton.addEventListener('click', handleEdit);
    }

    function handleLike(e) {
        e.preventDefault();
        const postId = e.currentTarget.getAttribute('data-id').split('-')[1];
        const csrfToken = getCookie('csrftoken');
        const request = new Request(
            `/like/${postId}`,
            { headers: { 'X-CSRFToken': csrfToken } }
        );
    
        fetch(request, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({ id: postId }),
        }).then(() => {
            fetch(`/like/${postId}`)
                .then(response => response.json())
                .then(likes => {
                    e.currentTarget.querySelector('span').innerHTML = likes;
                });
        });
    }
    
    function handleEdit(e) {
        e.preventDefault();
        createEditForm(e.currentTarget.closest('.card'));
    }
    
    // Re-add the event listeners to all existing like and edit buttons
    document.querySelectorAll('.like-link').forEach(button => {
        button.removeEventListener('click', handleLike); // Ensure no duplicate listeners
        button.addEventListener('click', handleLike);
    });
    document.querySelectorAll('.edit-link').forEach(button => {
        button.removeEventListener('click', handleEdit); // Ensure no duplicate listeners
        button.addEventListener('click', handleEdit);
    });
    // Add click event listeners to each 'edit-link' button
    document.querySelectorAll('.edit-link').forEach(button => button.addEventListener('click', (e) => {
        e.preventDefault();
        createEditForm(button.closest('.card'));
    }));

    // Add click event listeners to each 'like-link' button
    document.querySelectorAll('.like-link').forEach(button => button.addEventListener('click', (e) => {
        e.preventDefault();
        // Get the post ID from the data attribute of the button
        const postId = button.getAttribute('data-id').split('-')[1];

        // Get the CSRF token from the cookie
        const csrfToken = getCookie('csrftoken');
        // Create a request object with the CSRF token in the header
        const request = new Request(
            `/like/${postId}`,
            { headers: { 'X-CSRFToken': csrfToken } }
        );

        // Send a POST request to the server to increment likes
        fetch(request, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                id: postId,
            }),
        }).then(() => {
            // Send a GET request to get the updated number of likes
            fetch(`/like/${postId}`)
                .then(response => response.json())
                .then(likes => {
                    // Update the number of likes displayed on the button
                    button.querySelector('span').innerHTML = likes;
                });
        });
    }));

    document.getElementById('toggleForm').addEventListener('click', function () {
        var form = document.getElementById('postForm');
        if (form.style.display === 'none') {
            form.style.display = 'block';
        } else {
            form.style.display = 'none';
        }
    });
}); 