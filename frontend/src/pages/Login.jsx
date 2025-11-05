import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const API_BASE_URL = "http://localhost:8000/api/v1";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setError(""); // Clear error when user types
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Please fill in both username and password");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        // Use the auth context to handle login
        login(data.access_token, data.token_type);

        setSuccess("Login successful! Redirecting...");
        setFormData({ username: "", password: "" });

        // Redirect to home page after successful login
        setTimeout(() => {
          navigate("/analyze");
        }, 1500);
      } else {
        setError(
          data.detail || "Invalid username or password. Please try again."
        );
      }
    } catch (error) {
      console.error("Login error:", error);
      setError("Network error. Please check your connection and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="login-page min-vh-100 d-flex align-items-center justify-content-center"
      style={{
        background: "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
      }}
    >
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-4">
            <div className="card shadow border-0">
              <div className="card-body p-5">
                {/* Header */}
                <div className="text-center mb-4">
                  <h4 className="fw-bold mb-3">Welcome Back</h4>
                </div>

                {/* Error Message */}
                {error && (
                  <div className="alert alert-danger text-center" role="alert">
                    {error}
                  </div>
                )}

                {/* Success Message */}
                {success && (
                  <div className="alert alert-success text-center" role="alert">
                    {success}
                  </div>
                )}

                {/* Login Form */}
                <form onSubmit={handleSubmit}>
                  {/* Username */}
                  <div className="mb-3">
                    <input
                      type="text"
                      className="form-control form-control-lg fs-6"
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleInputChange}
                      placeholder="Enter your username"
                      required
                    />
                  </div>

                  {/* Password */}
                  <div className="mb-4">
                    <input
                      type="password"
                      className="form-control form-control-lg fs-6"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      placeholder="Enter your password"
                      required
                    />
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="btn btn-primary btn-lg w-100 mb-3"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <span
                          className="spinner-border spinner-border-sm me-2"
                          role="status"
                        ></span>
                        Signing In...
                      </>
                    ) : (
                      "Sign In"
                    )}
                  </button>

                  {/* Signup Link */}
                  <div className="text-center fs-6">
                    <p className="text-muted mb-0">
                      Don't have an account?
                      <Link
                        to="/signup"
                        className="text-primary text-decoration-none fw-semibold ms-1"
                      >
                        Create one here
                      </Link>
                    </p>
                  </div>
                  <div className="text-center ">
                    <p className="text-muted mb-0 fs-6">
                      <Link
                        to="/"
                        className="text-primary text-decoration-none ms-1 "
                      >
                        Back to Home
                      </Link>
                    </p>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
