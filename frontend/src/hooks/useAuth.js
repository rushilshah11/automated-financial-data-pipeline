// src/hooks/useAuth.js
// Small helper hook that components use to access authentication state.
// Instead of importing useContext(AuthContext) everywhere, calling useAuth()
// is cleaner and lets you add cross-cutting logic here later (like redirects).

import { useContext } from "react";
import AuthContext from "../context/AuthContext";

export default function useAuth() {
  return useContext(AuthContext);
}
