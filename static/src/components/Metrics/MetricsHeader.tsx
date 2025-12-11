import React from 'react';

interface MetricsHeaderProps {
    crawlId: number;
    loading: boolean;
    onRefresh: () => void;
}

export function MetricsHeader({ crawlId, loading, onRefresh }: MetricsHeaderProps) {
    return (
        <div className="metrics-header">
            <h2>Redis Metrics (Crawl #{crawlId})</h2>
            <button className="btn btn-secondary" onClick={onRefresh} disabled={loading}>
                Refresh
            </button>
        </div>
    );
}
