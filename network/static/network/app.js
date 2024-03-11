import getCookie from "./util.js";

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', function() {
        const postId = this.dataset.post;
        fetch(`/like/${postId}`, {
            method: 'POST',
            body: JSON.stringify({
                like: true
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
    });
  });
});

