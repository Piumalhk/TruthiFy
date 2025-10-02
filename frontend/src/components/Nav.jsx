import React from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";

export default function Nav() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, isAuthenticated } = useAuth();

  const handleAboutClick = (e) => {
    e.preventDefault();

    // If we're already on the home page, just scroll to the about section
    if (location.pathname === "/") {
      const aboutSection = document.getElementById("about-section");
      if (aboutSection) {
        aboutSection.scrollIntoView({ behavior: "smooth" });
      }
    } else {
      // Navigate to home page first, then scroll to about section
      navigate("/");
      setTimeout(() => {
        const aboutSection = document.getElementById("about-section");
        if (aboutSection) {
          aboutSection.scrollIntoView({ behavior: "smooth" });
        }
      }, 100);
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark shadow-sm ">
      <div className="container">
        {" "}
        {/* Logo */}
        <Link className="navbar-brand" to="/">
          <img
            src={logo}
            alt="TruthiFy Logo"
            className="logo"
            width="40"
            height="40"
          />
        </Link>
        {/* Mobile toggle button */}
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        {/* Navigation links */}
        <div
          className="collapse navbar-collapse justify-content-center"
          id="navbarNav"
        >
          <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link hover-primary px-3" href="/">
                Home
              </a>
            </li>{" "}
            <li className="nav-item">
              <a
                className="nav-link hover-primary px-3"
                href="#about-section"
                onClick={handleAboutClick}
              >
                About
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link  hover-primary px-3" href="/services">
                Services
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link  hover-primary px-3" href="/history">
                History
              </a>
            </li>
          </ul>{" "}
        </div>
        {/* Authentication buttons */}
        <div className="d-flex align-items-center gap-2">
          {isAuthenticated() ? (
            <div className="dropdown">
              <button
                className="btn btn-outline-light dropdown-toggle px-3 rounded-pill"
                type="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                {user?.username || "User"}
              </button>
              <ul className="dropdown-menu dropdown-menu-end">
                <li>
                  <Link className="dropdown-item" to="/history">
                    <i className="bi bi-clock-history me-2"></i>
                    History
                  </Link>
                </li>
                <li>
                  <hr className="dropdown-divider" />
                </li>
                <li>
                  <button
                    className="dropdown-item text-danger"
                    onClick={logout}
                  >
                    <i className="bi bi-box-arrow-right me-2"></i>
                    Logout
                  </button>
                </li>
              </ul>
            </div>
          ) : (
            <>
              
              <Link to="/signup">
                <button className="btn btn-primary px-4 rounded-pill">
                  Sign Up
                </button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
