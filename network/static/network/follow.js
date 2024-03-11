import getCookie from "./util.js";

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#follow-toggle-button').addEventListener("click",  () => {
        const username = document.querySelector('#follow-toggle-button').dataset.username;
        fetch(`/toggle_follow/${username}`, {
            method: 'POST',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // CSRF token as before
            },
        })
        .then(response => response.json())
        .then(result => {
            // Update the button and followers count based on the result
            if (result.status === "success") {
                document.querySelector('#follow-toggle-button').innerHTML = result.action === "followed" ? "Unfollow" : "Follow";
                document.querySelector('#followers-count').innerHTML = `${result.followers_count}`;
            }
        });
    });
});


