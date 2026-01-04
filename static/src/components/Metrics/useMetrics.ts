import { useState, useEffect } from 'react';
import { MetricsData } from '../../types/MetricsData';
import { QueueData } from '../../types/QueueData';
import { fetchMetrics } from '../../utils/api/fetchMetrics';
import { fetchQueue } from '../../utils/api/fetchQueue';
import { METRICS_POLLING_INTERVAL } from '../../constants';

export function useMetrics() {
    const [metrics, setMetrics] = useState<MetricsData | null>(null);
    const [queue, setQueue] = useState<QueueData | null>(null);
    const [loading, setLoading] = useState(false);
    const [showQueue, setShowQueue] = useState(false);

    const loadData = async () => {
        setLoading(true);
        try {
            const [metricsData, queueData] = await Promise.all([
                fetchMetrics(),
                fetchQueue()
            ]);
            setMetrics(metricsData);
            setQueue(queueData);
        } catch (error) {
            console.error('Error fetching metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
        const interval = setInterval(loadData, METRICS_POLLING_INTERVAL);
        return () => clearInterval(interval);
    }, []);

    return { metrics, queue, loading, showQueue, setShowQueue, loadData };
}

