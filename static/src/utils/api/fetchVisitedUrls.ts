import { VisitedUrlsData } from '../../types/VisitedUrlsData';
import { API_ENDPOINTS } from '../../constants';

export async function fetchVisitedUrls(): Promise<VisitedUrlsData> {
    const res = await fetch(API_ENDPOINTS.VISITED_URLS);
    return res.json();
}

