import React, { useState } from "react";
import Nav from "../components/Nav";


export default function Newsenter() {
  const [newsText, setNewsText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!newsText.trim()) {
      setError("Please enter some news text to analyze");
      return;
    }

    setIsAnalyzing(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: newsText,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze news");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Error analyzing news. Please try again.");
      console.error("Analysis error:", err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearInput = () => {
    setNewsText("");
    setResult(null);
    setError("");
  };

  const getResultColor = (prediction) => {
    return prediction === "FAKE" ? "text-danger" : "text-success";
  };

  const getResultBadgeColor = (prediction) => {
    return prediction === "FAKE" ? "bg-danger" : "bg-success";
  };

  return (
    <div>
      <Nav />



      {/* Main Content Section */}
      <section className="news-analysis-section py-5">
        <div className="container ">
          <div className="row justify-content-center">
            <div className="col-lg-10">
              {/* Input Section */}
              <div className="card shadow-lg border-0 mb-4">
                <div className="card-header bg-primary text-white">
                  <h4 className="mb-0">
                    <i className="fas fa-newspaper me-2"></i>
                    Enter News Content
                  </h4>
                </div>
                <div className="card-body p-4">
                  <div className="mb-4">
                    <label
                      htmlFor="newsText"
                      className="form-label fw-semibold"
                    >
                      News Article or Content
                    </label>
                    <textarea
                      id="newsText"
                      className="form-control"
                      rows="8"
                      value={newsText}
                      onChange={(e) => setNewsText(e.target.value)}
                      placeholder="Paste your news article, social media post, or any text content you want to verify here..."
                      style={{ resize: "vertical" }}
                    />
                    <div className="form-text">
                      <i className="fas fa-info-circle me-1"></i>
                      For best results, enter at least 50 characters of content
                    </div>
                  </div>

                  {error && (
                    <div
                      className="alert alert-danger d-flex align-items-center"
                      role="alert"
                    >
                      <i className="fas fa-exclamation-triangle me-2"></i>
                      {error}
                    </div>
                  )}

                  <div className="d-flex gap-3 flex-wrap">
                    <button
                      className="btn btn-primary btn-lg px-4"
                      onClick={handleAnalyze}
                      disabled={isAnalyzing || !newsText.trim()}
                    >
                      {isAnalyzing ? (
                        <>
                          <span
                            className="spinner-border spinner-border-sm me-2"
                            role="status"
                          ></span>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <i className="fas fa-search me-2"></i>
                          Analyze News
                        </>
                      )}
                    </button>

                    <button
                      className="btn btn-outline-secondary btn-lg px-4"
                      onClick={clearInput}
                      disabled={isAnalyzing}
                    >
                      <i className="fas fa-times me-2"></i>
                      Clear
                    </button>
                  </div>
                </div>
              </div>

              {/* Results Section */}
              {result && (
                <div className="card shadow-lg border-0 mb-4">
                  <div className="card-header bg-light">
                    <h4 className="mb-0">
                      <i className="fas fa-chart-bar me-2"></i>
                      Analysis Results
                    </h4>
                  </div>
                  <div className="card-body p-4">
                    <div className="row">
                      <div className="col-md-6 mb-4">
                        <div className="text-center">
                          <h5 className="fw-bold mb-3">Prediction</h5>
                          <span
                            className={`badge ${getResultBadgeColor(
                              result.prediction
                            )} fs-4 px-4 py-2`}
                          >
                            {result.prediction}
                          </span>
                        </div>
                      </div>

                      <div className="col-md-6 mb-4">
                        <div className="text-center">
                          <h5 className="fw-bold mb-3">Confidence Score</h5>
                          <div
                            className="progress mb-2"
                            style={{ height: "25px" }}
                          >
                            <div
                              className={`progress-bar ${
                                result.prediction === "FAKE"
                                  ? "bg-danger"
                                  : "bg-success"
                              }`}
                              role="progressbar"
                              style={{
                                width: `${(result.confidence * 100).toFixed(
                                  1
                                )}%`,
                              }}
                            >
                              {(result.confidence * 100).toFixed(1)}%
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {result.probabilities && (
                      <div className="mt-4">
                        <h5 className="fw-bold mb-3">Detailed Probabilities</h5>
                        <div className="row">
                          <div className="col-md-6">
                            <div className="d-flex justify-content-between align-items-center mb-2">
                              <span className="fw-semibold">Real News:</span>
                              <span className="text-success fw-bold">
                                {(result.probabilities.REAL * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div
                              className="progress mb-3"
                              style={{ height: "8px" }}
                            >
                              <div
                                className="progress-bar bg-success"
                                style={{
                                  width: `${(
                                    result.probabilities.REAL * 100
                                  ).toFixed(1)}%`,
                                }}
                              ></div>
                            </div>
                          </div>

                          <div className="col-md-6">
                            <div className="d-flex justify-content-between align-items-center mb-2">
                              <span className="fw-semibold">Fake News:</span>
                              <span className="text-danger fw-bold">
                                {(result.probabilities.FAKE * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div
                              className="progress mb-3"
                              style={{ height: "8px" }}
                            >
                              <div
                                className="progress-bar bg-danger"
                                style={{
                                  width: `${(
                                    result.probabilities.FAKE * 100
                                  ).toFixed(1)}%`,
                                }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    <div className="alert alert-info mt-4">
                      <i className="fas fa-info-circle me-2"></i>
                      <strong>Note:</strong> This analysis is based on AI
                      predictions and should be used as a guide. Always verify
                      information through multiple reliable sources.
                    </div>
                  </div>
                </div>
              )}

            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
