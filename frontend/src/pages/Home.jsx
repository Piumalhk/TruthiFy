import React from "react";
import Nav from "../components/Nav";

export default function Home() {
  return (
    <div>
      <Nav />

      {/* Hero Section with Gradient Background */}
      <section className="hero-section d-flex align-items-center justify-content-center text-center text-white">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-lg-10">
              <h1 className="display-1 fw-bold mb-4 hero-title">
                Detect Fake News with{" "}
                <span className="text-primary">AI Precision</span>
              </h1>
              <p className="lead fs-4 mb-5 hero-subtitle">
                In today's digital age, misinformation spreads faster than
                wildfire. TruthiFy harnesses the power of advanced artificial
                intelligence and machine learning algorithms to help you
                identify fake news, verify information authenticity, and stay
                informed with credible sources. Join millions of users who trust
                our cutting-edge technology to navigate the complex landscape of
                digital information.
              </p>
              <div className="d-flex justify-content-center gap-3 flex-wrap">
                <a
                  href="/login"
                  className="btn btn-light btn-lg px-5 py-3 rounded-pill fw-semibold get-started-btn"
                >
                  Get Started
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about-section" className="about-section py-5">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-lg-10">
              <div className="text-center mb-5">
                <h2 className="display-4 fw-bold mb-4">About TruthiFy</h2>

                <p className="text-muted fs-5 mt-4">
                  TruthiFy was born from the urgent need to combat the growing
                  epidemic of misinformation that threatens democratic
                  discourse, public health decisions, and social cohesion. Our
                  team of data scientists, journalists, and technology experts
                  has developed a sophisticated platform that combines natural
                  language processing, sentiment analysis, source credibility
                  assessment, and pattern recognition to provide you with
                  reliable truth detection tools.
                </p>
              </div>

              <div className="row g-4">
                <div className="col-md-4">
                  <div className="card h-100 border-0 shadow-sm feature-card">
                    <div className="card-body text-center p-4">
                      <div className="mb-3">
                        <i
                          className="fas fa-brain text-primary"
                          style={{ fontSize: "3rem" }}
                        ></i>
                      </div>
                      <h5 className="card-title fw-bold">
                        AI-Powered Detection
                      </h5>
                      <p className="card-text text-muted">
                        Our advanced neural networks analyze linguistic
                        patterns, cross-reference multiple sources, and evaluate
                        content credibility.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="col-md-4">
                  <div className="card h-100 border-0 shadow-sm feature-card">
                    <div className="card-body text-center p-4">
                      <div className="mb-3">
                        <i
                          className="fas fa-shield-alt text-success"
                          style={{ fontSize: "3rem" }}
                        ></i>
                      </div>
                      <h5 className="card-title fw-bold">Real-time Analysis</h5>
                      <p className="card-text text-muted">
                        Get instantaneous results on news articles, social media
                        posts, press releases, and other digital content.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="col-md-4">
                  <div className="card h-100 border-0 shadow-sm feature-card">
                    <div className="card-body text-center p-4">
                      <div className="mb-3">
                        <i
                          className="fas fa-users text-info"
                          style={{ fontSize: "3rem" }}
                        ></i>
                      </div>
                      <h5 className="card-title fw-bold">Community Driven</h5>
                      <p className="card-text text-muted">
                        Join our growing community of educators, and concerned
                        citizens working together to create a digital
                        environment.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer bg-dark text-white py-5">
        <div className="container h-auto">
          <div className="row">
            <div className="col-lg-4 mb-4">
              <h5 className="fw-bold mb-3">TruthiFy</h5>
              <p className="text-light w-55">
                We empower people and communities with AI tools to combat
                misinformation and build a more informed society.
              </p>
              <div className="social-links">
                <a href="#" className="text-white me-3">
                  <i className="fab fa-facebook-f"></i>
                </a>
                <a href="#" className="text-white me-3">
                  <i className="fab fa-twitter"></i>
                </a>
                <a href="#" className="text-white me-3">
                  <i className="fab fa-linkedin-in"></i>
                </a>
                <a href="#" className="text-white">
                  <i className="fab fa-instagram"></i>
                </a>
              </div>
            </div>

            <div className="col-lg-2 col-md-6 mb-4">
              <h6 className="fw-bold mb-3">Quick Links</h6>
              <ul className="list-unstyled">
                <li>
                  <a href="/" className="text-light text-decoration-none">
                    Home
                  </a>
                </li>
                <li>
                  <a href="/about" className="text-light text-decoration-none">
                    About
                  </a>
                </li>
                <li>
                  <a
                    href="/services"
                    className="text-light text-decoration-none"
                  >
                    Services
                  </a>
                </li>
                <li>
                  <a
                    href="/history"
                    className="text-light text-decoration-none"
                  >
                    History
                  </a>
                </li>
              </ul>
            </div>

            <div className="col-lg-2 col-md-6 mb-4">
              <h6 className="fw-bold mb-3">Support</h6>
              <ul className="list-unstyled">
                <li>
                  <a href="#" className="text-light text-decoration-none">
                    Contact Us
                  </a>
                </li>
                <li>
                  <a href="#" className="text-light text-decoration-none">
                    FAQ
                  </a>
                </li>
                <li>
                  <a href="#" className="text-light text-decoration-none">
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="text-light text-decoration-none">
                    Terms of Service
                  </a>
                </li>
              </ul>
            </div>

            <div className="col-lg-4 mb-4">
              <h6 className="fw-bold mb-3">Stay Updated</h6>
              <p className="text-light">
                Subscribe to our newsletter for the latest updates on fake news
                detection.
              </p>
              <div className="input-group">
                <input
                  type="email"
                  className="form-control"
                  placeholder="Enter your email address"
                />
                <button className="btn btn-primary" type="button">
                  Subscribe
                </button>
              </div>
            </div>
          </div>

          <hr className="my-4 border-secondary" />

          <div className="row align-items-center">
            <div className="col-md-6">
              <p className="mb-0 text-light">
                &copy; 2025 TruthiFy. All rights reserved. Protecting truth in
                the digital age.
              </p>
            </div>
            <div className="col-md-6 text-md-end">
              <p className="mb-0 text-light">
                <a href="#" className="text-light text-decoration-none">
                  Terms of Service
                </a>{" "}
                |
                <a href="#" className="text-light text-decoration-none ms-2">
                  Privacy Policy
                </a>{" "}
                |
                <a href="#" className="text-light text-decoration-none ms-2">
                  Cookie Policy
                </a>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
