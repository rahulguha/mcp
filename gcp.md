This document will capture necessary commands and settings to deploy apis and mcp servers to Google Cloud

## General

### Set project context

```
gcloud config set project mcp-playground-460722
```

#### Enable Cloud Run Service

```
gcloud services enable run.googleapis.com \
                       artifactregistry.googleapis.com \
                       cloudbuild.googleapis.com
```

##### Enable gcr

```
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### APIs

#### School List API

##### Local Build

```
docker build -f dockerfile.local -t school-list-api:1.0.0 .
```

##### GCP Build

```
docker build -f dockerfile.local -t school-list-api:1.0.0 .
```

##### TAG and Push

```
docker tag school-list-api:1.0.0 us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-list-api:1.0.0
docker push us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-list-api:1.0.0
```

##### Deploy Cloud Run App

```
gcloud run deploy school-list-api \
    --image us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-list-api:1.0.0 \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
# This should match the default or expected port of your Go app
```

#### School RAG API

##### LOCAL Build

```
docker build -f dockerfile.local -t gcp-school-rag-api:1.0.0 .
```

##### platform specific build for deployment to GCP

```
docker buildx build -f dockerfile.gcp --platform linux/amd64 --no-cache -t school-rag-api-gcp:1.0.0 . --load
```

##### TAG and Push

```
docker tag school-rag-api-gcp:1.0.0 us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-rag-api-gcp:1.0.0
docker push us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-rag-api-gcp:1.0.0
```

##### Deploy Cloud Run App

```
gcloud run deploy school-rag-api-gcp \
    --image us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-rag-api-gcp:1.0.0 \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
```

### MCP Server

##### Local

```
docker build  -t school-mcp-servers:1.0.0.0 .
```

##### GCP

```
docker build --platform linux/amd64 --no-cache  -t school-mcp-servers-linux:1.0.0.0 .
```

##### Tag and Push

```
docker tag school-mcp-servers-linux:1.0.0.0 us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-mcp-servers:1.0.0.0
docker push us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-mcp-servers:1.0.0.0
```

##### Deploy Cloud Run App

```
gcloud run deploy school-mcp-server \
    --image us-central1-docker.pkg.dev/mcp-playground-460722/mcp-school/school-mcp-servers:1.0.0.0 \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
```
