import React from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Nav() {
  const navigate = useNavigate();
  const location = useLocation();

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
    <nav className="navbar navbar-expand-lg navbar-dark shadow-sm sticky-top">
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
          </ul>
        </div>
        <a href="/signup">
          <button className="btn btn-primary px-4 rounded-pill ">
            Sign Up
          </button>
        </a>
      </div>
    </nav>
  );
}
