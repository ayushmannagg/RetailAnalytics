import { useEffect, useState } from "react";
import apiClient from "../api/client";
import { TrendingUp, TrendingDown, Filter } from "lucide-react";

const ForecastCard = ({ selectedItem, onItemChange }) => {
  const [forecast, setForecast] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  // 1. Fetch List of Items (Urea, DAP, etc.)
  useEffect(() => {
    apiClient
      .get("/sales/items")
      .then((res) => setItems(res.data))
      .catch((err) => console.error("Error fetching items:", err));
  }, []);

  // 2. Fetch Forecast
  useEffect(() => {
    setLoading(true);
    // Updated Query Parameter: ?item=...
    const url = selectedItem
      ? `/sales/forecast?item=${encodeURIComponent(selectedItem)}`
      : "/sales/forecast";

    apiClient
      .get(url)
      .then((response) => {
        setForecast(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Forecast error:", error);
        setLoading(false);
      });
  }, [selectedItem]);

  return (
    <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow mb-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-700">
            🔮 Next Month Forecast
          </h3>
          <p className="text-xs text-gray-400">
            AI Prediction for:{" "}
            <span className="font-bold text-gray-600">
              {selectedItem || "Total Sales"}
            </span>
          </p>
        </div>

        {/* Dropdown for Items */}
        <div className="relative">
          <Filter className="absolute left-2 top-2.5 text-gray-400" size={14} />
          <select
            className="pl-7 pr-3 py-1.5 text-sm border rounded-md text-gray-600 bg-gray-50 focus:ring-2 focus:ring-green-500 outline-none max-w-[200px]"
            value={selectedItem}
            onChange={(e) => onItemChange(e.target.value)}
          >
            <option value="">All Items</option>
            {items.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="animate-pulse h-10 w-32 bg-gray-200 rounded"></div>
      ) : forecast ? (
        <div className="flex items-center gap-4">
          <div className="text-3xl font-bold text-green-700">
            ₹{forecast.next_month_prediction.toLocaleString("en-IN")}
          </div>

          <div
            className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
              forecast.trend_direction === "Up"
                ? "bg-green-100 text-green-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {forecast.trend_direction === "Up" ? (
              <TrendingUp size={16} />
            ) : (
              <TrendingDown size={16} />
            )}
            {forecast.trend_direction}
          </div>
        </div>
      ) : (
        <div className="text-red-400 text-sm">Not enough data history.</div>
      )}
    </div>
  );
};

export default ForecastCard;
