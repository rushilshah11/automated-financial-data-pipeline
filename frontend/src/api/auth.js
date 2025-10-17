// src/api/auth.js
// Lightweight API wrappers for the backend endpoints used by the UI.
// Keep network code in one place so UI components stay small and focused.

import client from "./client";

// Register a new user. `userData` should include first_name, last_name, email, password
export const registerUser = (userData) => {
  return client.post("/auth/register", userData);
};

// Login: sends email/password and expects a { token: '...' } response
export const loginUser = (credentials) => {
  return client.post("/auth/login", credentials);
};

// Subscriptions: CRUD helpers used by the Dashboard page
export const addSubscription = (subscriptionData) => {
  return client.post("/subscriptions", subscriptionData);
};

export const listSubscriptions = () => {
  return client.get("/subscriptions");
};

export const deleteSubscription = (subscriptionId) => {
  return client.delete(`/subscriptions/${subscriptionId}`);
};
