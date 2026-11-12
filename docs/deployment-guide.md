# SYSTEM DEPLOYMENT & OPERATION GUIDE (PROTOTYPE HANDOVER)
## SMART CRM – MEKONG MOBILE (FLOW 05: SPARE PARTS INVENTORY SUBSYSTEM)

- **Track:** Software Engineering (`SE`)
- **Student Name:** Huynh Nguyen Bao Ngoc — **Student ID:** `2374802010339` | **Class:** `261_71ITGR40203_06`
- **Supervisor:** Dr. Nguyen Tri Hai — Faculty of Information Technology, Van Lang University
- **Repository:** https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git (Tag `v1.0`)

---

## 1. Environment Requirements

To ensure a seamless clean-room deployment on a newly formatted machine, verify that your environment satisfies the following minimum prerequisites:

| Resource / Tool | Minimum Specification | Recommended Specification | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11 64-bit, macOS 12+, or Ubuntu 20.04+ LTS | Ubuntu 22.04 LTS or Windows 11 Pro | Cross-platform Docker support |
| **Container Engine** | Docker Engine `20.10.x` & Docker Compose `v2.x` | Docker Desktop `4.25+` / Docker Compose `v2.24+` | Mandatory for single-command run |
| **Python Runtime** *(Optional for local dev)* | Python `3.11.x` (`3.11.5` tested) | Python `3.11.5` 64-bit | Managed automatically inside Docker |
| **RAM** | Minimum `4.0 GB` free RAM | `8.0 GB` RAM | For running app + MongoDB container |
| **Disk Space** | Minimum `3.0 GB` free disk space | `5.0 GB` SSD | For Docker images and volumes |
| **Network Ports** | Port `8000` (Web UI & REST API), Port `27017` (MongoDB) | Ports `8000` & `27017` must be available | Ensure no existing service occupies 8000 |

---

## 2. Step-by-Step Setup Guide (Clean-Room Test <= 2 Commands)

The prototype adheres strictly to Core Deliverable Criteria `C1`: the entire multi-container environment spins up with **no more than two commands**.

### Step 1: Copy Environment Template
```bash
cp .env.example .env
```

### Step 2: Build and Launch Multi-Container Infrastructure
```bash
docker compose up -d --build
```

*(That is all! Docker Compose will automatically build the FastAPI + Dark 3D SPA application image, initialize the MongoDB 7.0 container with healthchecks, and seed 40 spare parts and 75 inventory items automatically).*

---

## 3. Environment Variables Reference

All configurable parameters are centralized in `.env`. Never commit production secrets to Git.

| Variable Name | Description & Technical Role | Default / Sample Value | Mandatory? |
| :--- | :--- | :--- | :---: |
| `API_PORT` | HTTP port exposed by Uvicorn server for REST API and Web UI. | `8000` | Optional (defaults to 8000) |
| `MONGO_URI` | MongoDB connection URI string (Container bridge or Atlas cloud). | `mongodb://localhost:27017/mekong_mobile_l5` | Yes |
| `DB_NAME` | Primary database name for collections and indexes. | `mekong_mobile_l5` | Yes |
| `JWT_SECRET_KEY` | Cryptographic secret key used to sign and verify HMAC-SHA256 JWT tokens. | `mekong_mobile_secret_jwt_key_2026_cdtn01` | Yes |
| `DEFAULT_CENTER_ID` | Primary service branch identifier for District 1 location. | `L5-WH-890` | Yes |

---

## 4. Seed and Demonstration Data

The prototype comes pre-packaged with rich industrial demo fixtures (`seeds/001_seed_parts_demo.json`) to prevent an empty system upon startup:

- **Service Centers (`service_center`):** `2` branches (`L5-WH-890` - District 1, `L5-WH-891` - District 3).
- **Spare Parts Catalog (`part`):** `40` phone and laptop parts covering iPhone 13/14/15, Samsung Galaxy S23/S24, MacBook Air/Pro, and Xiaomi.
- **Physical Inventory Stock (`part_stock`):** `75` branch stock balance records with concurrency versions (`version: 1`).
- **Warranty Repair Tickets (`ticket`):** `5` tickets across `OPEN`, `IN_PROGRESS`, `COMPLETED`, and `CANCELLED` states.
- **Initial Audit Log (`part_transaction`):** `5` immutable historical transaction records.
- **Default User Accounts (`users`):** `5` active personnel across 3 distinct roles:
  - Technical Staff (`TECH_STAFF`): `kythuat.test@gmail.com` / Password: `Password123@`
  - Material Specialist (`MATERIAL_STAFF`): `vattu.test@gmail.com` / Password: `Password123@`
  - Inventory Manager (`MANAGER`): `quanlykho.test@gmail.com` / Password: `Password123@`

