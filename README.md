# **DevPulse — Real-Time Tech Job Market Tracker**

**Live Demo:** [https://devpulse-job-tracker.onrender.com](https://devpulse-job-tracker.onrender.com/dashboard)

DevPulse is a full-stack data engineering application that tracks **real-time tech job market trends in South Africa**. It automates data ingestion, extracts in-demand technical skills using NLP (Regex), and visualizes insights on an interactive dashboard.

This isn’t just another job board. DevPulse analyzes job descriptions to reveal **what skills employers want right now** — Python, AWS, SQL, Azure, and many more.
<img width="1893" height="908" alt="image" src="https://github.com/user-attachments/assets/130f3565-3be0-422a-a822-c5e60edf651c" />




## 🚀 **Project Overview**

DevPulse combines **Data Engineering**, **ETL automation**, and **Full-Stack Web Development**:

* Fetches live job listings via the **Adzuna API**
* Cleans and normalizes raw data
* Extracts technical skills using Regex-based NLP
* Stores results in a relational database
* Serves an analytics dashboard through a Flask web app




## 🛠️ **Tech Stack & Architecture**

### **1. Data Engineering (ETL Pipeline)**

**Source:**

* Adzuna API — South Africa job categories (Software Engineering, Data Science, IT Support)

**Extract:**

* Python script pulls raw JSON from the API

**Transform:**

* **Pandas** for cleaning & normalization
* **BeautifulSoup** to remove HTML tags
* **Regex** to detect 20+ technical keywords

  * Example: `\bPython\b`, `\bAWS\b`, `\bAzure\b`

**Load:**

* SQLite / PostgreSQL
* Upsert logic prevents duplicates using unique job URL constraints




### **2. Software Engineering (Web Application)**

* **Backend:** Flask + Blueprints
* **Database:** SQLAlchemy ORM
* **Frontend:** Jinja2 + Bootstrap 5
* **Charts:** Chart.js
* **Deployment:** Render.com (Gunicorn)




## ✨ **Key Features**

* **Automated ETL Pipeline**
  Fetches and updates job data in the background.

* **Skill Extraction Engine**
  Detects in-demand skills from unstructured job descriptions.

* **Interactive Dashboard**
  View top skills, job stats, and recent listings.

* **Search & Filtering**
  Instantly filter by title, skill, or description.

* **Pipeline Status Monitor**
  Check logs of previous ingestion runs (success/failure).




## ⚙️ **Local Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/devpulse-job-tracker.git
cd devpulse-job-tracker
```

### **2. Create Virtual Environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key
ADZUNA_APP_ID=your_adzuna_id
ADZUNA_APP_KEY=your_adzuna_key
DATABASE_URL=sqlite:///devpulse.db
```

### **5. Initialize Database & Run Pipeline**

```bash
python run_pipeline.py
```

### **6. Start the Server**

```bash
python run.py
```

Visit: [http://127.0.0.1:5000](https://devpulse-job-tracker.onrender.com/dashboard)



## ☁️ **Deployment (Render)**

DevPulse runs on Render using Gunicorn.

**Build Command:**

```bash
pip install -r requirements.txt
```

**Start Command:**

```bash
gunicorn run:app --timeout 120
```

⚠️ **Free Tier Note:**
Render’s free tier resets file storage on redeploy.
A **Remote Pipeline Trigger** is included to repopulate data:

```
https://your-app-url.onrender.com/admin/run-pipeline
```




## 📬 **Contact**

**Ntokozo Ntombela**
Full Stack Developer & Data Engineer
GitHub: [ntokozo078](https://github.com/ntokozo078)
Linkedin: [Ntokozo ntombela](https://www.linkedin.com/in/ntokozo-ntombela-ba662235a)


