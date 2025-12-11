import React from 'react';
import { VisitedUrlsListHeader } from './VisitedUrlsListHeader';
import { VisitedUrlsListItem } from './VisitedUrlsListItem';

interface VisitedUrlsListProps {
    patterns: { pattern: string; count: number }[];
}

export function VisitedUrlsList({ patterns }: VisitedUrlsListProps) {
    const sorted = [...patterns].sort((a, b) => b.count - a.count);

    return (
        <div className="visited-urls-list">
            <VisitedUrlsListHeader />
            {sorted.length === 0 ? (
                <div className="visited-urls-list-empty">No URLs visited yet</div>
            ) : (
                <div>
                    {sorted.map((item, i) => (
                        <VisitedUrlsListItem key={i} pattern={item.pattern} count={item.count} />
                    ))}
                </div>
            )}
        </div>
    );
}
