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
            if (result.liked) {
                document.querySelector(`#like-button-${postId}`).innerHTML = "Unlike"
            } else {
                document.querySelector(`#like-button-${postId}`).innerHTML = "Like"
                
            }
            // Update the like count on the page

            document.querySelector(`#like-count-${postId}`).innerHTML = `Likes: ${result.like_count}`;
        });
    });
  });
});

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