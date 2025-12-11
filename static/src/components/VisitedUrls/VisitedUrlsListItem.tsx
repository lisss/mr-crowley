import React from 'react';

interface VisitedUrlsListItemProps {
    pattern: string;
    count: number;
}

export function VisitedUrlsListItem({ pattern, count }: VisitedUrlsListItemProps) {
    return (
        <div className="visited-urls-list-item">
            <div className="visited-urls-list-item-pattern">
                {pattern}
            </div>
            <div className="visited-urls-list-item-count">
                <span>{count}</span>
            </div>
        </div>
    );
}
