import { useEffect, useState } from 'react';
import apiClient from '../api/client';

const SalesTable = () => {
  const [sales, setSales] = useState([]);

  useEffect(() => {
    apiClient.get('/sales/?limit=10') 
      .then(res => setSales(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="mt-8 bg-white border rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b bg-gray-50">
        <h3 className="font-bold text-gray-700">Recent Transactions</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-gray-600">
          <thead className="bg-gray-100 uppercase text-xs font-semibold text-gray-500">
            <tr>
              <th className="px-6 py-3">Date</th>
              <th className="px-6 py-3">Customer</th>
              <th className="px-6 py-3">Item</th>
              <th className="px-6 py-3 text-right">Qty</th>
              <th className="px-6 py-3 text-right">Rate</th>
              <th className="px-6 py-3 text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {sales.map((sale) => (
              <tr key={sale.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(sale.date).toLocaleDateString('en-IN')}
                </td>
                <td className="px-6 py-4 font-medium text-gray-900">{sale.customer_name}</td>
                <td className="px-6 py-4">
                  {sale.item_details}
                  <span className="ml-2 text-xs text-gray-400">({sale.unit})</span>
                </td>
                <td className="px-6 py-4 text-right">{sale.quantity}</td>
                <td className="px-6 py-4 text-right">₹{sale.rate}</td>
                <td className="px-6 py-4 text-right font-bold text-green-700">
                  ₹{sale.amount.toLocaleString('en-IN')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SalesTable;