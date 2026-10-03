# myCloud Work Log

A concise record of the work completed for the myCloud project, including implementation, deployment, configuration, fixes, and final project state.

## 1. Application Development

1. Created the Flask-based myCloud personal cloud application.
2. Set up the Flask project structure and application configuration.
3. Implemented file upload functionality.
4. Implemented My Files / file listing.
5. Implemented file preview.
6. Implemented file download.
7. Implemented file deletion, including bulk deletion.
8. Added automatic filename conflict handling.
9. Added SQLite database with Flask-SQLAlchemy.
10. Created `User` model.
11. Created `File` model with user ownership.
12. Implemented user registration.
13. Implemented login and logout.
14. Added session-based authentication.
15. Added `login_required` protection to authenticated routes.
16. Added Werkzeug password hashing.
17. Added `.env` support for secrets.
18. Disabled Flask debug mode for production.
19. Added dynamic storage calculation using filesystem usage.
20. Added logged-in username display.
21. Redesigned the home/dashboard interface.
22. Updated login/register/upload/files pages to use the shared UI.
23. Added responsive/shared navigation styling.
24. Tested existing upload, delete, login, registration, and file-management functionality after UI changes.

## 2. Dockerization

1. Created `Dockerfile`.
2. Containerized the Flask application.
3. Created `compose.yaml`.
4. Added Docker named volume for SQLite data.
5. Added Docker named volume for uploaded files.
6. Verified data/uploads persist across normal container recreation.
7. Added `.dockerignore`.
8. Removed Gunicorn from the project as it was not required for this learning project.
9. Verified the application with Docker Compose locally.
10. Used the Compose service name `mycloud` for container commands.

## 3. AWS Deployment

1. Created an AWS EC2 server for myCloud.
2. Used AWS Sydney region (`ap-southeast-2`).
3. Deployed on a `t3.micro`.
4. Used Ubuntu 26.04 LTS.
5. Configured an 8 GiB gp3 root volume.
6. Installed Docker Engine.
7. Installed Docker Compose.
8. Added the EC2 user to the Docker group.
9. Tested Docker with `hello-world`.
10. Cloned the GitHub repository onto EC2.
11. Created a production `.env` with a server-side secret.
12. Built and started the application with Docker Compose.
13. Verified Flask locally on EC2 through port 5000.
14. Checked disk usage and Docker storage usage.
15. Confirmed the majority of disk usage came from the OS/server software rather than uploaded files.

## 4. Networking and Security

1. Created and configured the EC2 security group.
2. Restricted SSH port 22 to the user's IP.
3. Temporarily opened port 5000 for external testing.
4. Tested the application externally.
5. Later moved public access behind Nginx.
6. Removed the need for public application access through port 5000.
7. Kept HTTPS port 443 publicly accessible.
8. Removed duplicate/temporary security-group rules where applicable.
9. Kept Flask debug mode disabled in production.
10. Kept application secrets outside Git.

## 5. Domain and DNS

1. Created the DuckDNS domain:
   `mycloudnikk.duckdns.org`
2. Initially corrected the DuckDNS IP after it pointed to the wrong address.
3. Updated DuckDNS to the EC2 public IP.
4. Verified access through the domain from outside the local network.
5. Verified access using mobile data.

## 6. Nginx and HTTPS

1. Installed Nginx on EC2.
2. Configured Nginx as a reverse proxy to Flask on `127.0.0.1:5000`.
3. Configured the domain in Nginx.
4. Disabled the default Nginx site.
5. Tested the Nginx configuration.
6. Reloaded Nginx successfully.
7. Installed Certbot and the Nginx Certbot plugin.
8. Obtained a Let's Encrypt certificate.
9. Enabled HTTPS.
10. Verified the site through `https://mycloudnikk.duckdns.org`.
11. Verified HTTPS externally using mobile data.
12. Configured HTTP → HTTPS redirection.
13. Fixed the upload-size problem caused by Nginx's default 1 MB request-body limit.
14. Added `client_max_body_size 100M` to the HTTPS Nginx server block.
15. Verified 1 MB files upload correctly after the fix.

## 7. GitHub Actions / CI/CD

