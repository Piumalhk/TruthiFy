import React, { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

const API_BASE_URL = "http://localhost:8000/api/auth/register";

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

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
          } else {
            // Token is invalid, remove it
            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");
          }
        } catch (error) {
          console.error("Auth check failed:", error);
          localStorage.removeItem("access_token");
          localStorage.removeItem("token_type");
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = (token, tokenType) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("token_type", tokenType);

    // Fetch user data after login
    fetchUserData();
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
    setUser(null);
  };

  const fetchUserData = async () => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }
    }
  };

  const isAuthenticated = () => {
    return !!localStorage.getItem("access_token") && !!user;
  };

  const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated,
    getAuthHeaders,
    loading,
    fetchUserData,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
