import React from 'react';
import { MetricsData } from '../../types/MetricsData';

interface MetricsRatioProps {
    metrics: MetricsData;
}

export function MetricsRatio({ metrics }: MetricsRatioProps) {
    const visitedVsSeen = metrics.seen > 0 
        ? ((metrics.visited / metrics.seen) * 100).toFixed(1)
        : '0.0';

    return (
        <div className="metrics-ratio">
            <div className="metrics-ratio-label">Visited / Seen Ratio</div>
            <div className="metrics-ratio-value">
                {visitedVsSeen}%
            </div>
            <div className="metrics-ratio-detail">
                {metrics.visited} visited out of {metrics.seen} seen URLs
            </div>
        </div>
    );
}
