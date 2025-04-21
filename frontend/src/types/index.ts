export interface AccessLog {
    id: number;
    user_id: string;
    timestamp: string;
    resource_type: string;
    action: string;
    status: string;
    details: string;
}

export interface AnomalyAlert {
    id: number;
    timestamp: string;
    severity: 'low' | 'medium' | 'high';
    description: string;
    source_log_id: number;
    status: 'open' | 'investigating' | 'resolved';
}

export interface DashboardStats {
    totalLogs: number;
    totalAlerts: number;
    highSeverityAlerts: number;
    activeUsers: number;
} 