import getCookie from "./util.js";

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', function() {
        const postId = this.dataset.post;
        handleLikeButton(postId)
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.post_id;
            handleEditButton(postId)
        });
    });
});

function savePost(postId) {
    let editedContent = document.getElementById('edit-content-' + postId).value;
    fetch(`/edit_post/${postId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Ensure you have a function to get the CSRF token
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `editPost=${encodeURIComponent(editedContent)}`
    })
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            let postDiv = document.getElementById('post-' + postId);
            // Assume `data.like_count` is the updated like count sent back from the server
            const created_at = `<p class="card-text"><small class="text-muted">Posted on: ${ data.created_at }</small></p>`
            const editButton = `<button class="edit-button btn btn-secondary mb-2" data-post_id="${postId}">Edit</button>`
            const likeButton = `<button id="like-button-${postId}" class="like-button btn btn-primary mb-2" data-post="${postId}" type="button">${data.is_liked ? "Unlike" : "Like"}</button>`;
            const likeCount = `<p id="like-count-${postId}">Likes: ${ data.like_count }</p>`;

            postDiv.innerHTML = `<p class="card-text post-content">${editedContent}</p>
                                ${created_at}
                                ${editButton}
                                ${likeButton}
                                ${likeCount}`;

            // Call attachEventListenersToButtons to re-attach event listeners
            attachEventListenersToButtons();
           
        } else {
            // Handle errors, such as validation errors or authentication issues
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}


function attachEventListenersToButtons() {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.post_id;
            handleEditButton(postId)
        });
    });

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.post;
            handleLikeButton(postId)
        });
    });
}


function handleLikeButton(postId) {
    fetch(`/like/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            'postId': postId
        }),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Ensure you have a function to get CSRF token or adjust accordingly
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#like-button-${postId}`).innerHTML = result.liked ? "Unlike" : "Like"
        
        // Update the like count on the page
        document.querySelector(`#like-count-${postId}`).innerHTML = `Likes: ${result.like_count}`;
    });
}


function handleEditButton(postId) {
    let postDiv = document.getElementById('post-' + postId);
    let content = postDiv.querySelector('.post-content').innerText;

        // Setup the editable textarea and Save button
    const textarea = `<textarea id="edit-content-${postId}" class="form-control mb-2">${content}</textarea>`;
    const saveButton = `<button class="save-edit btn btn-success" data-post-id="${postId}">Save</button>`;
    
    postDiv.innerHTML = textarea + saveButton;

    // Add click listener for the newly added Save button
    document.querySelector(`.save-edit[data-post-id="${postId}"]`).addEventListener('click', function() {
        savePost(postId);
    });
}