const API_BASE = '/api';

async function transcribeVideo(url, n, modelSize) {
    const response = await fetch(`${API_BASE}/transcribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, n, model_size: modelSize })
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Transcription failed');
    }
    return response.json();
}

async function transcribeChain(url, n, modelSize) {
    const response = await fetch(`${API_BASE}/transcribe-chain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, n, model_size: modelSize })
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Transcription failed');
    }
    return response.json();
}

async function getVideos(url, n) {
    const params = new URLSearchParams({ url, n });
    const response = await fetch(`${API_BASE}/videos?${params}`);
    if (!response.ok) {
        throw new Error('Failed to get videos');
    }
    return response.json();
}

async function getTranscripts() {
    const response = await fetch(`${API_BASE}/transcripts`);
    if (!response.ok) {
        throw new Error('Failed to get transcripts');
    }
    return response.json();
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function renderResults(results) {
    const container = document.getElementById('results-content');
    const section = document.getElementById('results-section');
    
    section.style.display = 'block';
    
    if (!Array.isArray(results)) {
        results = [results];
    }
    
    container.innerHTML = results.map(result => {
        const isSuccess = !result.error;
        const status = isSuccess ? result.source : 'error';
        const statusClass = isSuccess ? 'result-item__status--success' : 'result-item__status--error';
        const transcript = result.transcript || '';
        const preview = transcript.length > 500 ? transcript.substring(0, 500) + '...' : transcript;
        
        return `
            <div class="result-item">
                <div class="result-item__header">
                    <span class="result-item__title">${result.title || 'Untitled'}</span>
                    <span class="result-item__status ${statusClass}">${status}</span>
                </div>
                <div class="result-item__url">${result.url}</div>
                ${result.error ? `<div class="error">${result.error}</div>` : ''}
                ${transcript ? `<div class="result-item__transcript">${preview}</div>` : ''}
            </div>
        `;
    }).join('');
}

function renderTranscripts(transcripts) {
    const container = document.getElementById('transcripts-content');
    
    if (!transcripts || transcripts.length === 0) {
        container.innerHTML = '<p class="empty-state">No transcripts saved yet</p>';
        return;
    }
    
    container.innerHTML = `
        <div class="transcripts-list__items">
            ${transcripts.map(t => `
                <div class="transcript-item">
                    <span class="transcript-item__name">${t.filename}</span>
                    <span class="transcript-item__size">${formatFileSize(t.size)}</span>
                </div>
            `).join('')}
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('transcribe-form');
    const getVideosBtn = document.getElementById('get-videos-btn');
    const refreshTranscriptsBtn = document.getElementById('refresh-transcripts');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = document.getElementById('url').value;
        const n = parseInt(document.getElementById('n-videos').value) || 1;
        const modelSize = document.getElementById('model-size').value;
        
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Transcribing...';
        
        try {
            let results;
            if (n === 1) {
                results = await transcribeVideo(url, n, modelSize);
            } else {
                results = await transcribeChain(url, n, modelSize);
            }
            renderResults(results);
            refreshTranscriptsBtn.click();
        } catch (error) {
            const container = document.getElementById('results-section');
            const content = document.getElementById('results-content');
            container.style.display = 'block';
            content.innerHTML = `<div class="error">${error.message}</div>`;
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Transcribe';
        }
    });
    
    getVideosBtn.addEventListener('click', async () => {
        const url = document.getElementById('url').value;
        const n = parseInt(document.getElementById('n-videos').value) || 5;
        
        if (!url) {
            alert('Please enter a YouTube URL');
            return;
        }
        
        getVideosBtn.disabled = true;
        getVideosBtn.textContent = 'Loading...';
        
        try {
            const videos = await getVideos(url, n);
            renderResults(videos.map(v => ({ title: v.title, url: v.url, source: 'video' })));
        } catch (error) {
            alert(error.message);
        } finally {
            getVideosBtn.disabled = false;
            getVideosBtn.textContent = 'Get Videos';
        }
    });
    
    refreshTranscriptsBtn.addEventListener('click', async () => {
        const container = document.getElementById('transcripts-content');
        container.innerHTML = '<p class="loading">Loading...</p>';
        
        try {
            const transcripts = await getTranscripts();
            renderTranscripts(transcripts);
        } catch (error) {
            container.innerHTML = `<div class="error">${error.message}</div>`;
        }
    });
    
    refreshTranscriptsBtn.click();
});
