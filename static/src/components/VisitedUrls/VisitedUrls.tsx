import React from 'react';
import { VisitedUrlsHeader } from './VisitedUrlsHeader';
import { VisitedUrlsList } from './VisitedUrlsList';
import { VisitedUrlsError } from './VisitedUrlsError';
import { useVisitedUrls } from './useVisitedUrls';

interface VisitedUrlsProps {
    isRunning: boolean;
}

export default function VisitedUrls({ isRunning }: VisitedUrlsProps) {
    const { patterns, total, loading, error, loadData } = useVisitedUrls(isRunning);

    return (
        <div className="card">
            <VisitedUrlsHeader total={total} loading={loading} onRefresh={loadData} />
            {loading && <div className="visited-urls-loading">Loading...</div>}
            {error && <VisitedUrlsError error={error} />}
            <VisitedUrlsList patterns={patterns} />
        </div>
    );
}
