# CI/CD Pipeline

## Stages
- Lint & Type Check (ruff, black, mypy)
- Unit Tests (pytest)
- Build Docker Images (dev, trt)
- SBOM & Security Scans (Trivy, pip-audit)
- Push to Registry
- Deploy to Staging (K8s)
- Manual Promotion to Prod

## Artifacts
- Docker images tagged with semver + git sha
- Model artifacts stored in object storage with checksums

## Notes
- Use GitHub Actions under `.github/workflows/ci.yml` (to be added) for automation.
