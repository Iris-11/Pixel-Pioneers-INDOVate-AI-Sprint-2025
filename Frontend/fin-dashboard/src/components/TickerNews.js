import React, { useState } from "react";
import axios from "axios";

const TickerNews = () => {
  const [ticker, setTicker] = useState("");
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchNews = async () => {
    if (!ticker) return;
    setLoading(true);
    setError("");

    try {
      const response = await axios.get(
        `http://localhost:5000/market-news/search?ticker=${ticker}`
      );
      setNews(response.data);
    } catch (err) {
      setError("No news found for this ticker.");
      setNews([]);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    if (sentiment.label === "positive") return "bg-green-500";
    if (sentiment.label === "neutral") return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="max-w-2xl mx-auto mt-8 p-4 border rounded-lg shadow-lg bg-white">
      <h2 className="text-xl font-bold mb-4">Stock News Search</h2>
      <div className="flex">
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="Enter Ticker (e.g., AAPL)"
          className="border p-2 rounded w-full"
        />
        <button
          onClick={fetchNews}
          className="ml-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-gray-500 mt-4">Loading...</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}

      <div className="mt-4 max-h-80 overflow-y-auto border rounded p-2">
        {news.map((article, index) => (
          <div key={index} className="mb-3 p-2 border-b">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-700 font-semibold hover:underline"
            >
              {article.headline}
            </a>
            <p className="text-sm text-gray-500">{article.source}</p>
            <span
              className={`inline-block px-2 py-1 text-xs text-white rounded ${getSentimentColor(
                article.sentiment
              )}`}
            >
              {article.sentiment.label.toUpperCase()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TickerNews;
