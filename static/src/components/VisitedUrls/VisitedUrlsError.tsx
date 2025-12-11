import React from 'react';

interface VisitedUrlsErrorProps {
    error: string;
}

export function VisitedUrlsError({ error }: VisitedUrlsErrorProps) {
    return (
        <div className="visited-urls-error">
            <strong>Error:</strong> {error}
        </div>
    );
}
