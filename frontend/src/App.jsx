// src/App.jsx - application root and routing
// This file defines the high-level routes and wraps the app with the
// AuthProvider. If you're new to React, think of this as the app's
// "index of pages" where URLs map to components.

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthProvider";
import useAuth from "./hooks/useAuth";
import Header from "./components/Header";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import "./index.css";
// import { use } from "react";

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route
        path="/"
        element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />}
      />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Header />
        <main className="container">
          <AppRoutes />
        </main>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
