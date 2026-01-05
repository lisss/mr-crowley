import { LogsResponse } from '../../types/LogsResponse';
import { API_ENDPOINTS } from '../../constants';

export async function fetchLogs(): Promise<LogsResponse> {
    const res = await fetch(API_ENDPOINTS.LOGS);
    return res.json();
}

