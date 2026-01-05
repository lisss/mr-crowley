import { QueueData } from '../../types/QueueData';
import { API_ENDPOINTS } from '../../constants';

export async function fetchQueue(): Promise<QueueData> {
    const res = await fetch(API_ENDPOINTS.QUEUE);
    return res.json();
}

