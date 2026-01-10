import { useState } from "react";
import ForecastCard from "./ForecastCard";
import SalesTable from "./SalesTable";
import SalesChart from "./SalesChart";

const Dashboard = () => {
  // Renamed state to 'selectedItem'
  const [selectedItem, setSelectedItem] = useState("");

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Fertilizer Sales Dashboard
          </h1>
          <p className="text-gray-500">Inventory & Financial Analytics</p>
        </header>

        {/* Pass selectedItem to children */}
        <ForecastCard
          selectedItem={selectedItem}
          onItemChange={setSelectedItem}
        />

        <SalesChart selectedItem={selectedItem} />

        <SalesTable />
      </div>
    </div>
  );
};

export default Dashboard;