1. Created `.github/workflows/deploy.yml`.
2. Initially attempted SSH-based GitHub Actions deployment.
3. Generated a dedicated Ed25519 deployment key.
4. Added the public key to EC2.
5. Tested SSH access using the deployment key.
6. Created GitHub repository secrets for the SSH deployment approach.
7. Discovered the GitHub-hosted runner could not connect because SSH was restricted to the user's IP.
8. Switched to a self-hosted GitHub Actions runner on EC2.
9. Installed and configured the runner with label `mycloud-ec2`.
10. Changed the workflow to use:
    `runs-on: [self-hosted, linux, x64]`
11. Implemented automatic deployment on pushes to `main`.
12. Deployment runs:
    - `git pull origin main`
    - `docker compose up --build -d`
    - `docker compose ps`
13. Successfully tested the automated deployment.
14. Resolved a deployment failure caused by an uncommitted EC2 change to `run.py`.
15. Committed the production `debug=False` change to GitHub.
16. Restored/pulled the repository on EC2.
17. Verified subsequent deployments worked.
18. Identified that the old SSH deployment secrets are no longer required for the self-hosted runner approach.

## 8. Production UI / Frontend Work

1. Added shared responsive header/navigation.
2. Added username display to authenticated pages.
3. Added dynamic storage usage indicator.
4. Made storage usage come from actual filesystem statistics instead of a hardcoded value.
5. Added storage percentage/free-space display.
6. Redesigned the home page/dashboard.
7. Improved login page layout.
8. Improved registration page layout.
9. Updated upload page layout.
10. Updated files page layout.
11. Verified the updated frontend inside the running Docker container.
12. Diagnosed browser caching when the new UI initially did not appear.
13. Confirmed the new UI was correctly deployed and working.

## 9. 100 MB Upload Limit

### Committed application changes

1. Added Flask's request-size limit in `config.py`:

   `MAX_CONTENT_LENGTH = 100 * 1024 * 1024`

2. Verified the running container reports:

   `104857600`

3. Added browser-side JavaScript validation for files larger than 100 MB.
4. Disabled the upload button for oversized selected files.
5. Added a user-facing oversized-file message.
6. Added a Flask 413 error handler/page as server-side fallback.
7. Tested the limit with files above 100 MB.

### Non-Git server configuration

1. Initially added `client_max_body_size 100M` to the HTTP Nginx block.
2. Discovered HTTPS was using a different Nginx server block.
3. Diagnosed the issue using Nginx error logs.
4. Found the actual error:
   `client intended to send too large body`
5. Added `client_max_body_size 100M` to the HTTPS server block.
6. Reloaded Nginx.
7. Verified normal 1 MB uploads work.
8. Verified oversized uploads are blocked.

The Nginx configuration is a server-side change and is not stored in the GitHub repository.

## 10. Monitoring Decision

1. Reviewed AWS/CloudWatch monitoring options.
2. Checked EC2 metrics including CPU, network, and status metrics.
3. Decided not to add continuous CloudWatch alarms because myCloud is a small learning project and does not require 24/7 monitoring.
4. Kept the deployment simple and avoided unnecessary monitoring infrastructure.

## 11. Storage / Resource Checks

1. Checked EC2 root filesystem usage.
2. Confirmed approximately 6.7 GB usable root storage.
3. Checked Docker disk usage.
4. Checked Docker images, containers, volumes, and build cache.
5. Checked major `/var`, `/usr`, `/home`, and `/boot` usage.
6. Confirmed uploaded files currently consume very little storage.
7. Chose not to run destructive/unnecessary Docker cleanup commands.

## 12. Documentation

1. Replaced the old minimal `README.md` with a complete project README.
2. Documented:
   - Features
   - Tech stack
   - Project structure
   - Local setup
   - Configuration
   - Production architecture
   - CI/CD
   - Security
   - Learning outcomes
   - Project status
3. Created this `myCloudWork.md` as the detailed project work log.

## 13. Final Project State

1. Flask application complete.
2. Authentication complete.
3. File management complete.
4. SQLite database integrated.
5. Docker deployment complete.
6. AWS EC2 deployment complete.
7. Nginx reverse proxy complete.
8. HTTPS complete.
9. DuckDNS domain configured.
10. GitHub Actions self-hosted CI/CD complete.
11. Production UI complete.
12. 100 MB upload protection complete.
13. Dynamic storage display complete.
14. Basic production security configuration complete.
15. External HTTPS access verified.
16. Automated deployment verified.
17. Project documentation complete.
18. Monitoring intentionally kept minimal.
19. **Project status: COMPLETE.**
