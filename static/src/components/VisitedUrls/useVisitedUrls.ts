import { useState, useEffect } from 'react';
import { VisitedUrlsData } from '../../types/VisitedUrlsData';
import { fetchVisitedUrls } from '../../utils/api/fetchVisitedUrls';
import { groupUrlsByPattern } from '../../utils/urlPatterns';

export function useVisitedUrls(isRunning: boolean) {
    const [patterns, setPatterns] = useState<{ pattern: string; count: number }[]>([]);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const loadData = async () => {
        setLoading(true);
        setError(null);
        try {
            const data: VisitedUrlsData = await fetchVisitedUrls();
            if (!data.visited || data.error) {
                setError(data.error || 'Failed to load URLs');
                setTotal(0);
                setPatterns([]);
                return;
            }
            const grouped = groupUrlsByPattern(data.visited);
            setPatterns(grouped);
            setTotal(data.visited.length);
        } catch (err) {
            setError(`Failed to fetch URLs: ${err instanceof Error ? err.message : 'Unknown error'}`);
            setTotal(0);
            setPatterns([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    useEffect(() => {
        if (!isRunning) {
            loadData();
        }
    }, [isRunning]);

    return { patterns, total, loading, error, loadData };
}

