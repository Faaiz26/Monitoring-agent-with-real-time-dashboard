from flask import Flask, Response

from prometheus_client import Gauge, generate_latest, REGISTRY

from metrics import collect_system_metric

from flask import jsonify

import threading
import time
from metrics import collect_all_metrics
from sql import insert_metrics  # assuming insert_metrics saves to DB

import pandas as pd
import plotly.graph_objs as go
import plotly
import json
import sqlite3
from flask import Flask, render_template_string, jsonify



log_file_path = "D:/SRE-Projects/venv/test.log"

app = Flask(__name__)

#create Prometheus gauges

cpu_gauge = Gauge('system_cpu_percent', 'System CPU usage  Percent')
memory_gauge = Gauge('systme_memory_percent', 'System Memory usage Percent')
disk_gauge = Gauge('system_disk_percent', 'System Disk usgage Percent')

@app.route('/metrics')

def metrics():
    metrics = collect_system_metric()
    cpu_gauge.set(metrics['cpu_percent'])
    memory_gauge.set(metrics['memory_percent'])
    disk_gauge.set(metrics['disk_percent'])
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

@app.route('/health')

def health():
    try:
        metrics = collect_system_metric()
        if metrics is None:
            return jsonify(status="DOWN"),500
        return jsonify(status='UP'),200
    except Exception as e:
        return jsonify(status="Down"),500
    
def periodic_collection(interval=60):
    while True:
        metrics = collect_all_metrics(log_file_path)
        insert_metrics(metrics)
        print(f"Metrics recorded at {time.ctime()}: {metrics}")
        time.sleep(interval)

# Start the background thread BEFORE starting Flask or other long-running service
thread = threading.Thread(target=periodic_collection, args=(60,), daemon=True)
thread.start()

def fetch_metrics():
    conn = sqlite3.connect('metric.db')
    df = pd.read_sql_query("SELECT * FROM system_metrics ORDER BY timestamp", conn)
    conn.close()
    return df

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <title>Real Time Metrics Dashboard</title>
        <!-- Fixed CDN path -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h2>System Metrics Over Time (Real-Time)</h2>
        <div id="metric-chart" style="width:100%; height:500px;"></div>
        <script>
            async function fetchDataAndPlot(){
                let response = await fetch('/chart-data');
                let figString = await response.text();  // get as text, not json
                let fig = JSON.parse(figString);        // parse to JS object
                Plotly.newPlot('metric-chart', fig.data, fig.layout);  // fixed Plotly
            }

            // Initial plot
            fetchDataAndPlot();
            // Update every 60 seconds
            setInterval(fetchDataAndPlot, 60000);
        </script>
    </body>
    </html>
    ''')


@app.route('/chart-data')

def chart_data():
    df = fetch_metrics()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['cpu_percent'], mode='lines+markers', name='CPU %'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['memory_percent'], mode='lines+markers', name='Memory %'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['disk_percent'], mode='lines+markers', name='Disk %'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['log_error_count'], mode='lines+markers', name='Log Error Count', yaxis='y2'))

    fig.update_layout(
        title='System Metrics Real-Time',
        xaxis_title='Timestamp',
        yaxis=dict(title='Percent / Count'),
        legend=dict(orientation='h'),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return plotly.io.to_json(fig)
    

if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=8000)

