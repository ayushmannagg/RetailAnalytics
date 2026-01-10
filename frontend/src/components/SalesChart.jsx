import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import apiClient from "../api/client";

const SalesChart = ({ selectedItem }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    let url = "/sales/?limit=50";
    if (selectedItem) {
      url += `&item=${encodeURIComponent(selectedItem)}`;
    }

    apiClient
      .get(url)
      .then((res) => {
        // Format for Chart: Sort by Date Ascending
        const formattedData = res.data
          .sort((a, b) => new Date(a.date) - new Date(b.date))
          .map((item) => ({
            date: new Date(item.date).toLocaleDateString("en-IN"), // Indian Date Format
            amount: item.amount,
          }));
        setData(formattedData);
      })
      .catch((err) => console.error(err));
  }, [selectedItem]);

  return (
    <div className="mt-8 bg-white p-6 rounded-lg shadow border border-gray-200 mb-8">
      <h3 className="text-lg font-semibold text-gray-700 mb-4">
        Sales Trend: {selectedItem || "All Items"}
      </h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" hide />
            <YAxis />
            <Tooltip
              formatter={(value) => [`₹${value}`, "Amount"]}
              contentStyle={{
                borderRadius: "8px",
                border: "none",
                boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
              }}
            />
            <Line
              type="monotone"
              dataKey="amount"
              stroke="#16a34a" // Green color for Agriculture
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SalesChart;
