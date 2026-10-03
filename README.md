# myCloud

A lightweight personal cloud storage application built with **Flask**, **SQLite**, **Docker**, and **Nginx**.

myCloud was built as a hands-on learning project to explore web development, authentication, databases, containers, Linux server administration, HTTPS, AWS, and CI/CD.

## Features

- User registration and login
- Password hashing with Werkzeug
- Session-based authentication
- File upload
- 100 MB maximum upload size
- Automatic filename conflict handling
- File listing
- File preview
- File download
- Bulk file deletion
- Per-user file ownership
- Dynamic server storage indicator
- Logged-in username display
- Responsive web interface
- Persistent SQLite database and uploads through Docker volumes
- HTTPS with Let's Encrypt
- Nginx reverse proxy
- Automatic deployment through GitHub Actions
- Self-hosted GitHub Actions runner on AWS EC2

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite, Flask-SQLAlchemy |
| Authentication | Flask Sessions, Werkzeug |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Containerization | Docker, Docker Compose |
| Web Server | Nginx |
| HTTPS | Let's Encrypt / Certbot |
| Hosting | AWS EC2 |
| CI/CD | GitHub Actions |
| Version Control | Git / GitHub |

## Project Structure

```text
myCloud/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── app/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
├── config.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── run.py
└── ...
```

## Running Locally

### Requirements

- Python 3.12+
- Docker Desktop
- Git

### Docker Compose

Clone the repository:

```bash
git clone https://github.com/nikunjmundhra/myCloud.git
cd myCloud
```

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
```

Start the application:

```bash
docker compose up --build -d
```

The application will be available at:

```text
http://localhost:5000
```

Stop it with:

```bash
docker compose down
```

Docker named volumes are used to persist the SQLite database and uploaded files.

## Configuration

Application configuration is stored in `config.py`.

The application enforces a 100 MB upload limit:

```python
MAX_CONTENT_LENGTH = 100 * 1024 * 1024
```

The upload page also performs a browser-side size check so oversized files are rejected before the upload begins.

Nginx is configured with a matching request-body limit in production.

## Production Architecture

The production deployment runs on AWS EC2:

```text
Internet
    │
    │ HTTPS :443
    ▼
  Nginx
    │
    │ reverse proxy
    ▼
Flask Container :5000
    │
    ├── SQLite Database
    │
    └── Uploaded Files
```

Docker Compose provides persistent volumes for:

- SQLite database
- Uploaded files

Nginx handles:

- HTTP → HTTPS redirection
- TLS termination
- Reverse proxying to Flask
- Upload request-size handling

Let's Encrypt provides the HTTPS certificate.

## CI/CD

GitHub Actions is configured with a self-hosted runner on the EC2 server.

Pushing to the `main` branch triggers deployment:

```text
git push
    │
    ▼
GitHub Actions
    │
    ▼
Self-hosted EC2 Runner
    │
    ├── git pull
    ├── docker compose up --build -d
    └── docker compose ps
```

This allows the production server to automatically rebuild and restart the application after changes are pushed to GitHub.

## Security

- Secrets are stored using environment variables.
- Passwords are hashed using Werkzeug.
- SSH access is restricted.
- Flask debug mode is disabled in production.
- HTTPS is enabled.
- Port 5000 is kept behind Nginx.
- Uploaded files are excluded from Git.
- SQLite data is stored in a persistent Docker volume.

## What I Learned

This project was built to learn how a web application works from development through production deployment.

Key areas covered:

- Flask application structure
- HTTP and file uploads
- Authentication and sessions
- Password hashing
- SQLAlchemy and SQLite
- Docker and Docker Compose
- Persistent Docker volumes
- Linux server administration
- AWS EC2
- Nginx reverse proxy
- HTTPS and TLS
- DNS
- GitHub Actions
- Self-hosted CI/CD
- Production configuration
- Basic cloud deployment

## Project Status

**Complete**

myCloud is deployed as a functional personal cloud storage server.

Built by **Nikunj Mundhra**.
