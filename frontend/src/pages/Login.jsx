// src/pages/Login.jsx
// Small login form. It uses the `login` function from AuthProvider (via
// useAuth) which stores the JWT in localStorage. After login the page
// navigates to /dashboard. Error responses from the API are displayed
// to the user for quick feedback.

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const { login } = useAuth();
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await login({ email, password });
      // on success navigate to dashboard
      nav("/dashboard");
    } catch (err) {
      // Show a friendly error message when login fails
      setError(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="card">
      <h2>Login</h2>
      {error && <div className="alert">{error}</div>}
      <form onSubmit={submit}>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="btn" type="submit">
          Login
        </button>
      </form>
    </div>
  );
}
