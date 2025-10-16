// frontend/src/api/config.js

// Accesses the variable provided during the React build process
export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";
