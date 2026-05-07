from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/paging', methods=['POST'])
def paging_simulation():
    data = request.json
    try:
        pages = [int(x.strip()) for x in data.get('pages', '').split(',')]
        frames_count = int(data.get('frames', 3))
        algo = data.get('algo', 'FIFO')
        
        frames = []
        faults = 0
        steps = []
        
        if algo == 'FIFO':
            queue = []
            for page in pages:
                fault = False
                if page not in frames:
                    fault = True
                    faults += 1
                    if len(frames) < frames_count:
                        frames.append(page)
                        queue.append(page)
                    else:
                        # replace oldest
                        oldest = queue.pop(0)
                        idx = frames.index(oldest)
                        frames[idx] = page
                        queue.append(page)
                
                steps.append({
                    'page': page,
                    'frames': list(frames),
                    'fault': fault
                })
                
        elif algo == 'LRU':
            recent = []
            for page in pages:
                fault = False
                if page not in frames:
                    fault = True
                    faults += 1
                    if len(frames) < frames_count:
                        frames.append(page)
                        recent.append(page)
                    else:
                        # find least recently used
                        lru_page = recent[0]
                        idx = frames.index(lru_page)
                        frames[idx] = page
                        recent.pop(0)
                        recent.append(page)
                else:
                    # update recently used
                    recent.remove(page)
                    recent.append(page)
                
                steps.append({
                    'page': page,
                    'frames': list(frames),
                    'fault': fault
                })
                
        return jsonify({'success': True, 'steps': steps, 'faults': faults})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/segmentation', methods=['POST'])
def segmentation_simulation():
    data = request.json
    try:
        # Example segments: [{id: 0, base: 1000, limit: 500}, ...]
        segments = data.get('segments', [])
        logical_address = data.get('logical_address', {})
        
        seg_id = int(logical_address.get('segment', 0))
        offset = int(logical_address.get('offset', 0))
        
        # find segment
        target_seg = None
        for seg in segments:
            if int(seg.get('id', -1)) == seg_id:
                target_seg = seg
                break
                
        if not target_seg:
            return jsonify({'success': False, 'error': 'Segment not found'})
            
        base = int(target_seg.get('base', 0))
        limit = int(target_seg.get('limit', 0))
        
        if offset >= limit:
            return jsonify({'success': True, 'result': 'Trap: Addressing Error (Offset > Limit)'})
            
        physical_addr = base + offset
        return jsonify({'success': True, 'result': f'Physical Address = {base} + {offset} = {physical_addr}'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/virtual_memory', methods=['POST'])
def virtual_memory_simulation():
    data = request.json
    try:
        # Simulating basic virtual memory concepts
        # total virtual pages, physical frames, and current process size
        total_virtual = int(data.get('virtual_pages', 10))
        total_physical = int(data.get('physical_frames', 4))
        process_pages = int(data.get('process_pages', 6))
        
        if process_pages > total_virtual:
            return jsonify({'success': False, 'error': 'Process exceeds virtual memory limits'})
            
        allocated_frames = min(process_pages, total_physical)
        pages_on_disk = process_pages - allocated_frames
        
        explanation = f"Process requires {process_pages} pages.\\n"
        explanation += f"Physical Memory has {total_physical} frames.\\n"
        explanation += f"Allocated {allocated_frames} pages in physical memory.\\n"
        if pages_on_disk > 0:
            explanation += f"{pages_on_disk} pages are stored on disk (swap space).\\n"
            explanation += "Page replacement will occur when these pages are accessed."
        else:
            explanation += "All pages fit in physical memory."
            
        return jsonify({'success': True, 'explanation': explanation})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
