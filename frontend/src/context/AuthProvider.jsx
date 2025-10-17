// src/context/AuthProvider.jsx
// This file contains the "provider" component for authentication state.
// React Context has two pieces:
//  1) The context object (created in AuthContext.js) which is like a key
//     used by consumers.
//  2) The provider component below that wraps part of the component tree
//     and supplies the actual values (user, login, logout).
//
// The provider persists the logged-in user in localStorage so a page refresh
// doesn't immediately log the user out (simple UX improvement for demos).

import React, { useState, useEffect } from "react";
import { loginUser, registerUser } from "../api/auth";
import AuthContext from "./AuthContext";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
      localStorage.removeItem("jwtToken");
    }
  }, [user]);

  const login = async (credentials) => {
    const resp = await loginUser(credentials);
    // API returns { token } and the protected /protected endpoint returns user payload
    const token = resp.data.token;
    localStorage.setItem("jwtToken", token);
    // Optionally fetch user profile from /protected or decode token
    setUser({ email: credentials.email });
    return resp;
  };

  const register = async (userData) => {
    const resp = await registerUser(userData);
    return resp;
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
