# Monitoring-agent-with-real-time-dashboard

# SRE Custom Monitoring Agent

This project implements a Python-based Site Reliability Engineering (SRE) monitoring agent that collects system metrics, stores them in an SQLite database, and provides a real-time interactive dashboard built with Flask and Plotly.

## Features

- Collects CPU, Memory, Disk, and Log Error Count metrics.
- Stores metrics persistently in SQLite database.
- Exposes Prometheus-compatible `/metrics` endpoint.
- Provides a Flask-based web dashboard at `/` with real-time Plotly charts.
- Background thread collects and inserts metrics at regular intervals.

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
4. Run the Flask app:

5. Access dashboard at `http://localhost:8000/`.

## Project Structure

- `app.py`: Main Flask application and metric scheduler.
- `metrics.py`: Functions for collecting system and log metrics.
- `sql.py`: Database interaction functions.
- `metric.db`: SQLite database file.
- `test.log`: Sample log file watched for error counts.

## Technologies Used

- Python 3
- Flask
- Plotly
- SQLite
- psutil

## License

MIT License


<img width="946" height="398" alt="image" src="https://github.com/user-attachments/assets/b2e37050-90e1-4294-9b21-1b57286aa1fc" />




