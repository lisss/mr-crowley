import { MetricsData } from '../../types/MetricsData';
import { API_ENDPOINTS } from '../../constants';

export async function fetchMetrics(): Promise<MetricsData> {
    const res = await fetch(API_ENDPOINTS.METRICS);
    return res.json();
}