---

## 5. Verification Steps (How to Verify the System is Running Correctly)

Execute the following verification commands to ensure 100% operational integrity:

### 5.1. Inspect Container Health Status
```bash
docker compose ps
```
**Expected Output:** Both `mekong_crm_l5_app` and `mekong_crm_l5_mongodb` must display status `Up ... (healthy)`.

### 5.2. Perform Automated Healthcheck Probe
```bash
curl -s http://localhost:8000/health
```
**Expected Output:**
```json
{
  "status": "online",
  "service": "Smart CRM - Inventory Subsystem (L5)",
  "timestamp": "2026-10-25T21:40:00Z"
}
```

### 5.3. Access Web SPA User Interface in Browser
- Open your web browser and navigate to: `http://localhost:8000/`
- **Expected Visual Result:** The Dark 3D Elevation Portal renders with the title *"SMART CRM — MEKONG MOBILE | Chi nhánh: Quận 1"*. Login using `kythuat.test@gmail.com` / `Password123@` to access the Tech Staff Dashboard.

### 5.4. Execute Automated Test Suite Inside Container
```bash
docker compose exec app pytest tests/ -v
```
**Expected Output:**
```text
======================= 67 passed in 3.13s =======================
```

### 5.5. Test Idempotency (Re-running Seed)
```bash
docker compose exec app python seeds/seed.py
```
**Expected Output:** Exits with `0` errors; the database retains exactly 40 parts and 75 stock records without duplicating records.

---

## 6. Optional Cloud Deployment (Render.com) — Free Tier Bonus

As specified in Assignment 3 (Section 3.3 & Session 16 Guideline), deploying the prototype to a public cloud platform with free tier qualifies for up to **+1.0 bonus point**.

### 6.1. Platform Overview
- **Hosting Provider:** Render.com (Free Tier Web Service)
- **Runtime Options Supported:**
  1. *Native Python Web Service* (Recommended for fast cold starts): Render builds directly via `pip install -r requirements.txt` and executes `uvicorn src.app:app --host 0.0.0.0 --port $PORT`.
  2. *Docker Web Service*: Render builds and runs the container using the root `Dockerfile`.
- **Database Strategy:** The backend automatically leverages its resilient offline fallback memory cache (`seeds/001_seed_parts_demo.json` and `data/users_store.json`), allowing complete independent demonstration without requiring an external database cluster. Alternatively, a free MongoDB Atlas connection string can be supplied via `MONGO_URI`.

### 6.2. Step-by-Step Render Deployment Walkthrough
1. **Sign In & Connect GitHub:**
   - Log in to [Render Dashboard](https://dashboard.render.com/) with your GitHub account.
2. **Create New Web Service:**
   - Click **New +** $\rightarrow$ **Web Service**.
   - Select **Build and deploy from a Git repository** and grant access to repository: `https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5`.
3. **Configure Service Parameters:**
   - **Name:** `mekong-mobile-inventory` (or custom name)
   - **Region:** `Singapore` (optimal network latency for Southeast Asia / Vietnam)
   - **Branch:** `main`
   - **Root Directory:** *(leave blank)*
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free` (0.1 CPU, 512 MB RAM)
4. **Configure Environment Variables:**
   Under the **Environment Variables** tab, define:
   - `PYTHON_VERSION`: `3.11.5`
   - `JWT_SECRET_KEY`: `mekong_mobile_secret_jwt_key_2026_cdtn01`
   - `DEFAULT_CENTER_ID`: `L5-WH-890`
   - `DB_NAME`: `mekong_mobile_l5`
   - `API_PORT`: `8000`
   *(Optional)* `MONGO_URI`: MongoDB Atlas connection URI if connected to managed cloud database.
5. **Deploy & Verify:**
   - Click **Deploy Web Service**.
   - Deployment logs will display successful package installation and Uvicorn server startup.
   - Once deployment status changes to **Live**, open the public URL provided by Render: `https://<your-service-name>.onrender.com/`.
   - **Official Live Production URL for Assignment 3:** **https://cdtn01.onrender.com** *(Pre-deployed and tested with resilient seed fallback and Dark 3D SPA Portal for +1.0 bonus point consideration)*.

### 6.3. Free Tier Caveats & Best Practices
- **Auto-Sleep Behavior:** Render free tier instances spin down after 15 minutes of inactivity. The first HTTP request after spin-down may take 30-50 seconds to wake up the service.
- **Pre-evaluation Warmup:** Wake up the service by visiting the public URL 1-2 minutes prior to teacher grading.
- **Production Secret Isolation:** Real credentials must never be committed to git; use Render's Environment Variables dashboard for injection.
