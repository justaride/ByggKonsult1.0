# 🚀 Deployment Guide

## Oslo Planning Documents - Premium Deployment

This guide covers deployment options for the Oslo Planning Documents Premium application.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.7 or higher (Recommended: 3.9+)
- **Memory**: 512MB RAM minimum (1GB recommended)
- **Storage**: 100MB available space
- **Network**: Internet connection for link verification

### Dependencies
All dependencies are listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 🖥️ Local Deployment

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/oslo-planning-premium.git
cd oslo-planning-premium

# Install dependencies
pip install -r requirements.txt

# Launch application
./launch_oslo_premium.sh
```

### Manual Start
```bash
# Run directly with Python
streamlit run oslo_planning_premium.py --server.port 8503
```

### Development Mode
```bash
# Enable auto-reload for development
streamlit run oslo_planning_premium.py --server.runOnSave true --server.port 8503
```

## ☁️ Cloud Deployment

### Streamlit Cloud
1. **Fork the repository** on GitHub
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from your forked repository
3. **Configure settings**:
   - Main file: `oslo_planning_premium.py`
   - Python version: 3.9
   - Requirements: `requirements.txt`

### Heroku Deployment

1. **Create Heroku app**:
   ```bash
   heroku create oslo-planning-premium
   ```

2. **Add Procfile**:
   ```
   web: streamlit run oslo_planning_premium.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8503
   
   CMD ["streamlit", "run", "oslo_planning_premium.py", "--server.port=8503", "--server.address=0.0.0.0"]
   ```

2. **Build and run**:
   ```bash
   docker build -t oslo-planning-premium .
   docker run -p 8503:8503 oslo-planning-premium
   ```

### DigitalOcean App Platform

1. **Connect repository** to DigitalOcean App Platform
2. **Configure build settings**:
   - Build command: `pip install -r requirements.txt`
   - Run command: `streamlit run oslo_planning_premium.py --server.port=8080 --server.address=0.0.0.0`
3. **Set environment variables** (if needed)

## 🔧 Configuration

### Environment Variables
Create `.env` file for configuration:
```env
# Application settings
STREAMLIT_PORT=8503
DEBUG_MODE=false

# Database settings
DATABASE_PATH=oslo_planning_premium.db
BACKUP_ENABLED=true

# External services
OSLO_KOMMUNE_API_BASE=https://oslo.kommune.no
VERIFICATION_ENABLED=true
```

### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[server]
port = 8503
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1B4F72"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🔒 Security Configuration

### Production Security
- **HTTPS**: Always use HTTPS in production
- **Access Control**: Implement proper access controls if needed
- **Environment Variables**: Store sensitive data in environment variables
- **Regular Updates**: Keep dependencies updated

### Firewall Settings
- **Port 8503**: Allow inbound traffic on application port
- **HTTPS (443)**: Allow HTTPS traffic
- **HTTP (80)**: Redirect to HTTPS

## 📊 Performance Optimization

### Production Optimizations
```python
# In oslo_planning_premium.py, add caching
@st.cache_data(ttl=3600)
def load_documents():
    return system.get_all_documents()

@st.cache_resource
def init_database():
    return OsloPlanningPremium()
```

### Database Optimization
- **SQLite PRAGMA** settings for performance
- **Index optimization** for frequent queries
- **Connection pooling** for concurrent access

### Memory Management
- **Efficient data structures** using pandas
- **Lazy loading** of components
- **Garbage collection** optimization

## 🔍 Monitoring & Logging

### Application Monitoring
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
Create health check endpoint:
```python
def health_check():
    try:
        # Test database connection
        system = OsloPlanningPremium()
        docs = system.get_all_documents()
        return {"status": "healthy", "documents": len(docs)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 🧪 Testing Deployment

### Pre-deployment Testing
```bash
# Run tests
python -m pytest tests/

# Check requirements
pip check

# Validate application
python -c "from oslo_planning_premium import OsloPlanningPremium; print('✅ Import successful')"
```

### Post-deployment Verification
1. **Application Load**: Verify the application loads correctly
2. **Database Access**: Check database connectivity
3. **URL Verification**: Test document link validation
4. **Performance**: Monitor load times and responsiveness

## 📱 Mobile Optimization

### Responsive Design
The application is optimized for mobile devices with:
- **Responsive layout** that adapts to screen size
- **Touch-friendly interface** with appropriate sizing
- **Mobile navigation** optimized for small screens
- **Performance optimization** for mobile networks

## 🔄 Updates & Maintenance

### Automatic Updates
Set up automatic updates using GitHub Actions:
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Deployment commands here
```

### Manual Updates
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
./launch_oslo_premium.sh
```

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port
   lsof -i :8503
   # Kill process
   kill -9 <PID>
   ```

2. **Module not found**:
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Database errors**:
   ```bash
   # Reset database
   rm oslo_planning_premium.db
   python -c "from oslo_planning_premium import OsloPlanningPremium; OsloPlanningPremium()"
   ```

### Performance Issues
- **Memory usage**: Monitor with `htop` or `ps`
- **Database locks**: Check SQLite file permissions
- **Network latency**: Test URL verification speed

## 📞 Support

For deployment support:
- **Documentation**: Check docs/ directory
- **Issues**: Create GitHub issue
- **Community**: Streamlit community forums

---

**🏛️ Oslo Planning Documents - Premium**  
*Professional deployment for production environments*