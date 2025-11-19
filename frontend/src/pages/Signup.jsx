import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [formData, setFormData] = useState({
    full_name: "",
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
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
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // ---- Validation ----
    if (
      !formData.full_name.trim() ||
      !formData.username.trim() ||
      !formData.email.trim() ||
      !formData.password.trim() ||
      !formData.confirmPassword.trim()
    ) {
      setError("Please fill in all fields");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters long");
      return;
    }

    if (formData.password.length > 72) {
      setError("Password cannot be longer than 72 characters");
      return;
    }

    setIsLoading(true);

    try {
      // Send data ONLY what backend expects
      const registrationData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
      };

      await register(registrationData);

      setSuccess("Account created successfully! Redirecting to login...");

      setFormData({
        full_name: "",
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
      });

      setTimeout(() => navigate("/login"), 1500);
    } catch (error) {
      console.error("Signup error:", error);
      setError("Registration failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="signup-page min-vh-100 d-flex align-items-center justify-content-center"
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
                  <h4 className="fw-bold mb-3">Create Account</h4>
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

                {/* Signup Form */}
                <form onSubmit={handleSubmit}>
                  {/* Full Name */}
                  <div className="mb-3">
                    <input
                      type="text"
                      className="form-control form-control-lg fs-6"
                      id="full_name"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleInputChange}
                      placeholder="Enter your full name"
                      required
                    />
                  </div>

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

                  {/* Email */}
                  <div className="mb-3">
                    <input
                      type="email"
                      className="form-control form-control-lg fs-6"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="Enter your email"
                      required
                    />
                  </div>

                  {/* Password */}
                  <div className="mb-3">
                    <input
                      type="password"
                      className="form-control form-control-lg fs-6"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      placeholder="Enter your password"
                      required
                      maxLength={72}
                    />
                  </div>

                  {/* Confirm Password */}
                  <div className="mb-3">
                    <input
                      type="password"
                      className="form-control form-control-lg fs-6"
                      id="confirmPassword"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleInputChange}
                      placeholder="Confirm your password"
                      required
                      maxLength={72}
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
                        Creating Account...
                      </>
                    ) : (
                      "Create Account"
                    )}
                  </button>

                  {/* Login Link */}
                  <div className="text-center">
                    <p className="text-muted mb-0 fs-6">
                      Already have an account?
                      <Link
                        to="/login"
                        className="text-primary text-decoration-none fw-semibold ms-1"
                      >
                        Login
                      </Link>
                    </p>
                  </div>

                  {/* Back to Home */}
                  <div className="text-center mt-2">
                    <p className="text-muted mb-0 fs-6">
                      <Link
                        to="/"
                        className="text-primary text-decoration-none ms-1"
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
