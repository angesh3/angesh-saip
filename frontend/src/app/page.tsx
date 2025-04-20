'use client';

import { useState, useEffect } from 'react';
import { AccessLog, AnomalyAlert, DashboardStats } from '@/types';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Get API URL from environment variable or use default
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Dashboard() {
  const [logs, setLogs] = useState<AccessLog[]>([]);
  const [alerts, setAlerts] = useState<AnomalyAlert[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    totalLogs: 0,
    totalAlerts: 0,
    highSeverityAlerts: 0,
    activeUsers: 0
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [logsRes, alertsRes] = await Promise.all([
          fetch(`${API_URL}/logs/`),
          fetch(`${API_URL}/alerts/`)
        ]);

        const logsData = await logsRes.json();
        const alertsData = await alertsRes.json();

        setLogs(logsData);
        setAlerts(alertsData);

        // Calculate stats
        setStats({
          totalLogs: logsData.length,
          totalAlerts: alertsData.length,
          highSeverityAlerts: alertsData.filter((a: AnomalyAlert) => a.severity === 'high').length,
          activeUsers: new Set(logsData.map((l: AccessLog) => l.user_id)).size
        });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: logs.slice(-10).map(log => new Date(log.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: 'Access Events',
        data: logs.slice(-10).map((_, i) => i + 1),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Secure Access Insights Platform</h1>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm">Total Logs</h3>
          <p className="text-2xl font-bold">{stats.totalLogs}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm">Total Alerts</h3>
          <p className="text-2xl font-bold">{stats.totalAlerts}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm">High Severity Alerts</h3>
          <p className="text-2xl font-bold text-red-600">{stats.highSeverityAlerts}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm">Active Users</h3>
          <p className="text-2xl font-bold">{stats.activeUsers}</p>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <h2 className="text-xl font-bold mb-4">Access Activity</h2>
        <div className="h-64">
          <Line data={chartData} options={{
            responsive: true,
            maintainAspectRatio: false
          }} />
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Recent Alerts</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Severity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {alerts.slice(0, 5).map((alert) => (
                <tr key={alert.alert_id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {new Date(alert.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{alert.user_id}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      alert.severity === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {alert.severity}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{alert.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
} 