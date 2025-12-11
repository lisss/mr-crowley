import React from 'react';

export function VisitedUrlsListHeader() {
    return (
        <div className="visited-urls-list-header">
            <div className="visited-urls-list-header-grid">
                <div>URL pattern</div>
                <div className="count-header">Count</div>
            </div>
        </div>
    );
}
