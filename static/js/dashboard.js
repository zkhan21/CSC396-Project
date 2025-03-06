document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded on the page!");

    function setupNavigationButtons() {
        console.log("Setting up navigation buttons...");

        document.querySelectorAll(".nav-btn").forEach(button => {
            console.log("Attaching click listener to:", button.innerText);
            button.addEventListener("click", function (event) {
                event.preventDefault();
                console.log("Button clicked:", this.innerText);
                window.location.href = this.getAttribute("href");
            });
        });
    }

    function reattachEventListeners() {
        setTimeout(() => {
            console.log("Reattaching event listeners after page update...");
            setupNavigationButtons();
        }, 500);  // Small delay to ensure elements are loaded
    }

    setupNavigationButtons();
    
    // Handle login form submission
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
                console.log("Login successful, redirecting to dashboard...");
                window.location.href = response.url;
                reattachEventListeners();  // Ensure buttons work after login
            } else {
                alert("Invalid credentials");
            }
        });
    }

    // Ensure buttons are functional even after navigating
    window.onload = function () {
        console.log("Window fully loaded, ensuring event listeners are active...");
        reattachEventListeners();
    };
});
