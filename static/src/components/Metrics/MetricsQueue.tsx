import React from 'react';
import { QueueData } from '../../types/QueueData';

interface MetricsQueueProps {
    queue: QueueData;
    showQueue: boolean;
    setShowQueue: (show: boolean) => void;
}

export function MetricsQueue({ queue, showQueue, setShowQueue }: MetricsQueueProps) {
    return (
        <div className="metrics-queue">
            <button 
                className="btn btn-secondary metrics-queue-toggle"
                onClick={() => setShowQueue(!showQueue)}
            >
                {showQueue ? 'Hide' : 'Show'} Queue ({queue.length} items)
            </button>

            {showQueue && (
                <div className="metrics-queue-container">
                    {queue.queue.length === 0 ? (
                        <div className="metrics-queue-empty">
                            Queue is empty
                        </div>
                    ) : (
                        <table>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>URL</th>
                                </tr>
                            </thead>
                            <tbody>
                                {queue.queue.map((url, index) => (
                                    <tr key={index}>
                                        <td>{index + 1}</td>
                                        <td>{url}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            )}
        </div>
    );
}
