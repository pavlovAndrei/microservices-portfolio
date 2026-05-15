#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

docker build -t portfolio/payment-service:latest -f "$ROOT/services/payment_service/Dockerfile" "$ROOT"
docker build -t portfolio/order-service:latest -f "$ROOT/services/order_service/Dockerfile" "$ROOT"
docker build -t portfolio/inventory-service:latest -f "$ROOT/services/inventory_service/Dockerfile" "$ROOT"
docker build -t portfolio/notification-service:latest -f "$ROOT/services/notification_service/Dockerfile" "$ROOT"
docker build -t portfolio/tests:latest -f "$ROOT/tests/Dockerfile" "$ROOT"

echo "Images built."
echo ""
echo "Rancher Desktop / Docker Desktop: images are already visible to the cluster."
echo "  kubectl apply -k k8s/"
echo ""
echo "kind (if installed):"
echo "  kind load docker-image portfolio/order-service:latest"
echo ""
echo "minikube (if installed):"
echo "  minikube image load portfolio/order-service:latest"
