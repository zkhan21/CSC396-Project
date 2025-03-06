document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Buttons.js Loaded - Ensuring buttons work!");

    function setupNavigationButtons() {
        document.querySelectorAll(".nav-btn, .logout-btn").forEach(button => {
            button.addEventListener("click", function (event) {
                event.preventDefault();
                console.log("🚀 Navigating to:", this.getAttribute("href"));
                window.location.href = this.getAttribute("href");
            });
        });
    }

    setupNavigationButtons();

    // Ensure login submission triggers a full page refresh
    const loginForm = document.querySelector("form");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const formData = new FormData(loginForm);
            const response = await fetch("/login", {
                method: "POST",
                body: formData
            });

            if (response.redirected) {
                console.log("✅ Login successful, forcing full reload...");
                window.location.href = response.url;
                setTimeout(() => location.reload(), 500);  // Force full refresh
            } else {
                alert("Invalid credentials");
            }
        });
    }

    // Debugging: Log clicks to check if they're intercepted
    document.addEventListener("click", function (event) {
        console.log("🖱 Clicked on:", event.target);
    });
});
