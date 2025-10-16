// src/api/client.js
import axios from "axios";
import { API_BASE_URL } from "./config"; // Assume you set this up

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor: Attach JWT token to all outgoing requests
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwtToken"); // Get token from storage
    if (
      token &&
      config.url !== "/auth/login" &&
      config.url !== "/auth/register"
    ) {
      // Attach token ONLY if it's a protected route
      config.headers.Authorization = `Bearer ${token}`; //
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default client;
