import React from 'react';
import { MetricsData } from '../../types/MetricsData';

interface MetricsGridProps {
    metrics: MetricsData;
    queueLength: number;
}

function getColorClass(color: string): string {
    if (color === '#28a745') return 'color-green';
    if (color === '#007bff') return 'color-blue';
    if (color === '#ffc107') return 'color-yellow';
    if (color === '#dc3545') return 'color-red';
    return 'color-green';
}

export function MetricsGrid({ metrics, queueLength }: MetricsGridProps) {
    return (
        <div className="metrics-grid">
            <MetricCard label="Visited URLs" value={metrics.visited} colorClass="color-green" />
            <MetricCard label="Seen URLs" value={metrics.seen} colorClass="color-blue" />
            <MetricCard label="Queued (Set)" value={metrics.queued} colorClass="color-yellow" />
            <MetricCard label="Queue Length" value={queueLength} colorClass={queueLength > 0 ? 'color-red' : 'color-green'} />
        </div>
    );
}

function MetricCard({ label, value, colorClass }: { label: string; value: number; colorClass: string }) {
    return (
        <div className="metrics-card">
            <div className="metrics-card-label">{label}</div>
            <div className={`metrics-card-value ${colorClass}`}>{value}</div>
        </div>
    );
}
