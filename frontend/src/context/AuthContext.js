// src/context/AuthContext.js
// Simple file that exports the context object used by the app.
// We separate the context object from the provider component to keep the
// provider focused on logic and make the context easy to import in hooks.

import { createContext } from "react";

// The shape of the context value: { user, login, register, logout }
const AuthContext = createContext(null);

export default AuthContext;
// Note: The actual provider component is in AuthProvider.jsx
