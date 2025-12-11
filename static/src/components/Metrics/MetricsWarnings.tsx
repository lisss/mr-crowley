import React from 'react';
import { MetricsData } from '../../types/MetricsData';

interface MetricsWarningsProps {
    metrics: MetricsData;
    queueLength: number;
}

export function MetricsWarnings({ metrics, queueLength }: MetricsWarningsProps) {
    return (
        <>
            {metrics.seen > metrics.visited && (
                <div className="metrics-warning metrics-warning-yellow">
                    <div>
                        ⚠️ {metrics.seen - metrics.visited} URLs were seen but not visited
                    </div>
                </div>
            )}
            {queueLength > 0 && (
                <div className="metrics-warning metrics-warning-red">
                    <div>
                        ⚠️ {queueLength} URLs still in queue
                    </div>
                </div>
            )}
        </>
    );
}
