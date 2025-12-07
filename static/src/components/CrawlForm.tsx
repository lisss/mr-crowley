import React, { useState } from 'react';

interface CrawlFormData {
    url: string;
    user_agent?: string;
    allowed_domain?: string;
    level?: number;
    use_storage?: boolean;
}

interface CrawlFormProps {
    onSubmit: (data: CrawlFormData) => void;
    isRunning: boolean;
    onStop: () => void;
}

function CrawlForm({ onSubmit, isRunning, onStop }: CrawlFormProps): JSX.Element {
    const [url, setUrl] = useState<string>('https://crawlme.monzo.com/');
    const [userAgent, setUserAgent] = useState<string>('');
    const [allowedDomain, setAllowedDomain] = useState<string>('');
    const [level, setLevel] = useState<string>('');
    const [useStorage, setUseStorage] = useState<boolean>(false);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        e.preventDefault();
        
        if (isRunning) {
            return;
        }

        const formData: CrawlFormData = {
            url: url,
        };

        if (userAgent.trim()) {
            formData.user_agent = userAgent.trim();
        }
        if (allowedDomain.trim()) {
            formData.allowed_domain = allowedDomain.trim();
        }
        if (level.trim()) {
            formData.level = parseInt(level, 10);
        }
        if (useStorage) {
            formData.use_storage = true;
        }

        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="url">Starting URL *</label>
                <input
                    type="text"
                    id="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://crawlme.monzo.com/"
                    required
                    disabled={isRunning}
                />
            </div>
            <div className="form-group">
                <label htmlFor="user_agent">User Agent</label>
                <input
                    type="text"
                    id="user_agent"
                    value={userAgent}
                    onChange={(e) => setUserAgent(e.target.value)}
                    placeholder="CrawleyBot/1.0"
                    disabled={isRunning}
                />
            </div>
            <div className="form-group">
                <label htmlFor="allowed_domain">Allowed Domain</label>
                <input
                    type="text"
                    id="allowed_domain"
                    value={allowedDomain}
                    onChange={(e) => setAllowedDomain(e.target.value)}
                    placeholder="Leave empty to use URL domain"
                    disabled={isRunning}
                />
            </div>
            <div className="form-group">
                <label htmlFor="level">Max Depth Level</label>
                <input
                    type="number"
                    id="level"
                    value={level}
                    onChange={(e) => setLevel(e.target.value)}
                    placeholder="Leave empty for unlimited"
                    min="0"
                    disabled={isRunning}
                />
            </div>
            <div className="form-group">
                <div className="checkbox-group">
                    <input
                        type="checkbox"
                        id="use_storage"
                        checked={useStorage}
                        onChange={(e) => setUseStorage(e.target.checked)}
                        disabled={isRunning}
                    />
                    <label htmlFor="use_storage">Use Redis Storage</label>
                </div>
            </div>
            <div className="button-group">
                <button type="submit" className="btn" disabled={isRunning}>
                    Start Crawl
                </button>
                {isRunning && (
                    <button type="button" className="btn btn-danger" onClick={onStop}>
                        Stop Crawl
                    </button>
                )}
                <button type="button" className="btn btn-secondary" onClick={() => {
                    fetch('/api/clear-logs', { method: 'POST' });
                }}>
                    Clear Logs
                </button>
            </div>
        </form>
    );
}

export default CrawlForm;

