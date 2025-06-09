# Real-Time Quiz Participation – WebSocket Server

This project implements the **WebSocket Quiz Server** for real-time quiz participation. Users can join quiz sessions using a unique quiz ID and interact instantly through a WebSocket connection.

## Focus

**This repository only covers the WebSocket Quiz Server.**  
- There is no database this implementation.  
- Metrics are pushed directly to a Prometheus server for observability.
- Code style: follow flake8.


## System Requirements

- Docker
- Docker Compose

## Documentation

Project documentation is available in the documentations/ directory at the root of this repository, including:

- HighLevel Design: `documentations/high_level_design.md`
- HighLevel Design - Component Description: `documentations/highlevel_design_components.md`
- DataFlow: `documentations/data_flow.md`
- Technical Justification: `documentations/technical_justification.md`

## Quick start
Start the server with:
```bash
docker-compose up
```

- The WebSocket server runs on port **8000**
- The Prometheus server runs on port **8001**

## Run test
- This project uses Locust for load and performance testing of the WebSocket Quiz Server. 
Locust simulates multiple users joining quiz sessions and submitting answers over WebSocket connections, 
helping evaluate server performance and stability under concurrent load.
- Test script in folder: `test/`
- Install libraries: ```bash pip install -r requirements.txt```
- Start test:
```bash ./start.sh ```
Open the Locust web interface at http://localhost:8089 to configure and launch test scenarios.



## Monitoring

The server pushes internal metrics to Prometheus. Use Prometheus (or Grafana) to visualize and create alerts for these metrics.

---
