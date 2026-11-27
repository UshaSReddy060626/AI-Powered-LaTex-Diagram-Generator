#!/usr/bin/env bash
# Usage: ./deploy_ibmcloud.sh   (run from the project folder; needs a filled-in .env)
set -euo pipefail
REGION=${REGION:-us-south}
ibmcloud login --sso -r "$REGION"
ibmcloud plugin install code-engine -f
ibmcloud ce project create --name tikz-agent-project || ibmcloud ce project select --name tikz-agent-project
# store credentials as a secret (never baked into the image)
ibmcloud ce secret delete --name watsonx-secrets -f 2>/dev/null || true
ibmcloud ce secret create --name watsonx-secrets --from-env-file .env
# build from source with the Dockerfile and deploy
ibmcloud ce application create --name tikz-agent \
  --build-source . --strategy dockerfile \
  --port 8501 --cpu 1 --memory 4G --min-scale 1 \
  --env-from-secret watsonx-secrets
ibmcloud ce application get --name tikz-agent --output url
