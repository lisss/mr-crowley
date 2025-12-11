import React from 'react';
import { MetricsHeader } from './MetricsHeader';
import { MetricsGrid } from './MetricsGrid';
import { MetricsRatio } from './MetricsRatio';
import { MetricsWarnings } from './MetricsWarnings';
import { MetricsQueue } from './MetricsQueue';
import { useMetrics } from './useMetrics';

export default function Metrics() {
    const { metrics, queue, loading, showQueue, setShowQueue, loadData } = useMetrics();

    if (!metrics || !queue) {
        return (
            <div className="card">
                <h2>Redis Metrics</h2>
                <div>{loading ? 'Loading...' : 'No data available'}</div>
            </div>
        );
    }

    return (
        <div className="card">
            <MetricsHeader crawlId={metrics.crawl_id} loading={loading} onRefresh={loadData} />
            <MetricsGrid metrics={metrics} queueLength={queue.length} />
            <MetricsRatio metrics={metrics} />
            <MetricsWarnings metrics={metrics} queueLength={queue.length} />
            <MetricsQueue queue={queue} showQueue={showQueue} setShowQueue={setShowQueue} />
        </div>
    );
}

