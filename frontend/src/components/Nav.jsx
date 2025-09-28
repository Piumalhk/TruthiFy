import React from "react";
import logo from "../assets/logo.png";

export default function Nav() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    
      <div className="container">
        {/* Logo */}
        <a className="navbar-brand" href="/">
          <img
            src={logo}
            alt="TruthiFy Logo"
            className="logo"
            width="40"
            height="40"
          />
        </a>

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
              <a className="nav-link text-dark hover-primary px-3" href="/">
                Home
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link text-dark hover-primary px-3"
                href="/about"
              >
                About
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link text-dark hover-primary px-3"
                href="/services"
              >
                Services
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link text-dark hover-primary px-3"
                href="/history"
              >
                History
              </a>
            </li>
          </ul>
        </div>
        <button className="btn btn-primary px-4 rounded-pill ">Sign Up</button>
      </div>
    </nav>
  );
}
