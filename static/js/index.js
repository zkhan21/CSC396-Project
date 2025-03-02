document.addEventListener("DOMContentLoaded", function () {
    console.log("Smart Expense Tracker Loaded!");

    const loginForm = document.querySelector("form");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const formData = new FormData(loginForm);
            const response = await fetch("/login", {
                method: "POST",
                body: formData
            });

            const text = await response.text();

            if (response.redirected) {
                window.location.href = response.url;  // Redirect user
            } else {
                alert("Invalid credentials");
            }
        });
    }
});
