import React from "react";
import { Link } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="site-header">
      <div className="site-brand">AutoFinance</div>
      <nav>
        {user ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <button className="link-button" onClick={logout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}
