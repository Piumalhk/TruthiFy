import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
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

    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Please fill in both username and password");
      return;
    }

    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500));
      alert("Account created successfully!");
      setFormData({ username: "", password: "" });
    } catch (error) {
      setError("Failed to create account. Please try again.");
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

                {/* Back to Home Button */}
              

                {/* Error Message */}
                {error && (
                  <div className="alert alert-danger text-center" role="alert">
                    {error}
                  </div>
                )}

                {/* Signup Form */}
                <form onSubmit={handleSubmit}>
                  {/* Username */}
                  <div className="mb-4">
                  
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
                      
                    />
                  </div>

                     <div className="mb-3">
                
                    <input
                      type="password"
                      className="form-control form-control-lg fs-6"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      placeholder="Confirm your password"
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
                        Creating Account...
                      </>
                    ) : (
                      "Create Account"
                    )}
                  </button>

                  {/* Login Link */}
                  
                  <div className="text-center ">
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
