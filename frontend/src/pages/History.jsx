import React, { useState, useEffect } from "react";
import Nav from "../components/Nav";

export default function History() {
  const [historyItems, setHistoryItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data - in a real app, this would come from an API or local storage
  useEffect(() => {
    // Simulate loading delay
    setTimeout(() => {
      const mockHistory = [
        {
          id: 1,
          newsText:
            "Breaking: Scientists discover new method for detecting misinformation using advanced AI algorithms that can analyze text patterns and cross-reference multiple sources in real-time.",
          prediction: "REAL",
          confidence: 0.92,
          date: new Date("2025-09-30T14:30:00"),
        },
        {
          id: 2,
          newsText:
            "SHOCKING: Local man discovers this one weird trick that doctors hate! Click here to learn the secret that pharmaceutical companies don't want you to know.",
          prediction: "FAKE",
          confidence: 0.87,
          date: new Date("2025-09-30T12:15:00"),
        },
        {
          id: 3,
          newsText:
            "The government announced new funding for renewable energy projects, allocating $2 billion for solar and wind power infrastructure development across the country.",
          prediction: "REAL",
          confidence: 0.89,
          date: new Date("2025-09-29T16:45:00"),
        },
        {
          id: 4,
          newsText:
            "URGENT: Aliens have landed in downtown and are distributing free pizza to everyone! The mayor has declared a state of emergency due to the overwhelming deliciousness.",
          prediction: "FAKE",
          confidence: 0.95,
          date: new Date("2025-09-29T10:20:00"),
        },
        {
          id: 5,
          newsText:
            "Research published in Nature journal shows promising results for new cancer treatment, with clinical trials showing 70% improvement in patient outcomes.",
          prediction: "REAL",
          confidence: 0.91,
          date: new Date("2025-09-28T13:10:00"),
        },
      ];
      setHistoryItems(mockHistory);
      setIsLoading(false);
    }, 1000);
  }, []);

  const deleteItem = (id) => {
    if (window.confirm("Are you sure you want to delete this item?")) {
      setHistoryItems(historyItems.filter((item) => item.id !== id));
    }
  };

  const clearAllHistory = () => {
    if (
      window.confirm(
        "Are you sure you want to clear all history? This action cannot be undone."
      )
    ) {
      setHistoryItems([]);
    }
  };

  const formatDate = (date) => {
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const formatTime = (date) => {
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
      </section>

      {/* History Content */}
      <section className="history-content">
        <div className="container">
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
                          </div>
                          <p className="card-text mb-3">
                            "{truncateText(item.newsText)}"
                          </p>
                          <div className="d-flex align-items-center text-muted">
                            <i className="fas fa-calendar me-2"></i>
                            <small className="me-3">
                              {formatDate(item.date)}
                            </small>
                            <i className="fas fa-clock me-2"></i>
                            <small>{formatTime(item.date)}</small>
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
