# 🚀 Oslo Planning Dashboard - Deployment Guide

## 🌐 **Share Your Web App Externally**

### **Option 1: Streamlit Cloud (Recommended - FREE)**

#### **Step 1: Prepare Repository**
```bash
# Create GitHub repository
git init
git add .
git commit -m "Oslo Planning Dashboard - Initial deployment"
git branch -M main
git remote add origin https://github.com/yourusername/oslo-planning-dashboard.git
git push -u origin main
```

#### **Step 2: Create requirements.txt**
```bash
# In your project directory
pip freeze > requirements.txt
```

#### **Step 3: Deploy to Streamlit Cloud**
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Choose main file: `oslo_standalone_implementation.py`
6. Click "Deploy"

**Result: Public URL like `https://oslo-planning-dashboard.streamlit.app`**

### **Option 2: Heroku (Professional)**

#### **Setup Files**
```bash
# Create Procfile
echo "web: streamlit run oslo_standalone_implementation.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Create runtime.txt
echo "python-3.11.7" > runtime.txt
```

#### **Deploy Commands**
```bash
heroku create oslo-planning-dashboard
git push heroku main
```

### **Option 3: Railway (Modern)**

#### **One-Command Deploy**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway link
railway up
```

### **Option 4: Local Network Sharing**

#### **Share on Local Network**
```bash
# Find your local IP
ipconfig getifaddr en0  # Mac
# or
hostname -I  # Linux

# Run with network access
streamlit run oslo_standalone_implementation.py --server.address=0.0.0.0 --server.port=8501
```

**Share URL: `http://YOUR_IP:8501`**

### **Option 5: ngrok (Instant Public Access)**

#### **Install and Setup**
```bash
# Install ngrok
brew install ngrok  # Mac
# or download from https://ngrok.com

# Make localhost public
ngrok http 8501
```

**Result: Public URL like `https://abc123.ngrok.io`**

## 📁 **Code Sharing Options**

### **Option 1: GitHub Repository**
```bash
# Create complete repository
git init
git add .
git commit -m "Oslo Planning Dashboard - Complete implementation"
git remote add origin https://github.com/yourusername/oslo-planning-dashboard.git
git push -u origin main
```

### **Option 2: Code Archive**
```bash
# Create deployment package
zip -r oslo-planning-dashboard.zip . -x "*.pyc" "__pycache__/*" ".git/*" "*.db"
```

### **Option 3: Docker Container**
```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "oslo_standalone_implementation.py", "--server.address=0.0.0.0"]
```

## 📊 **Demo Preparation**

### **Create Demo Data Package**
```python
# Export demo data for reviewers
import json
from oslo_standalone_implementation import OsloPlanningDatabase

# Create demo dataset
db = OsloPlanningDatabase()
demo_data = {
    'areas': db.get_oslo_areas().to_dict('records'),
    'documents': db.get_all_documents().to_dict('records'),
    'metadata': {
        'created': '2025-01-23',
        'version': '1.0',
        'description': 'Oslo Planning Dashboard Demo Data'
    }
}

with open('oslo_demo_data.json', 'w', encoding='utf-8') as f:
    json.dump(demo_data, f, indent=2, ensure_ascii=False)
```

### **Create Video Demo**
```bash
# Record screen demo
# Mac: QuickTime Player > File > New Screen Recording
# Windows: Windows Key + G
# Linux: OBS Studio or SimpleScreenRecorder

# Upload to:
# - YouTube (unlisted)
# - Loom
# - Vimeo
```

## 🎯 **Professional Presentation Package**

### **Create Presentation Materials**
```python
# Generate presentation screenshots
import os
from datetime import datetime

# Create presentation folder
os.makedirs('oslo_presentation', exist_ok=True)

# Copy key files
files_to_include = [
    'oslo_standalone_implementation.py',
    'oslo_enhanced_ui.py', 
    'oslo_factual_accuracy_report.md',
    'oslo_development_roadmap.md',
    'immediate_implementation_plan.md',
    'oslo_demo_data.json'
]

# Create README for reviewers
readme_content = f"""
# Oslo Planning Dashboard - Demo Review

## 🏛️ Overview
Professional municipal planning dashboard for Oslo kommune with real data integration.

## 🚀 Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `streamlit run oslo_standalone_implementation.py`
3. Access at: http://localhost:8501

## 📊 Features
- Interactive Oslo map with 15 official bydeler
- Real-time planning document analysis
- AI-powered document processing
- Professional Oslo kommune branding
- Mobile-responsive design

## 🎯 Key Highlights
- Real Oslo municipality data integration
- Factually accurate (15 bydeler, not 16)
- Professional graphics and UI/UX
- AI framework ready for expansion
- Production-ready architecture

## 📁 Files Overview
- `oslo_standalone_implementation.py` - Main application
- `oslo_enhanced_ui.py` - Professional styling
- `oslo_demo_data.json` - Sample data for testing
- `*_report.md` - Strategic analysis documents

## 🌐 Live Demo
[Insert your deployed URL here]

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

with open('oslo_presentation/README.md', 'w') as f:
    f.write(readme_content)
```

## 🔗 **Share Links Template**

### **Email Template for Reviewers**
```
Subject: Oslo Planning Dashboard - Demo Review

Hi [Name],

I'd like to share the Oslo Planning Dashboard we've developed - a professional municipal planning intelligence platform.

🌐 Live Demo: [Your deployed URL]
📁 Source Code: [GitHub repository URL]
📊 Documentation: [Link to presentation materials]

Key Features:
✅ Real Oslo municipality data (15 official bydeler)
✅ AI-powered document analysis
✅ Professional UI with Oslo branding
✅ Interactive planning map
✅ Production-ready architecture

The application demonstrates our capability to build professional municipal software and serves as the foundation for Norway's first AI regulatory analysis platform.

Please let me know your thoughts and if you'd like to discuss further.

Best regards,
[Your name]
```

## 📱 **Mobile-Friendly Sharing**

### **Create QR Code for Easy Access**
```python
import qrcode

# Create QR code for your deployed URL
def create_qr_code(url, filename='oslo_dashboard_qr.png'):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

# Usage
# create_qr_code("https://your-deployed-url.streamlit.app")
```

## ✅ **Recommended Approach**

### **For Quick Demo (Choose One):**
1. **ngrok** - Instant public access to localhost
2. **Streamlit Cloud** - Free permanent hosting
3. **GitHub + README** - Code review with documentation

### **For Professional Presentation:**
1. **Streamlit Cloud deployment** - Permanent public URL
2. **GitHub repository** - Complete code access
3. **Presentation package** - Screenshots, documentation, demo data
4. **Video demo** - 5-minute walkthrough

Would you like me to help you set up any of these deployment options?