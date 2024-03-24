import getCookie from "./util.js";

document.addEventListener('DOMContentLoaded', function() {
    const followToggleButton = document.querySelector('#follow-toggle-button');
    if (followToggleButton) {
        followToggleButton.addEventListener("click", () => {
            console.log(123);
            const username = followToggleButton.dataset.username;
            fetch(`/toggle_follow/${username}`, {
                method: 'POST',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then(response => response.json())
            .then(result => {
                if (result.status === "success") {
                    followToggleButton.innerHTML = result.action === "followed" ? `<i class="bi bi-person-dash-fill"></i> Unfollow` : `<i class="bi bi-person-plus-fill"></i> Follow`;
                    document.querySelector('#followers-count').innerHTML = `${result.followers_count}`;

                    followToggleButton.classList.remove("btn-success", "btn-danger");
                    followToggleButton.classList.add(result.action === "followed" ? "btn-danger" : "btn-success");
                }
            });
        });
    }
});



