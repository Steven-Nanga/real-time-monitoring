# Real-Time Database Monitoring README

## Overview
This project implements a **real-time database monitoring system** designed to track and ensure data quality in a PostgreSQL database. The system uses modern technologies to capture and display changes in real time, providing actionable insights.

## Features
- **Real-time data quality monitoring** using PostgreSQL.
- **Change Data Capture (CDC)** enabled through **Debezium**.
- Scalable event streaming powered by **Kafka**.
- High-performance caching with **Redis** for recent changes.
- User-friendly **Flask dashboard** for visualization.

---

## Data Flow Explanation

### 1. Data Generation and Capture
- Users perform actions within the application (e.g., login, purchase, profile update).
- Actions are recorded in the PostgreSQL `user_activities` table.
- **Debezium** detects changes in real time using PostgreSQL's Write-Ahead Log (WAL).

---

### 2. Change Data Capture (CDC) Process
- **Debezium** extracts the change event from PostgreSQL.
- Each event contains:
  - Operation type (create, update, delete).
  - Before and after states of the record.
  - Metadata such as timestamps and transaction details.

---

### 3. Kafka Streaming
- Debezium sends these change events to a Kafka topic (`monitoring_server.public.user_activities`).
- Kafka ensures:
  - **Event ordering**.
  - **Fault tolerance** for failures.
  - **Scalable message distribution** for large data volumes.

---

### 4. Redis Caching
- The Flask application consumes Kafka messages and processes them.
- Processed events are cached in Redis for quick access:
  - `redis_client.lpush('recent_changes', json.dumps(change_event))`
  - Maintains a cache of the **last 100 events**.
- Redis delivers fast, in-memory storage for efficient data handling.

---

### 5. Dashboard Visualization
- The Flask-based dashboard combines:
  - Historical data from PostgreSQL.
  - Recent changes from Redis cache.
  - Real-time metrics and visualizations.

---

## Data Flow Visualization
```plaintext
User Action 
   ↓
Postgres Database 
   ↓ (Captured by Debezium)
Change Data Capture 
   ↓ (Streamed via Kafka)
Distributed Message Queue 
   ↓ (Consumed by Flask App)
Redis Cache & PostgreSQL 
   ↓
Real-Time Dashboard
```

---

## Key Benefits of This Architecture
- **Low-latency change tracking:** Immediate detection of database changes.
- **Scalable event processing:** Kafka supports large-scale data flows.
- **Decoupled components:** Easy to maintain and scale each part independently.
- **Real-time visibility:** Dashboards provide instant insights into data changes.
- **Fault-tolerant design:** Reliable data streaming and storage.

---

## Technologies Used
- **PostgreSQL**: Primary database for user activity records.
- **Debezium**: Captures real-time changes from PostgreSQL's WAL.
- **Kafka**: Streams change events reliably to the Flask application.
- **Redis**: Caches recent changes for fast data retrieval.
- **Flask**: Web framework for real-time dashboard visualization.

---

## How to Run
### Prerequisites
- Docker and Docker Compose (for containerized services).
- Python 3.x environment with required dependencies installed.

### Steps
1. **Set up the services:**
   ```bash
   docker-compose up -d
   ```
   This starts PostgreSQL, Kafka, Debezium, and Redis services.

2. **Run the Flask application:**
   ```bash
   python app.py
   ```

3. **Access the dashboard:**
   Open your browser and navigate to `http://localhost:5000`.

---

## Future Enhancements
- Add support for more databases (e.g., MySQL, MongoDB).
- Integrate advanced analytics for anomaly detection.
- Implement role-based access control for enhanced security.

---

This project demonstrates the power of real-time data monitoring and quality management through a modern, scalable architecture.
