# Team 7 – GreenCampus: Sustainability & Waste Management Tracker

**GreenCampus** is a full-featured, modular Django web application for university campuses to streamline waste reporting with photo evidence, organize student clean-up drives, track real-time recycling analytics via interactive Chart.js dashboards, and gamify student engagement through Eco-Points, badges, and rewards.

---

## 👥 3-Member Team Distribution & Scope

| Team Member | Module & Responsibilities | Key Components & Files |
| :--- | :--- | :--- |
| **Member 1** | **Waste Reporting & Photo Management**<br>• Waste submission form with photo upload & live preview<br>• Campus zone tagging (e.g. Cafeteria, Science Block, Hostels)<br>• Waste status workflow (`Pending` → `In Progress` → `Cleaned & Resolved`)<br>• Green Marshal / Admin verification with points reward | `reports/models.py`<br>`reports/views.py`<br>`reports/forms.py`<br>`templates/reports/` |
| **Member 2** | **Campaign & Event Management**<br>• Clean-up drives, e-waste rallies & tree plantation listings<br>• Event creation form with banner upload<br>• Volunteer RSVP system & live participant progress tracking<br>• Organizer attendance confirmation & points award | `events/models.py`<br>`events/views.py`<br>`events/forms.py`<br>`templates/events/` |
| **Member 3** | **Statistics Dashboard & Gamification Rewards**<br>• Real-time Chart.js graphs (Waste by category, monthly trend, campus hotspots)<br>• Environmental impact metrics (CO₂ saved kg, trees equivalent)<br>• University Leaderboard (Individual 🥇🥈🥉 podium, Department & Hostel ranks)<br>• Eco-Rewards store with redeemable campus vouchers | `analytics/models.py`<br>`analytics/views.py`<br>`static/js/charts.js`<br>`templates/analytics/` |

---

## 🌿 GitHub Branching Strategy & Workflow

To work smoothly across all 3 members without merge conflicts:

### 1. Initial Setup (One Team Member)
```bash
git init
git add .
git commit -m "Initial commit: GreenCampus full structure & core modules"
git branch -M main
git remote add origin https://github.com/<your-username>/GreenCampus.git
git push -u origin main

# Create the integration branch 'dev'
git checkout -b dev
git push -u origin dev
```

### 2. Member 1 (Waste Reporting)
```bash
# Clone the repository
git clone https://github.com/<your-username>/GreenCampus.git
cd GreenCampus

# Checkout and work on Member 1 branch
git checkout dev
git checkout -b feature/waste-reporting

# Work on reports app, then commit & push
git add reports/ templates/reports/
git commit -m "feat(reports): add image upload, status filter, and marshal verification"
git push -u origin feature/waste-reporting
# Open Pull Request on GitHub: feature/waste-reporting -> dev
```

### 3. Member 2 (Campaigns & Events)
```bash
# Clone the repository
git clone https://github.com/<your-username>/GreenCampus.git
cd GreenCampus

# Checkout and work on Member 2 branch
git checkout dev
git checkout -b feature/events-campaigns

# Work on events app, then commit & push
git add events/ templates/events/
git commit -m "feat(events): add campaign creation, banner upload, and RSVP tracking"
git push -u origin feature/events-campaigns
# Open Pull Request on GitHub: feature/events-campaigns -> dev
```

### 4. Member 3 (Analytics Dashboard & Rewards)
```bash
# Clone the repository
git clone https://github.com/<your-username>/GreenCampus.git
cd GreenCampus

# Checkout and work on Member 3 branch
git checkout dev
git checkout -b feature/analytics-rewards

# Work on analytics app, charts, and leaderboard, then commit & push
git add analytics/ templates/analytics/ static/js/charts.js
git commit -m "feat(analytics): add Chart.js interactive graphs, leaderboard, and rewards store"
git push -u origin feature/analytics-rewards
# Open Pull Request on GitHub: feature/analytics-rewards -> dev
```

### 5. Merging to Main (Release)
Once all 3 feature branches are reviewed and merged into `dev`:
```bash
git checkout main
git merge dev
git push origin main
```

---

## 🚀 Quickstart & Local Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Seed Initial Demo Data
Populates categories, demo waste reports with photos, upcoming campaigns, leaderboard ranks, and rewards:
```bash
python seed_data.py
```

### 4. Start Local Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser.

---

## 🔑 Demo Login Accounts

| Role | Username | Password | Permissions / Capabilities |
| :--- | :--- | :--- | :--- |
| **Sustainability Admin** | `admin` | `admin123` | Full admin access (`/admin/`), manage all modules, create campaigns |
| **Green Marshal (Staff)** | `marshal_alex` | `alex123` | Verify waste reports, upload clean photos, award points to students |
| **Student Eco-Champion** | `priya_sharma` | `student123` | Submit waste reports with photos, RSVP to campaigns, redeem vouchers |
| **Student** | `rahul_verma` | `student123` | Active student on leaderboard with earned badges |

---

## 🛠️ Tech Stack
- **Backend:** Python, Django 6.x, SQLite
- **File & Image Processing:** Pillow
- **Frontend:** Vanilla CSS (Modern glassmorphism & emerald design system), HTML5, JavaScript
- **Icons & Fonts:** FontAwesome 6, Google Fonts (Outfit & Plus Jakarta Sans)
- **Data Visualizations:** Chart.js 4 (Doughnut, Line, Bar, Pie charts)
