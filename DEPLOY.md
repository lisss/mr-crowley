# Deployment

## Fly.io

1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
2. Set secrets:
   ```bash
   flyctl secrets set REDIS_HOST=your-host REDIS_PASSWORD=your-password
   ```
3. Deploy: `flyctl deploy`

Auto-deploys on push to `main` via GitHub Actions.
