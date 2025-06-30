# Identity Provider Demo

A Flask web application demonstrating Identity Provider (IdP) integration with Keycloak for Single Sign-On (SSO) authentication to demonstrate a secure, centralised IdP platform designed for organisations (schools, government, businesses) to manage student and teacher identities. The platform will serve as a trusted authentication and authorisation system, allowing users to seamlessly access various educational tools and services while ensuring compliance with privacy regulations and data residency laws.

⚠️ **This is a demo application with hardcoded secrets.** Do not use in production without:

- Using environment variables for secrets
- Implementing proper SSL/TLS
- Setting up secure cookie configurations
- Adding CSRF protection

## Features

- User registration and login via Keycloak
- OpenID Connect (OIDC) integration
- Session-based authentication with JWT tokens
- Form validation with WTForms
- Dockerized development environment

## Architecture

- **Flask Application**: Web server running on port 5000
- **Keycloak**: Identity provider running on port 7080
- **Docker Compose**: Orchestrates both services with health checks

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)

## Quick Start

1. Clone the repository:

   ```bash
   git clone git@github.com:Siyavula/idp-demo.git
   cd idp-demo
   ```

2. Start the services:

   ```bash
   docker-compose up --build
   ```

3. Wait for Keycloak to be healthy (check logs), then access:
   - Flask app: <http://localhost:5000>
   - Keycloak admin: <http://localhost:7080> (admin/admin)

## Development

### Local Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   flask --app app run --debug
   ```

### Configuration

The application auto-configures the Keycloak client on startup. Key settings in `app/__init__.py`:

- **SERVER_URL**: Keycloak server URL
- **CLIENT_ID**: OIDC client identifier
- **CLIENT_SECRET**: Client authentication secret
- **REALM_NAME**: Keycloak realm (default: master)

## Project Structure

```bash
app/
├── __init__.py          # Flask app factory
├── auth.py              # Authentication blueprint
├── home.py              # Home page blueprint
├── forms.py             # WTForms validation
├── utils.py             # Keycloak utility functions
├── models/
│   └── user.py          # User model with Keycloak integration
├── templates/           # Jinja2 templates
├── static/              # CSS and static assets
└── config/
    └── oid_client_config.json  # OIDC client configuration
```

## Authentication Flow

1. Users register/login through Flask forms
2. Credentials are validated against Keycloak
3. Successful authentication returns JWT tokens
4. Tokens are stored in session and cookies
5. Protected routes check for valid sessions
