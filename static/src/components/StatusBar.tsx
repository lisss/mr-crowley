import React from 'react';

interface StatusBarProps {
    status: 'idle' | 'running' | 'error';
}

function StatusBar({ status }: StatusBarProps): JSX.Element {
    const statusClass = status === 'running' ? 'running' : status === 'error' ? 'error' : 'idle';
    const statusText = status === 'running' ? 'Running...' : status === 'error' ? 'Error' : 'Ready';

    return (
        <div className={`status ${statusClass}`}>
            Status: {statusText}
        </div>
    );
}

export default StatusBar;

