import { CrawlFormData } from '../../types/CrawlFormData';
import { API_ENDPOINTS } from '../../constants';

export async function startCrawl(data: CrawlFormData) {
    const res = await fetch(API_ENDPOINTS.START_CRAWL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const result = await res.json();
        throw new Error(result.error || 'Failed to start crawl');
    }
}

