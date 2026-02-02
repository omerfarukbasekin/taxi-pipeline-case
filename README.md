# Taxi Pipeline Case Study

Comprehensive data pipeline solution for taxi trip management with Apache Airflow orchestration, FastAPI REST API, PostgreSQL database, and Kubernetes deployment.

## Project Architecture

```
├── airflow/              # Data orchestration and ETL pipeline
├── api/                  # REST API service (FastAPI)
├── sql/                  # Database schema and SQL queries
├── k8s/                  # Kubernetes deployment manifests
├── data/                 # Data storage (incoming, history, rejected)
└── utilities/            # Testing and validation screenshots
```

## Core Components

### 1. **Airflow DAG Pipeline** (`airflow/`)
Automated daily ETL pipeline that:
- **Monitors** incoming CSV files using FileSensor
- **Validates** CSV data structure and content via CSVValidator
- **Loads** validated data into PostgreSQL database
- **Archives** processed files to history directory
- **Rejects** invalid files to rejected directory

Key files:
- `dags/daily_dag.py` - Main DAG definition with task orchestration
- `validation/csv_validator.py` - Data validation logic
- `loader/postgres_loader.py` - Database loader implementation

### 2. **FastAPI REST API** (`api/`)
RESTful API service exposing endpoints for:
- **Drivers** - Driver information and analytics
- **Clients** - Client data management
- **Health** - Service health checks

Features:
- Docker containerization
- PostgreSQL integration
- Environment-based configuration
- Health check endpoints for Kubernetes liveness/readiness probes

### 3. **Database** (`sql/`)
PostgreSQL schema includes:

```sql
trips table:
- trip_id (PK)
- client_id (FK)
- driver_id (FK)
- trip_date (Indexed)
- status (done/not_respond)
```

Additional analytics queries:
- `driver_performance_report.sql` - Driver metrics and statistics
- `loyal_customer_analysis.sql` - Customer loyalty analysis

### 4. **Kubernetes Deployment** (`k8s/`)
Production-ready Kubernetes manifests:
- **deployment.yaml** - API deployment with health probes
- **service.yaml** - Service exposure configuration
- **secret.yaml** - PostgreSQL credentials management

## Setup & Running

### Prerequisites
```
- Docker & Docker Compose
- Kubernetes (minikube/kubectl)
- Python 3.8+
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### 1. Start PostgreSQL Database
```bash
cd sql
git bash ile start postgresql
chmod +x /start_postgres.sh
./start_postgres.sh # or bash start_postgres.sh
```
```bash
# To connect db
docker ps
docker exec -ti postgres psql -U postgres -d trips_db
```
```bash
# create table with sql/schema.sql
trips_db=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | trips | table | postgres
(1 row)

# To get server IP
docker exec -ti postgres bash
hostname -I
# 172.17.0.2 can be used for k8s secret
```

### 2. Start Airflow
```bash
cd airflow
docker compose build
docker compose up
# Access UI: http://localhost:8080

docker exec -ti airflow bash
airflow dags list
airflow webserver -p 8080

# Airflow User creation
airflow users create \
  --username .... \
  --password .... \
  --firstname .... \
  --lastname .... \
  --role Admin \
  --email ....

#   Airflow conn sets
airflow connections add postgres_trips \
  --conn-type ... \
  --conn-host ... \
  --conn-schema ... \
  --conn-login ... \
  --conn-password ... \
  --conn-port 5432
# or add screts docker-compose.yml or add conn_ids manully to airflow UI

#   conn_id fail for fs_conn_id
#   add  fs_default with conn_type fs to path </>
```

### 3. Deploy API to Kubernetes
```bash
# Build and load image
cd api
docker build -t trips-api .

kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Apply Kubernetes manifests
kubectl apply -f k8s/
kubectl port-forward svc/trips-api 8000:80
# API available: http://localhost:8000
```

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Drivers
```
GET /drivers
GET /drivers/{driver_id}
POST /drivers
```

### Clients
```
GET /clients
GET /clients/{client_id}
POST /clients
```

## Data Flow Pipeline

```
CSV File (incoming/)
    ↓
[Airflow FileSensor] → Detects new file
    ↓
[Validate Task] → CSVValidator checks data integrity
    ↓
[Load Task] → PostgresTripLoader inserts to DB
    ↓
[Archive Task] → Move to history/ OR rejected/
```

## Testing & Validation

Screenshots documenting API endpoints and functionality available in `utilities/`:

| Screenshot | Description |
|-----------|-------------|
| `health.png` | Health check endpoint test |
| `driver api.png` | Driver endpoints demonstration |
| `client api.png` | Client endpoints demonstration |
| `docks.png` | Docker & container setup |
| `utilities.png` | Testing utilities overview |

## Troubleshooting

### Airflow Tasks Fail
- Check logs: `kubectl logs -f deployment/airflow-webserver`
- Verify data path: `/data/incoming/output.csv` exists

### API Deployment Issues
- Verify secret exists: `kubectl get secrets postgres-secret`
- Check image: `docker images | grep trips-api`

### Kubernetes Connectivity
```bash
# Port forward
kubectl port-forward svc/trips-api 8000:80

# Check pod status
kubectl get pods -l app=trips-api
kubectl logs -f deployment/trips-api

# To update yaml files for all files
kubectl delete pod -l app=trips-api
# or
kubectl delete deployment trips-api

kubectl apply -f k8s/deployment.yaml

# To restrat pod 
kubectl rollout restart deployment trips-api
```

### Docker Virutal ENV errors
```bash
# wsl activate
# Hyper-V activation For Windows 11
# Windows + R write optionalfeatures
# select Hyper-V and restart
# PowerShell
wsl --install
wsl --set-default-version 2
# make sure activate vm from BIOS
```

## Technologies Used

- **Orchestration**: Apache Airflow
- **API Framework**: FastAPI
- **Database**: PostgreSQL
- **Container**: Docker
- **Orchestration**: Kubernetes
- **Language**: Python 3.8+
- **venv**: miniconda

---

**Last Updated**: February 2, 2026
