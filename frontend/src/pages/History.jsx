import React, { useState, useEffect } from "react";
import Nav from "../components/Nav";
import { useAuth } from "../context/AuthContext";
import { newsAPI } from "../utils/api";

export default function History() {
  const { user, isAuthenticated } = useAuth();
  const [historyItems, setHistoryItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState(null); // Load user's analysis history and stats
  useEffect(() => {
    const loadHistoryAndStats = async () => {
      if (!isAuthenticated()) {
        setIsLoading(false);
        return;
      }

      try {
        setError("");

        // Load history and stats in parallel
        const [historyResponse, statsResponse] = await Promise.all([
          newsAPI.getHistory(),
          newsAPI.getStats(),
        ]);

        setHistoryItems(historyResponse.history || []);
        setStats(statsResponse);
      } catch (err) {
        console.error("Failed to load history:", err);
        setError("Failed to load analysis history. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    loadHistoryAndStats();
  }, [isAuthenticated]);
  const deleteItem = async (id) => {
    if (window.confirm("Are you sure you want to delete this item?")) {
      try {
        await newsAPI.deleteAnalysis(id);
        setHistoryItems(historyItems.filter((item) => item.id !== id));
      } catch (err) {
        console.error("Failed to delete item:", err);
        setError("Failed to delete item. Please try again.");
      }
    }
  };

  const clearAllHistory = async () => {
    if (
      window.confirm(
        "Are you sure you want to clear all history? This action cannot be undone."
      )
    ) {
      try {
        await newsAPI.clearHistory();
        setHistoryItems([]);
        setStats({ ...stats, total_analyses: 0, fake_count: 0, real_count: 0 });
      } catch (err) {
        console.error("Failed to clear history:", err);
        setError("Failed to clear history. Please try again.");
      }
    }
  };
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getPredictionBadgeClass = (prediction) => {
    return prediction === "FAKE" ? "bg-danger" : "bg-success";
  };

  const truncateText = (text, maxLength = 150) => {
    return text.length > maxLength
      ? text.substring(0, maxLength) + "..."
      : text;
  };

  return (
    <div>
      <Nav />
      {/* Header Section */}
      <section className="history-header bg-light">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h1 className="display-5 fw-bold mb-2">Analysis History</h1>
              <p className="text mb-0">
                View and manage your previous news analysis results
              </p>
            </div>
            <div className="col-md-4 text-md-end">
              {historyItems.length > 0 && (
                <button
                  className="btn btn-outline-danger"
                  onClick={clearAllHistory}
                >
                  <i className="fas fa-trash me-2"></i>
                  Clear All History
                </button>
              )}
            </div>
          </div>
          <hr className="mt-3 mb-0" />
        </div>
      </section>{" "}
      {/* Stats Section */}
      {stats && (
        <section className="stats-section bg-white py-4 border-bottom">
          <div className="container">
            <div className="row text-center">
              <div className="col-md-3">
                <div className="stat-item">
                  <h3 className="h4 text-primary mb-1">
                    {stats.total_analyses}
                  </h3>
                  <p className="text-muted mb-0">Total Analyses</p>
                </div>
              </div>
              <div className="col-md-3">
                <div className="stat-item">
                  <h3 className="h4 text-success mb-1">{stats.real_count}</h3>
                  <p className="text-muted mb-0">Real News</p>
                </div>
              </div>
              <div className="col-md-3">
                <div className="stat-item">
                  <h3 className="h4 text-danger mb-1">{stats.fake_count}</h3>
                  <p className="text-muted mb-0">Fake News</p>
                </div>
              </div>
              <div className="col-md-3">
                <div className="stat-item">
                  <h3 className="h4 text-info mb-1">
                    {(stats.average_confidence * 100).toFixed(1)}%
                  </h3>
                  <p className="text-muted mb-0">Avg Confidence</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
      {/* History Content */}
      <section className="history-content">
        <div className="container">
          {/* Error Message */}
          {error && (
            <div className="alert alert-danger mt-4" role="alert">
              <i className="fas fa-exclamation-triangle me-2"></i>
              {error}
            </div>
          )}

          {isLoading ? (
            // Loading State
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <p className="text-muted mt-3">
                Loading your analysis history...
              </p>
            </div>
          ) : historyItems.length === 0 ? (
            // Empty State
            <div className="text-center py-5">
              <i
                className="fas fa-history text-muted mb-3"
                style={{ fontSize: "4rem" }}
              ></i>
              <h3 className="text-muted mb-3">No Analysis History</h3>
              <p className="text-muted mb-4">
                You haven't analyzed any news yet. Start by checking some news
                content!
              </p>
              <a href="/analyze" className="btn btn-primary">
                <i className="fas fa-plus me-2"></i>
                Analyze News
              </a>
            </div>
          ) : (
            // History Items
            <div className="row">
              {historyItems.map((item) => (
                <div key={item.id} className="col-12 mb-4">
                  <div className="card shadow-sm border-0 h-100">
                    <div className="card-body">
                      <div className="row align-items-start">
                        <div className="col-md-8">
                          <div className="d-flex align-items-center mb-2">
                            <span
                              className={`badge ${getPredictionBadgeClass(
                                item.prediction
                              )} me-2`}
                            >
                              {item.prediction}
                            </span>
                            <small className="text-muted">
                              Confidence: {(item.confidence * 100).toFixed(1)}%
                            </small>
                          </div>{" "}
                          <p className="card-text mb-3">
                            "{truncateText(item.text)}"
                          </p>
                          <div className="d-flex align-items-center text-muted">
                            <i className="fas fa-calendar me-2"></i>
                            <small className="me-3">
                              {formatDate(item.analyzed_at)}
                            </small>
                            <i className="fas fa-clock me-2"></i>
                            <small>{formatTime(item.analyzed_at)}</small>
                          </div>
                        </div>
                        <div className="col-md-4 text-md-end">
                          <div className="btn-group" role="group">
                            <button
                              className="btn btn-outline-primary btn-sm"
                              onClick={() => {
                                // In a real app, this would navigate to the analysis page with this text
                                alert(
                                  "Feature coming soon: Re-analyze this content"
                                );
                              }}
                            >
                              <i className="fas fa-redo me-1"></i>
                              Re-analyze
                            </button>
                            <button
                              className="btn btn-outline-danger btn-sm"
                              onClick={() => deleteItem(item.id)}
                            >
                              <i className="fas fa-trash"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
