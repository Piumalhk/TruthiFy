// API utility functions for making authenticated requests

const API_BASE_URL = "http://localhost:8000/api/v1";

// Get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

// Generic API request function
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: getAuthHeaders(),
    ...options,
  };

  try {
    const response = await fetch(url, config);

    // Handle 401 (Unauthorized) by redirecting to login
    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("token_type");
      window.location.href = "/login";
      return null;
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error(`API request failed for ${endpoint}:`, error);
    throw error;
  }
};

// Auth API functions
export const authAPI = {
  register: async (userData) => {
    return apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify(userData),
    });
  },

  login: async (credentials) => {
    return apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify(credentials),
    });
  },

  getProfile: async () => {
    return apiRequest("/auth/profile");
  },

  getCurrentUser: async () => {
    return apiRequest("/auth/me");
  },

  logout: async () => {
    return apiRequest("/auth/logout", {
      method: "POST",
    });
  },
};

// News analysis API functions
export const newsAPI = {
 analyzeNews: async (text) => {
  return apiRequest("/analyze", {
    method: "POST",
    body: JSON.stringify({ content: text }), // 👈 change key name
  });

  },



  getHistory: async (limit = 50, skip = 0) => {
    return apiRequest(`/history?limit=${limit}&skip=${skip}`);
  },

  deleteAnalysis: async (analysisId) => {
    return apiRequest(`/history/${analysisId}`, {
      method: "DELETE",
    });
  },

  clearHistory: async () => {
    return apiRequest("/history/clear", {
      method: "DELETE",
    });
  },

  getStats: async () => {
    return apiRequest("/history/stats");
  },
};

export default {
  authAPI,
  newsAPI,
};
