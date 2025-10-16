// src/context/AuthContext.js

import { createContext } from "react";

// The shape of the context value: { user, login, register, logout }
const AuthContext = createContext(null);

export default AuthContext;
// Note: The actual provider component is in AuthProvider.jsx