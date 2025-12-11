import React from 'react';

interface VisitedUrlsHeaderProps {
    total: number;
    loading: boolean;
    onRefresh: () => void;
}

export function VisitedUrlsHeader({ total, loading, onRefresh }: VisitedUrlsHeaderProps) {
    return (
        <div className="visited-urls-header">
            <h2>Visited URLs ({total})</h2>
            <button className="btn btn-secondary" onClick={onRefresh} disabled={loading}>
                Refresh
            </button>
        </div>
    );
}
