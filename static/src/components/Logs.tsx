import React from 'react';

interface LogsProps {
    logs: string;
}

function Logs({ logs }: LogsProps): JSX.Element {
    return (
        <div className="card">
            <h2 style={{ marginBottom: '15px' }}>Crawl Logs</h2>
            <div className="logs">{logs}</div>
        </div>
    );
}

export default Logs;

