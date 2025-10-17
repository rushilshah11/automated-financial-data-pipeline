// src/pages/Register.jsx
// Simple registration form. The backend expects fields matching the
// UserInRegister schema: first_name, last_name, email, password.
// After successful registration this sample app navigates to the login page.

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function Register() {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const { register } = useAuth();
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await register({ first_name, last_name, email, password });
      nav("/login");
    } catch (err) {
      setError(err?.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="card">
      <h2>Register</h2>
      {error && <div className="alert">{error}</div>}
      <form onSubmit={submit}>
        <label>First name</label>
        <input
          value={first_name}
          onChange={(e) => setFirstName(e.target.value)}
        />
        <label>Last name</label>
        <input
          value={last_name}
          onChange={(e) => setLastName(e.target.value)}
        />
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="btn" type="submit">
          Create account
        </button>
      </form>
    </div>
  );
}
