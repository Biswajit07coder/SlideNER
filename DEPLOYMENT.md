# Complete Deployment Guide: Vercel & Docker Containerization

This guide provides step-by-step instructions for beginners on how to run your containerized Landslide Early Warning prototype and deploy it on **Vercel** with your **Student Domain**.

---

## 🎯 Architecture Summary

- **Frontend & Web Dashboard**: Hosted on **Vercel** under your **Student Domain** (`https://yourname.me`). Provides an interactive dashboard with live weather metrics, station maps, ML risk gauges, and historical simulations.
- **Backend API**: Python FastAPI with XGBoost ML model (`landslide_risk_model.json`), Open-Meteo weather integration, and SQLite storage.
- **Docker Container**: Fully containerized using `Dockerfile` and `docker-compose.yml` for 100% reproducible execution anywhere.

---

## 🚀 Part 1: How to Deploy on Vercel & Get Your Live URL (2 Minutes)

Vercel deploys directly from GitHub with zero server configuration.

### Step 1: Push your code to GitHub
Open your terminal in the project directory:
```bash
git push origin main
```
*(If you are pushing to your personal GitHub account, create a new repository on [github.com/new](https://github.com/new) and run:)*
```bash
git remote set-url origin https://github.com/<YOUR_GITHUB_USERNAME>/landslide-ai.git
git push -u origin main
```

### Step 2: Import into Vercel
1. Go to [https://vercel.com](https://vercel.com) and log in with your **GitHub account**.
2. Click the **"Add New..."** button (top right) ➔ Select **"Project"**.
3. Under **"Import Git Repository"**, find your `landslide-ai` repository and click **"Import"**.
4. Leave all settings at default:
   - **Framework Preset**: *Other*
   - **Root Directory**: `./`
5. Click **"Deploy"**.

Within 30–60 seconds, Vercel will build and give you an instant live URL (e.g., `https://landslide-ai.vercel.app`)!

---

## 🎓 Part 2: How to Connect Your Student Domain on Vercel

If you have a student domain (such as from the **GitHub Student Developer Pack** via Namecheap, Name.com, or `.edu`):

### 1. Add Domain in Vercel
1. In your Vercel Dashboard, open your deployed project.
2. Click **Settings** (top navigation tab) ➔ Click **Domains** (left sidebar).
3. In the input box, enter your student domain:
   - Example: `landslide.yourname.me` or `yourname.me`
4. Click **Add**.

### 2. Configure DNS Records in Your Domain Registrar (e.g. Namecheap)
Vercel will display the required DNS records (usually a `CNAME` or `A` record).
1. Log in to your domain registrar (where you registered the student domain, e.g. Namecheap).
2. Go to **Domain List** ➔ Click **Manage** next to your domain ➔ Go to **Advanced DNS**.
3. Add the records shown in Vercel:
   - **Type**: `CNAME Record`  
     **Host**: `landslide` (or `www` / `@`)  
     **Value**: `cname.vercel-dns.com`  
     **TTL**: `Automatic`
   - *(If using an apex domain like `yourname.me`, add an **A Record** with Host `@` pointing to `76.76.21.21`)*.
4. Save changes. Within 1–5 minutes, Vercel will automatically verify the domain, issue a **free SSL/HTTPS certificate**, and your prototype will be live at `https://your-student-domain.me`!

---

## 🐳 Part 3: Running the Backend in Docker (Containerization)

The prototype backend is packaged into a Docker container.

### Step 1: Ensure Docker Desktop is Running
Make sure Docker Desktop is open on your computer.

### Step 2: Build and Run with Docker Compose
From the project root, run:
```bash
docker compose up --build
```

### Step 3: Verify the Container is Running
Once started, the backend will be available at:
- **Health Check**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Web Dashboard**: Open `public/index.html` in your browser (or visit [http://localhost:8000/](http://localhost:8000/)).

To stop the container:
```bash
docker compose down
```

---

## ☁️ Part 4: Deploying the Docker Container to Cloud (Render / Railway)

If your assignment specifically asks for the Docker container itself to be hosted live in the cloud:

### Deploying to Render (Free Docker Web Service):
1. Go to [https://render.com](https://render.com) and sign up with GitHub.
2. Click **New +** ➔ Select **Web Service**.
3. Connect your GitHub repository (`landslide-ai`).
4. Set:
   - **Environment**: `Docker`
   - **Region**: Closest to you (e.g. Singapore or Frankfurt)
   - **Instance Type**: `Free`
5. Click **Deploy Web Service**.
6. Render will automatically build your `Dockerfile` and provide a public HTTPS URL (e.g. `https://landslide-backend.onrender.com`).
7. Enter this URL into your Vercel Web Dashboard's **Backend API Target** banner, and the Vercel frontend will immediately query your live cloud Docker container!

---

## 🧪 Part 5: Testing All Endpoints

You can test the prototype with standard `curl` commands or directly through the Web Dashboard UI:

### 1. Register a Location
```bash
curl -X POST http://localhost:8000/locations/register \
  -H "Content-Type: application/json" \
  -d '{"location_name": "Joshimath Station", "latitude": 30.5564, "longitude": 79.5663, "device_token": "demo_token"}'
```

### 2. Fetch Live Risk Assessment (Open-Meteo + XGBoost)
```bash
curl -X GET http://localhost:8000/risk/1
```

### 3. Check All Registered Locations
```bash
curl -X POST http://localhost:8000/risk/check-all
```

### 4. Run Historical Disaster Simulation (2011 Chamoli Disaster)
```bash
curl -X POST http://localhost:8000/simulate/4924 \
  -H "Content-Type: application/json" \
  -d '{"device_token": "demo_token"}'
```
