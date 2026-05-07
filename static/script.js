// Function to handle Paging simulation
function runPaging() {
    const pages = document.getElementById('page-string').value;
    const frames = document.getElementById('frame-count').value;
    const algo = document.getElementById('algo-select').value;
    
    const outputDiv = document.getElementById('paging-output');
    outputDiv.innerHTML = '<p>Loading...</p>';

    fetch('/api/paging', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pages: pages, frames: frames, algo: algo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let html = `<h3>Results for ${algo}</h3>`;
            html += `<p>Total Page Faults: <strong>${data.faults}</strong></p>`;
            html += `<hr>`;
            
            // Loop through each step to display frames
            data.steps.forEach(step => {
                let framesHtml = '';
                
                // Draw frames as simple boxes
                for (let i = 0; i < frames; i++) {
                    const val = step.frames[i] !== undefined ? step.frames[i] : '-';
                    framesHtml += `<div class="frame-box">${val}</div>`;
                }
                
                const faultHtml = step.fault ? `<span class="fault-indicator fault-text">Page Fault</span>` : '';
                
                html += `
                    <div class="paging-step">
                        <div class="page-ref">P: ${step.page}</div>
                        <div class="frames-container">
                            ${framesHtml}
                        </div>
                        ${faultHtml}
                    </div>
                `;
            });
            
            outputDiv.innerHTML = html;
        } else {
            outputDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    })
    .catch(error => {
        outputDiv.innerHTML = `<p style="color: red;">Failed to fetch data.</p>`;
    });
}

// Function to handle Segmentation
function runSegmentation() {
    const segBase = document.getElementById('seg-base').value;
    const segLimit = document.getElementById('seg-limit').value;
    
    const logSeg = document.getElementById('logical-seg').value;
    const logOffset = document.getElementById('logical-offset').value;
    
    const outputDiv = document.getElementById('segmentation-output');
    
    const payload = {
        segments: [
            { id: 0, base: segBase, limit: segLimit }
        ],
        logical_address: {
            segment: logSeg,
            offset: logOffset
        }
    };

    fetch('/api/segmentation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            outputDiv.innerHTML = `<p><strong>Result:</strong> ${data.result}</p>`;
        } else {
            outputDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    })
    .catch(err => {
        outputDiv.innerHTML = `<p style="color: red;">Failed to calculate address.</p>`;
    });
}

// Function to handle Virtual Memory
function runVirtualMemory() {
    const vPages = document.getElementById('vm-virtual').value;
    const pFrames = document.getElementById('vm-physical').value;
    const processPages = document.getElementById('vm-process').value;
    
    const outputDiv = document.getElementById('vm-output');

    fetch('/api/virtual_memory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            virtual_pages: vPages,
            physical_frames: pFrames,
            process_pages: processPages
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Replace newlines with <br> for HTML display
            const formattedExplanation = data.explanation.replace(/\\n/g, '<br>');
            outputDiv.innerHTML = `<p>${formattedExplanation}</p>`;
        } else {
            outputDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    })
    .catch(err => {
        outputDiv.innerHTML = `<p style="color: red;">Failed to simulate virtual memory.</p>`;
    });
}
