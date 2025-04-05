
# T2S Services – Work with Emmanuel (Deployed on Minikube using Helm & PostgreSQL)

This project shows how to deploy a full-stack web application using **Helm** and **Minikube**, where client form submissions are stored in a **PostgreSQL** database. The form is presented via an HTML frontend that promotes working with **Emmanuel Naweji**.

---

## Preview

**Landing Page Sample:**
-  “Work with Emmanuel” branding
-  Emmanuel’s picture
-  [Book a FREE consultation](https://here4you.setmore.com)

---

##  Project Layout

```
t2s-services/
├── index.html               # Frontend form with Emmanuel’s branding
├── backend/
│   └── app.py               # Flask API for form submission handling
├── Dockerfile               # Flask backend Docker image
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── postgres-deployment.yaml
│       └── postgres-service.yaml
```

---

##  Prerequisites

- Docker
- Minikube
- Helm
- kubectl
- PostgreSQL Client (optional, for debugging)

---

##  Step-by-Step Deployment Instructions

###  1. Start Minikube

```bash
minikube start
eval $(minikube docker-env)
```

>  Minikube gives us a local Kubernetes cluster for dev/testing.

---

###  2. Build the Flask Backend Image

**Dockerfile:**

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/app.py .
RUN pip install flask psycopg2
CMD ["python", "app.py"]
```

```bash
docker build -t t2s-web-app:1.0 .
```

>  This image handles POST requests from the HTML form and writes data to PostgreSQL.

---

###  3. Configure Helm Chart

#### Chart.yaml

```yaml
apiVersion: v2
name: t2s-services
description: T2S App with PostgreSQL using Helm
version: 0.1.0
```

#### values.yaml

```yaml
image:
  repository: t2s-web-app
  tag: "1.0"
  pullPolicy: IfNotPresent

service:
  type: NodePort
  port: 80
```

---

###  4. PostgreSQL Deployment

**postgres-deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: t2s-postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: t2s-postgres
  template:
    metadata:
      labels:
        app: t2s-postgres
    spec:
      containers:
        - name: postgres
          image: postgres:13
          env:
            - name: POSTGRES_DB
              value: "t2sdb"
            - name: POSTGRES_USER
              value: "t2suser"
            - name: POSTGRES_PASSWORD
              value: "t2spassword"
          ports:
            - containerPort: 5432
```

**postgres-service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: t2s-postgres
spec:
  selector:
    app: t2s-postgres
  ports:
    - port: 5432
```

---

###  5. Deploy Backend & PostgreSQL using Helm

```bash
helm install t2s-services ./helm-chart
```

---

###  6. Create the Table in PostgreSQL

```bash
kubectl exec -it deploy/t2s-postgres -- bash
psql -U t2suser -d t2sdb
```

Inside PostgreSQL shell:

```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT,
    service TEXT
);
```

---

###  7. Access the App

```bash
minikube service t2s-services --url
```

Open the URL in your browser to access the **Work with Emmanuel** form.

 Make sure your Flask app endpoint matches the frontend fetch URL (e.g. `/signup`).

---

###  Why These Steps Matter

| Step | Purpose |
|------|---------|
| Docker | Containerizes the backend logic |
| Flask | Handles POST request logic and DB connection |
| PostgreSQL | Stores submitted leads |
| Helm | Manages Kubernetes configuration declaratively |
| Minikube | Local dev environment to test the full setup |

---

###  Cleanup

```bash
helm uninstall t2s-services
minikube stop
```

---

##  Book a Free Consultation

 [Schedule with Emmanuel](https://here4you.setmore.com)

---


