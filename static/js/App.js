import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./style.css"; // Optional: add CSS for styling

const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        const formData = new FormData();
        formData.append("email", email);
        formData.append("password", password);

        const response = await fetch("/login", {
            method: "POST",
            body: formData,
        });

        if (response.redirected) {
            console.log("✅ Login successful, redirecting to dashboard...");
            navigate("/dashboard");
        } else {
            setError("❌ Invalid credentials");
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleLogin}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

const Dashboard = () => {
    const navigate = useNavigate();

    return (
        <div className="dashboard">
            <h2>Welcome to the Dashboard</h2>
            <button className="nav-btn" onClick={() => navigate("/profile")}>Go to Profile</button>
            <button className="nav-btn" onClick={() => navigate("/settings")}>Go to Settings</button>
            <button onClick={() => navigate("/")}>Logout</button>
        </div>
    );
};

const Profile = () => <h2>Profile Page</h2>;
const Settings = () => <h2>Settings Page</h2>;

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/settings" element={<Settings />} />
            </Routes>
        </Router>
    );
};

export default App;
