import { Bar } from "react-chartjs-2"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top" as const,
    },
    title: {
      display: true,
      text: "Access Events by Resource Type",
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: "rgba(0, 0, 0, 0.1)",
      },
    },
    x: {
      grid: {
        display: false,
      },
    },
  },
}

const data = {
  labels: [
    "Database",
    "File System",
    "API",
    "Network",
    "Applications",
    "Cloud Services",
  ],
  datasets: [
    {
      label: "Successful Access",
      data: [120, 98, 85, 75, 65, 55],
      backgroundColor: "rgba(75, 192, 192, 0.5)",
      borderColor: "rgb(75, 192, 192)",
      borderWidth: 1,
    },
    {
      label: "Failed Access",
      data: [15, 12, 8, 7, 5, 4],
      backgroundColor: "rgba(255, 99, 132, 0.5)",
      borderColor: "rgb(255, 99, 132)",
      borderWidth: 1,
    },
  ],
}

export function Overview() {
  return (
    <div className="h-[400px]">
      <Bar options={options} data={data} />
    </div>
  )
} 