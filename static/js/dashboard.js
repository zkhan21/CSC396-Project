import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Navigation = () => {
    const navigate = useNavigate();
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        console.log("🚀 React Component Loaded!");

        // Setup navigation buttons dynamically
        const setupNavigationButtons = () => {
            console.log("🔹 Setting up navigation buttons...");

            document.querySelectorAll(".nav-btn").forEach(button => {
                console.log("🔘 Attaching click listener to:", button.innerText);
                button.addEventListener("click", (event) => {
                    event.preventDefault();
                    console.log("✅ Button clicked:", button.innerText);

                    const targetHref = button.getAttribute("href");
                    if (targetHref) {
                        console.log("🔗 Redirecting to:", targetHref);
                        navigate(targetHref);
                    } else {
                        console.error("❌ Button has no href attribute:", button.innerText);
                    }
                });
            });
        };

        setupNavigationButtons();

        // Observer for dynamically loaded buttons
        const observer = new MutationObserver(() => {
            console.log("🔄 DOM updated, reattaching event listeners...");
            setupNavigationButtons();
        });

        observer.observe(document.body, { childList: true, subtree: true });

        return () => observer.disconnect();
    }, [navigate]);

    const handleLogin = async (event) => {
        event.preventDefault();
        console.log("🔑 Attempting login...");

        const formData = new FormData(event.target);
        const response = await fetch("/login", {
            method: "POST",
            body: formData
        });

        if (response.redirected) {
            console.log("✅ Login successful, redirecting to dashboard...");
            setIsAuthenticated(true);
            navigate("/dashboard");
        } else {
            alert("❌ Invalid credentials");
        }
    };

    return (
        <div>
            {!isAuthenticated ? (
                <form onSubmit={handleLogin}>
                    <label>Email:</label>
                    <input type="email" name="email" required />
                    <label>Password:</label>
                    <input type="password" name="password" required />
                    <button type="submit">Login</button>
                </form>
            ) : (
                <div>
                    <h2>Welcome to the Dashboard</h2>
                    <button className="nav-btn" href="/profile">Go to Profile</button>
                    <button className="nav-btn" href="/settings">Go to Settings</button>
                    <button onClick={() => setIsAuthenticated(false)}>Logout</button>
                </div>
            )}
        </div>
    );
};

export default Navigation;
