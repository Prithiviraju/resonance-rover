from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import time
import threading
import random

app = FastAPI(title="Resonance Rover - Acoustic TDR Edge Node")

DB_FILE = "ndrf_mission_log.db"

# --- 1. INDUSTRIAL DATABASE ARCHITECTURE ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Database schema matching the Acoustic TDR and Geophone Array specifications
    c.execute('''CREATE TABLE IF NOT EXISTS acoustic_telemetry
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp REAL, 
                  pulse_emitter_status TEXT, 
                  geophone_echo_delay_ms REAL, 
                  slam_map_confidence REAL, 
                  victim_signature_detected BOOLEAN)''')
    conn.commit()
    conn.close()

init_db()

# --- 2. EDGE COMPUTE SIMULATION (JETSON/RASPBERRY PI) ---
def hardware_ingestion_loop():
    """Background automation: Simulates the edge node processing acoustic delays offline"""
    while True:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Simulating data from the high output transducer and 4x seismic sensors
        emitter_status = "ACTIVE"
        echo_delay = round(random.uniform(12.0, 85.5), 2) # milliseconds
        slam_conf = round(random.uniform(88.0, 99.9), 1) # percentage
        
        # Simulating the detection of trapped human movement via ground vibrations
        victim_detected = random.choice([True, False, False, False, False, False]) 
        
        c.execute("INSERT INTO acoustic_telemetry (timestamp, pulse_emitter_status, geophone_echo_delay_ms, slam_map_confidence, victim_signature_detected) VALUES (?, ?, ?, ?, ?)",
                  (time.time(), emitter_status, echo_delay, slam_conf, victim_detected))
        conn.commit()
        conn.close()
        time.sleep(2.5)

threading.Thread(target=hardware_ingestion_loop, daemon=True).start()

# --- 3. API ENDPOINTS ---
@app.get("/api/v2/telemetry")
def get_latest_telemetry():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM acoustic_telemetry ORDER BY id DESC LIMIT 8")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "time": r[1], "pulse": r[2], "delay": r[3], "slam": r[4], "victim": r[5]} for r in rows]

# --- 4. PROFESSIONAL INDUSTRIAL GUI ---
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NDRF Resonance Rover Terminal</title>
        <style>
            body { background-color: #f4f4f9; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; }
            .header-panel { background-color: #1e3a5f; color: white; padding: 15px 30px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
            .header-panel h1 { margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 1px; }
            .specs { font-size: 12px; color: #a9c2df; text-align: right; }
            .specs p { margin: 2px 0; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
            th, td { border: 1px solid #ddd; padding: 12px 15px; text-align: center; }
            th { background-color: #e3e8ee; font-weight: 600; color: #1e3a5f; }
            .alert { background-color: #ffeaea; color: #d32f2f; font-weight: bold; border-left: 4px solid #d32f2f; }
            .safe { color: #2e7d32; font-weight: bold; }
            .db-status { color: #666; font-size: 14px; margin-top: 15px; font-weight: 500; }
        </style>
    </head>
    <body>
        <div class="header-panel">
            <div>
                <h1>Autonomous Sub-Surface Resonance Rover</h1>
                <p style="margin: 5px 0 0 0; color: #a9c2df;">Acoustic TDR Navigation & Extraction Terminal</p>
            </div>
            <div class="specs">
                <p><strong>CHASSIS:</strong> IP68 Omni-Directional Tracked</p>
                <p><strong>DIMENSIONS:</strong> 2850mm x 1600mm x 1250mm</p>
                <p><strong>MASS:</strong> ~450 kg | <strong>POWER:</strong> Hybrid</p>
            </div>
        </div>
        
        <div class="db-status">Logging Edge Node SLAM mapping and MEMS Geophone arrays to local database...</div>
        
        <table>
            <thead>
                <tr>
                    <th>Log ID</th><th>System Time</th><th>Acoustic Emitter</th><th>Geophone Echo Delay (ms)</th><th>Offline SLAM Confidence</th><th>Target Status</th>
                </tr>
            </thead>
            <tbody id="db-logs">
                <tr><td colspan="6">Initializing Edge Node Connection...</td></tr>
            </tbody>
        </table>
        
        <script>
            setInterval(() => {
                fetch('/api/v2/telemetry')
                .then(r => r.json())
                .then(data => {
                    let html = '';
                    data.forEach(row => {
                        let timeStr = new Date(row.time * 1000).toLocaleTimeString();
                        let rowClass = row.victim ? 'class="alert"' : '';
                        let scanStatus = row.victim 
                            ? `⚠ VICTIM VIBRATION SIGNATURE DETECTED` 
                            : `<span class="safe">SCANNING RUBBLE...</span>`;
                        
                        html += `<tr ${rowClass}>
                            <td>#${row.id}</td>
                            <td>${timeStr}</td>
                            <td>${row.pulse}</td>
                            <td>${row.delay.toFixed(2)} ms</td>
                            <td>${row.slam.toFixed(1)} %</td>
                            <td>${scanStatus}</td>
                        </tr>`;
                    });
                    document.getElementById('db-logs').innerHTML = html;
                });
            }, 1000);
        </script>
    </body>
    </html>
    """