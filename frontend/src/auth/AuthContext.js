import { createContext, useState } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));

  function login(jwt) {
    localStorage.setItem("token", jwt);
    setToken(jwt);
  }

  function register(jwt) {
    localStorage.setItem("token", jwt);
    setToken(jwt);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ token, login, logout, register}}>
      {children}
    </AuthContext.Provider>
  );
}

// Helper for axios to get token
export function getToken() {
  return localStorage.getItem("token");
}
