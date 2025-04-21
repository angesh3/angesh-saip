import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const alerts = [
  {
    id: 1,
    timestamp: "2024-03-19T10:30:00Z",
    user: "john.doe@example.com",
    severity: "high",
    description: "Multiple failed login attempts detected",
  },
  {
    id: 2,
    timestamp: "2024-03-19T09:45:00Z",
    user: "alice.smith@example.com",
    severity: "medium",
    description: "Unusual file access pattern observed",
  },
  {
    id: 3,
    timestamp: "2024-03-19T09:15:00Z",
    user: "bob.wilson@example.com",
    severity: "high",
    description: "Unauthorized access attempt to restricted resource",
  },
  {
    id: 4,
    timestamp: "2024-03-19T08:30:00Z",
    user: "carol.brown@example.com",
    severity: "low",
    description: "New device connection detected",
  },
]

export function RecentAlerts() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[150px]">Time</TableHead>
          <TableHead>User</TableHead>
          <TableHead className="w-[100px]">Severity</TableHead>
          <TableHead>Description</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {alerts.map((alert) => (
          <TableRow key={alert.id}>
            <TableCell className="font-medium">
              {new Date(alert.timestamp).toLocaleTimeString()}
            </TableCell>
            <TableCell>{alert.user}</TableCell>
            <TableCell>
              <span
                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                  alert.severity === "high"
                    ? "bg-red-100 text-red-800"
                    : alert.severity === "medium"
                    ? "bg-yellow-100 text-yellow-800"
                    : "bg-green-100 text-green-800"
                }`}
              >
                {alert.severity}
              </span>
            </TableCell>
            <TableCell>{alert.description}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
} 