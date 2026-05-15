# Portfolio Project

Microservices demo: order API (FastAPI), payment (gRPC), inventory and notification (Kafka consumers), plus Zookeeper/Kafka.

## Prerequisites

- Docker
- For Kubernetes: `kubectl` and a local cluster (e.g. [Rancher Desktop](https://docs.rancherdesktop.io/) or Docker Desktop with Kubernetes enabled)

## Endpoints

| Service | Protocol | Host (Compose) | Host (Kubernetes) | Notes |
|---------|----------|----------------|-------------------|-------|
| Order API | HTTP | `http://localhost:8000` | `http://localhost:30080` | Only service exposed outside the cluster |
| Health check | HTTP | `GET /health` | `GET /health` | Returns `{"status":"ok"}` |
| Create order | HTTP | `POST /order` | `POST /order` | Calls payment gRPC, publishes to Kafka |
| Payment | gRPC | `localhost:50051` | internal only | Not exposed in k8s |
| Kafka | TCP | `localhost:9092` | internal (`kafka-broker:9092`) | See k8s note below |
| Zookeeper | TCP | `localhost:2181` | internal | Infrastructure only |

### Example requests

```bash
# Docker Compose
curl http://localhost:8000/health
curl -X POST http://localhost:8000/order

# Kubernetes (NodePort)
curl http://localhost:30080/health
curl -X POST http://localhost:30080/order
```

---

## Run with Docker Compose

From the project root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Wait until all containers are up, then use the [endpoints](#endpoints) above on port **8000**.

### Run integration tests (Compose)

```bash
docker compose -f docker/docker-compose.yml run --rm tests
```

### Stop

```bash
docker compose -f docker/docker-compose.yml down
```

---

## Run with Kubernetes

Manifests live in [`k8s/`](k8s/). They deploy into the `portfolio` namespace.

### 1. Build images

From the project root:

```bash
./k8s/build-images.sh
```

On Rancher Desktop / Docker Desktop, images built with Docker are available to the cluster automatically (no `kind load` needed).

### 2. Apply manifests

```bash
kubectl apply -k k8s/
kubectl get pods -n portfolio -w
```

All pods should reach `1/1 Running`.

### 3. Call the API

Order service is exposed via **NodePort 30080**:

```bash
curl http://localhost:30080/health
curl -X POST http://localhost:30080/order
```

Alternative (any cluster):

```bash
kubectl port-forward -n portfolio svc/order-service 8000:8000
curl http://localhost:8000/health
```

### 4. Run integration tests (optional)

Uncomment `tests-job.yaml` in [`k8s/kustomization.yaml`](k8s/kustomization.yaml), ensure `portfolio/tests:latest` is built, then:

```bash
kubectl apply -k k8s/
kubectl logs -n portfolio job/portfolio-tests -f
```

### Stop / remove

```bash
kubectl delete -k k8s/
```

### Kubernetes notes

- **Kafka service name** is `kafka-broker`, not `kafka`. A Service named `kafka` causes Kubernetes to inject `KAFKA_PORT`, which breaks the Confluent Kafka image.
- App configuration is in [`k8s/configmap.yaml`](k8s/configmap.yaml) (`KAFKA_BOOTSTRAP_SERVERS`, `PAYMENT_GRPC_TARGET`, etc.).
- If you previously deployed a Service named `kafka`, delete it before re-applying:  
  `kubectl delete svc kafka -n portfolio`

---

## Local development (single service)

Run only the order service on your machine (requires Kafka and payment service elsewhere, or mocks):

```bash
cd services/order_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Default env vars match Docker Compose hostnames (`kafka:9092`, `payment_service:50051`). Override as needed:

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export PAYMENT_GRPC_TARGET=localhost:50051
```

---

## Architecture

See [docs/architecture.md](docs/architecture.md).
