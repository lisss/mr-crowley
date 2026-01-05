import { API_ENDPOINTS } from '../../constants';

export async function stopCrawl() {
    const res = await fetch(API_ENDPOINTS.STOP_CRAWL, { method: 'POST' });
    if (!res.ok) {
        const result = await res.json();
        throw new Error(result.error || 'Failed to stop crawl');
    }
}

