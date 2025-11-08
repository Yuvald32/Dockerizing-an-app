# Smart-Link Flask Application

## Overview
This is a Flask-based Smart-Link application for Dana Maram's song "מה אם?". It serves as a central landing page showcasing the song across multiple streaming platforms.

## What Has Been Implemented
- ✅ Flask web application with dynamic routing
- ✅ YAML-based configuration (`links.yaml`) for easy content management
- ✅ Responsive HTML templates with RTL (Hebrew) support
- ✅ Embedded Spotify and YouTube players
- ✅ Health check endpoint (`/healthz`) for Kubernetes probes
- ✅ Gunicorn WSGI server for production deployment
- ✅ Timezone support (Asia/Jerusalem)
- ✅ Non-root user security (appuser)

## Technology Stack
- **Python 3.13**
- **Flask 3.0.0** - Web framework
- **Gunicorn 22.0.0** - WSGI HTTP Server
- **PyYAML 6.0.2** - Configuration management
- **boto3 1.34.153** - AWS SDK (for future AWS integration)

## Project Structure
app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── links.yaml          # Configuration for links and embeds
├── static/
│   └── styles.css      # Styling
└── templates/
├── base.html       # Base template
└── index.html      # Main page template

## How to Run Locally

### Prerequisites
- Python 3.13+
- pip

### Steps
```bash
# 1. Navigate to app directory
cd app/

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser
# Visit: http://localhost:5001
```

## How to Run with Docker
```bash
# From project root
docker build -t smartlink:latest .
docker run -p 5001:5001 smartlink:latest

# Access at: http://localhost:5001
```

## Environment Variables
- `TZ` - Timezone (default: Asia/Jerusalem)

## Health Check
The application provides a health check endpoint:
```bash
curl http://localhost:5001/healthz
# Response: {"status": "ok"}
```

## Blockers
None currently. Application is fully functional for its intended purpose.

## Testing
```bash
# Test health endpoint
curl http://localhost:5001/healthz

# Test main page
curl http://localhost:5001/
```

## Notes
- Application approved by instructor as valid Flask project alternative
- Focuses on real-world use case (music industry smart-link)
- Demonstrates containerization and cloud-native practices
