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
