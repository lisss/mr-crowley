import { API_ENDPOINTS } from '../../constants';

export async function clearLogs() {
    await fetch(API_ENDPOINTS.CLEAR_LOGS, { method: 'POST' });
}

