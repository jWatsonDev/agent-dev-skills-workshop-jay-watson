#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
AGENT_RESOURCE_NAME="${AGENT_RESOURCE_NAME:-projects/825583847169/locations/us-central1/reasoningEngines/9188791846405406720}"
REGION="${REGION:-us-central1}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "No active project. Run: gcloud config set project <PROJECT_ID>" >&2
  exit 1
fi

echo "Project:  $PROJECT_ID"
echo "Region:   $REGION"
echo "Agent:    $AGENT_RESOURCE_NAME"
echo

PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')

echo "Granting Cloud Run's service account access to the deployed agent..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/aiplatform.user" \
  --quiet

echo
echo "Deploying to Cloud Run..."
gcloud run deploy readynow-web \
  --source "$(dirname "$0")" \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --allow-unauthenticated \
  --set-env-vars "AGENT_RESOURCE_NAME=${AGENT_RESOURCE_NAME}"
