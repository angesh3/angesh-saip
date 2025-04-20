export interface AccessLog {
    user_id: string;
    timestamp: string;
    resource: string;
    action: string;
    ip_address: string;
    location?: string;
    device_type?: string;
    status: string;
}

export interface AnomalyAlert {
    alert_id: string;
    user_id: string;
    timestamp: string;
    severity: string;
    description: string;
    details: {
        resource: string;
        action: string;
        ip_address: string;
    };
}

export interface DashboardStats {
    totalLogs: number;
    totalAlerts: number;
    highSeverityAlerts: number;
    activeUsers: number;
} 