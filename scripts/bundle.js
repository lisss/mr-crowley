const fs = require('fs');
const path = require('path');

const distDir = path.join(__dirname, '../static/dist');
const componentsDir = path.join(distDir, 'components');

const componentFiles = ['StatusBar.js', 'Logs.js', 'CrawlForm.js'];
let componentsCode = '';

componentFiles.forEach(file => {
    const filePath = path.join(componentsDir, file);
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        content = content.replace(/import\s+.*?from\s+['"].*?['"];?/g, '');
        content = content.replace(/export\s+default\s+/g, '');
        content = content.replace(/export\s+\{.*?\}\s+from\s+['"].*?['"];?/g, '');
        componentsCode += content + '\n';
    }
});

let appCode = fs.readFileSync(path.join(distDir, 'App.js'), 'utf8');
appCode = appCode.replace(/import\s+.*?from\s+['"].*?['"];?/g, '');
const lines = appCode.split('\n');
const filteredLines = lines.filter(line => {
    return !line.includes('ReactDOM.createRoot') && !line.includes('root.render');
});
appCode = filteredLines.join('\n').trim();

const bundle = `const React = window.React;
const ReactDOM = window.ReactDOM;
const { useState, useEffect, useCallback, useRef } = React;
${componentsCode}
${appCode}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(React.createElement(App, null));
    });
} else {
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(React.createElement(App, null));
}`;

fs.writeFileSync(path.join(distDir, 'bundle.js'), bundle);
console.log('Bundle created successfully');

