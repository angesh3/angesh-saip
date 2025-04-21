export interface AccessLog {
    id: number;
    user_id: number;
    timestamp: string;
    resource_type: string;
    resource_name: string;
    action: string;
    location: string;
    success: boolean;
    ip_address: string;
    user_agent: string;
    anomaly_score: number;
}

export interface AnomalyAlert {
    id: number;
    timestamp: string;
    alert_type: string;
    severity: string;
    status: string;
    description: string;
    source_log_id: number;
    assigned_to_id: number | null;
    resolution_notes: string | null;
}

export interface DashboardStats {
    totalLogs: number;
    totalAlerts: number;
    highSeverityAlerts: number;
    activeUsers: number;
} 