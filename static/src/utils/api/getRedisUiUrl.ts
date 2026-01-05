import { API_ENDPOINTS } from '../../constants';

export async function getRedisUiUrl(): Promise<string | null> {
    try {
        const res = await fetch(API_ENDPOINTS.REDIS_UI_URL);
        const data = await res.json();
        return data.url || null;
    } catch {
        return null;
    }
}

