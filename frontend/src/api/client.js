// src/api/client.js
// Centralized axios instance used across the frontend.
// Reasons for a single axios instance:
// - Configure baseURL in one place.
// - Add request/response interceptors (attach tokens, refresh logic).
// - Easier to mock in tests.

import axios from "axios";
import { API_BASE_URL } from "./config"; // Reads from Vite env (VITE_API_URL)

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor attaches the JWT from localStorage to outgoing requests.
// This means UI components don't need to manually add the Authorization header.
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwtToken");
    // Don't attach token to login/register requests (they don't need it)
    if (
      token &&
      !config.url.includes("/auth/login") &&
      !config.url.includes("/auth/register")
    ) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default client;
