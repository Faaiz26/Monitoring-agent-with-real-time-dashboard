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

