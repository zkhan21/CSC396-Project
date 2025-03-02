import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../style-sheets/Login.css";
import backgroundImage from "../assets/smartExpenseTrackerLogo.jpeg"; // import project name/logo image

const Login = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Retrieve user data (mock database in localStorage)
  const users = JSON.parse(localStorage.getItem("users")) || [];

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Both email and password fields are required.");
      return;
    }

    if (isSignUp) {
      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }

      if (users.find((user) => user.email === email)) {
        setError("This email is already registered. Please log in.");
        return;
      }

      const newUser = { email, password };
      users.push(newUser);
      localStorage.setItem("users", JSON.stringify(users));

      setError("");
      setIsSignUp(false);
      alert("Account created successfully! Please log in.");
    } else {
      const user = users.find((user) => user.email === email && user.password === password);
      if (user) {
        console.log("Login successful!");
        setError("");
        navigate("/dashboard");
      } else {
        setError("Invalid email or password.");
      }
    }
  };

  return (
    <div style={styles.background}>
      <img src={backgroundImage} alt="Logo" style={styles.logo} />
      <div style={styles.container}>
        <h2>{isSignUp ? "Create an Account" : "Login"}</h2>
        {error && <p style={styles.error}>{error}</p>}
        <form onSubmit={handleSubmit} style={styles.form}>
          <div>
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required style={styles.input} />
          </div>
          <div>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required style={styles.input} />
          </div>
          {isSignUp && (
            <div>
              <label>Confirm Password:</label>
              <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required style={styles.input} />
            </div>
          )}
          <button type="submit" style={styles.button}>{isSignUp ? "Sign Up" : "Login"}</button>
        </form>
        <p onClick={() => setIsSignUp(!isSignUp)} style={styles.toggleText}>
          {isSignUp ? "Already have an account? Log in" : "Don't have an account? Sign up"}
        </p>
      </div>
    </div>
  );
};

// ✅ Adjusted Styling to Fix Cut-off Issue
const styles = {
  background: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center", // Center content vertically
    alignItems: "center",
    backgroundColor: "#121212", // Darker background for consistency
    transition: "all 0.5s ease-in-out",
    padding: "5vh 10px", // Added horizontal padding to prevent cut-off
  },
  logo: {
    width: "220px", // Slightly increased logo size
    marginBottom: "20px", // Space between logo and login box
  },
  container: {
    width: "90%", // Responsive width to prevent cutting
    maxWidth: "400px", // Ensures it doesn't get too wide
    padding: "30px",
    backgroundColor: "rgba(255, 255, 255, 0.9)", // More solid background for contrast
    borderRadius: "12px",
    textAlign: "center",
    boxShadow: "0px 6px 15px rgba(0, 0, 0, 0.3)", // Stronger shadow for depth
  },
  form: { display: "flex", flexDirection: "column", gap: "15px" },
  input: { width: "100%", padding: "10px", marginTop: "5px", borderRadius: "5px", border: "1px solid #ccc" },
  button: { padding: "12px", backgroundColor: "#007bff", color: "white", border: "none", cursor: "pointer", borderRadius: "5px" },
  error: { color: "red" },
  toggleText: { marginTop: "15px", color: "#007bff", cursor: "pointer" },
};

export default Login;