// src/api/auth.js
import client from "./client";

export const registerUser = (userData) => {
  // Matches UserInRegister schema
  return client.post("/auth/register", userData);
};

export const loginUser = (credentials) => {
  // Expects UserInLogin schema
  return client.post("/auth/login", credentials); // Returns UserWithToken {token: str}
};

// ... subscriptions functions (add, list, delete) follow the same pattern.
export const addSubscription = (subscriptionData) => {
  return client.post("/subscriptions", subscriptionData);
};

export const listSubscriptions = () => {
  return client.get("/subscriptions");
};

export const deleteSubscription = (subscriptionId) => {
  return client.delete(`/subscriptions/${subscriptionId}`);
};