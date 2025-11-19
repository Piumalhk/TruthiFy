import React, { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();
const API_BASE_URL = "http://localhost:8000/api/v1";

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // -------------------------------------------------
  // ✅ Check authentication on first load
  // -------------------------------------------------
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
          } else {
            localStorage.removeItem("access_token");
          }
        } catch (error) {
          console.error("Auth check failed:", error);
          localStorage.removeItem("access_token");
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  // -------------------------------------------------
  // ✅ Fetch user data after login
  // -------------------------------------------------
  const fetchUserData = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        setUser(null);
        localStorage.removeItem("access_token");
      }
    } catch (error) {
      console.error("Failed to fetch user data:", error);
    }
  };

  // -------------------------------------------------
  // ✅ Login Handler
  // -------------------------------------------------
  const login = async (token, tokenType) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("token_type", tokenType);
    await fetchUserData();
  };

  // -------------------------------------------------
  // ✅ Register New User  (Corrected)
  // -------------------------------------------------
  const register = async (userData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData), // FIXED
      });

      const data = await response.json();

      return response.ok
        ? { success: true, message: data.message || "Account created" }
        : { success: false, message: data.detail || "Registration failed" };
    } catch (error) {
      console.error("Registration error:", error);
      return { success: false, message: "Network error" };
    }
  };

  // -------------------------------------------------
  // ✅ Logout
  // -------------------------------------------------
  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  // -------------------------------------------------
  // Helpers
  // -------------------------------------------------
  const isAuthenticated = () =>
    !!localStorage.getItem("access_token") && !!user;

  const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  // -------------------------------------------------
  const value = {
    user,
    login,
    register,
    logout,
    isAuthenticated,
    getAuthHeaders,
    loading,
    fetchUserData,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
