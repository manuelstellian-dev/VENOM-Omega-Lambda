# Deployment Guide

**Multi-Device VENOM Ω-Λ Deployment**

---

## Table of Contents

1. [Overview](#overview)
2. [Single Device (Android)](#single-device-android)
3. [Multi-Device Mesh](#multi-device-mesh)
4. [Production Deployment](#production-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Overview

VENOM Ω-Λ can be deployed in multiple configurations:

1. **Standalone Android** - All components on one device
2. **Android + PC** - Phone as edge, PC as compute node
3. **Android + Multiple PCs** - Full mesh network
4. **Server Cluster** - Lambda-only nodes for heavy compute

---

## Single Device (Android)

### **Prerequisites**

- Android 8.0+ (API 26+)
- 4GB+ RAM
- 8+ CPU cores recommended
- 2GB+ free storage

### **Installation**

#### **Option 1: Using Installation Script**

```bash
# Clone repository
git clone https://github.com/manuelstellian-dev/VENOM-Omega-Lambda.git
cd VENOM-Omega-Lambda

# Run installation script
chmod +x scripts/install_android.sh
./scripts/install_android.sh
```

#### **Option 2: Manual Installation**

**Step 1: Build APK**

```bash
# Build release APK
./gradlew assembleRelease

# APK location:
# app/build/outputs/apk/release/app-release.apk
```

**Step 2: Install on Device**

```bash
# Connect device via USB (enable USB debugging)
adb devices

# Install APK
adb install -r app/build/outputs/apk/release/app-release.apk
```

**Step 3: Grant Permissions**

```bash
PACKAGE="com.venom.aios"

adb shell pm grant $PACKAGE android.permission.INTERNET
adb shell pm grant $PACKAGE android.permission.ACCESS_NETWORK_STATE
adb shell pm grant $PACKAGE android.permission.WAKE_LOCK
adb shell pm grant $PACKAGE android.permission.POST_NOTIFICATIONS
```

**Step 4: Create Directories**

```bash
adb shell "mkdir -p /sdcard/venom/models"
adb shell "mkdir -p /sdcard/venom/knowledge"
adb shell "mkdir -p /sdcard/venom/logs"
```

**Step 5: Launch App**

```bash
adb shell am start -n $PACKAGE/.main.MainActivity
```

### **Verification**

```bash
# View logs
adb logcat | grep VENOM

# Check if organism is alive
adb logcat | grep "ORGANISM: ALIVE"
```

**Expected Output**:
```
[VENOM] 🌌 VENOM Ω-Λ ORGANISM: ALIVE! 🌌
[VENOM] Ω COMPONENTS: ✅ (6 components)
[VENOM] Λ COMPONENTS: ✅ (5 components)
[VENOM] Organism is now breathing, thinking, and evolving...
```

---

## Multi-Device Mesh

### **Architecture**

```
┌─────────────────┐
│  Android Phone  │ ← User interface + Omega brain
│  (Edge Node)    │
└────────┬────────┘
         │
         ├──────────┐
         │          │
    ┌────▼────┐  ┌──▼──────┐
    │ Linux   │  │ Linux   │ ← Lambda compute nodes
    │ Laptop  │  │ Server  │
    └─────────┘  └─────────┘
    
    All nodes auto-discover via UDP multicast (224.1.1.1:19845)
```

### **Deployment Steps**

#### **1. Deploy Android (Edge Node)**

Follow [Single Device](#single-device-android) steps above.

#### **2. Deploy Linux Node(s)**

**On each Linux machine:**

```bash
# Clone repository
git clone https://github.com/manuelstellian-dev/VENOM-Omega-Lambda.git
cd VENOM-Omega-Lambda

# Run installation script
chmod +x scripts/install_linux.sh
./scripts/install_linux.sh
```

**Manual Steps**:

**A. Install Python dependencies**

```bash
pip3 install --user -r requirements.txt
```

**B. Generate gRPC stubs**

```bash
cd lambda/core
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. venom.proto
cd ../..
```

**C. Create directories**

```bash
mkdir -p ~/venom/logs
mkdir -p ~/venom/lambda
cp -r lambda/* ~/venom/lambda/
```

**D. Install systemd services**

```bash
# Copy service files
cp systemd/*.service ~/.config/systemd/user/

# Reload systemd
systemctl --user daemon-reload

# Enable services
systemctl --user enable venom-fractal.service
systemctl --user enable venom-api.service
systemctl --user enable venom-mesh-discovery.service
systemctl --user enable venom-mesh-orchestrator.service

# Start services
systemctl --user start venom-fractal.service
systemctl --user start venom-api.service
systemctl --user start venom-mesh-discovery.service
systemctl --user start venom-mesh-orchestrator.service
```

**E. Verify services**

```bash
# Check status
systemctl --user status venom-api.service

# View logs
journalctl --user -u venom-api.service -f
```

**Expected Output**:
```
[INFO] 🕸️ VENOM Mesh Discovery Daemon starting
[INFO] 🕸️ Listening on 224.1.1.1:19845
[INFO] 📡 Announced presence
[INFO] 🔗 Discovered peer: abc123... at 192.168.1.100:8443
```

#### **3. Verify Mesh Formation**

**On Android:**

```bash
adb logcat | grep "Mesh Nodes"
```

**Expected**: `Mesh Nodes: 3` (or more)

**On Linux:**

```bash
cat ~/.venom_peers.json
```

**Expected Output**:
```json
{
  "node-uuid-1": {
    "addr": ["192.168.1.100", 8443],
    "last_seen": 1735854453.123,
    "healthy": true
  },
  "node-uuid-2": {
    "addr": ["192.168.1.101", 8443],
    "last_seen": 1735854453.456,
    "healthy": true
  }
}
```

#### **4. Test Mesh Communication**

**From Android:**

```kotlin
// In your code
omegaLambdaBridge.broadcastToMesh("Hello from Android!")
```

**From Linux:**

```python
from lambda.mesh.mesh import Mesh

mesh = Mesh()
mesh.start()
mesh.broadcast("linux_node", "Hello from Linux!")
```

**Verify**:

```bash
# On any node, check logs
journalctl --user -u venom-mesh-discovery.service | grep "Hello"
```

---

## Production Deployment

### **Security Hardening**

#### **1. Network Isolation**

Use VPN or private network for mesh communication:

```bash
# Configure mesh to use VPN interface
export VENOM_MESH_INTERFACE=tun0
```

#### **2. Firewall Rules**

**Allow only mesh nodes**:

```bash
# Allow UDP multicast
sudo ufw allow from 192.168.1.0/24 to 224.1.1.1 port 19845 proto udp

# Allow gRPC
sudo ufw allow from 192.168.1.0/24 to any port 8443 proto tcp

# Allow REST API (local only)
sudo ufw allow from 127.0.0.1 to any port 8000 proto tcp
```

#### **3. TLS/SSL for gRPC**

**Generate certificates**:

```bash
# Generate CA
openssl req -x509 -newkey rsa:4096 -keyout ca-key.pem -out ca-cert.pem -days 365 -nodes

# Generate server cert
openssl req -newkey rsa:4096 -keyout server-key.pem -out server-req.pem -nodes
openssl x509 -req -in server-req.pem -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days 365
```

**Configure gRPC server**:

```python
# In venom-api.py
credentials = grpc.ssl_server_credentials([
    (server_key, server_cert)
])
server.add_secure_port('0.0.0.0:8443', credentials)
```

#### **4. Authentication**

Add API key authentication:

```python
# In venom-api.py
API_KEY = os.getenv("VENOM_API_KEY")

@app.get("/time_wrap")
def time_wrap_endpoint(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401)
    # ... rest of code
```

### **Performance Tuning**

#### **1. Systemd Service Limits**

Edit service files to increase limits:

```ini
[Service]
# Increase memory limit
MemoryMax=2G

# Increase CPU quota
CPUQuota=200%

# Increase file descriptors
LimitNOFILE=65536
```

#### **2. Python Optimization**

```bash
# Use PyPy for better performance
pip3 install pypy3

# Update service to use PyPy
ExecStart=/usr/bin/pypy3 fractal.py
```

#### **3. Database Optimization**

If using vector databases:

```python
# Use FAISS with GPU
import faiss

# GPU index
res = faiss.StandardGpuResources()
index = faiss.index_cpu_to_gpu(res, 0, index_cpu)
```

### **High Availability**

#### **1. Multiple Android Devices**

Deploy on multiple phones for redundancy:

```
Phone 1 (Primary) ←→ Mesh
Phone 2 (Backup)  ←→ Mesh
```

If primary fails, backup takes over automatically.

#### **2. Load Balancing**

The mesh orchestrator automatically balances load:

```python
# In venom-mesh-orchestrator.py
def dispatch_task(task):
    # Picks node with lowest load (EMA-based)
    target = min(peers, key=lambda p: recent_load(p))
    return execute_on_node(target, task)
```

#### **3. Health Monitoring**

Set up monitoring:

```bash
# Prometheus exporter (optional)
pip3 install prometheus-client

# Add to venom-api.py
from prometheus_client import start_http_server, Counter

requests_total = Counter('venom_requests_total', 'Total requests')

start_http_server(9090)
```

**Monitor with Grafana**:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'venom'
    static_configs:
      - targets: ['localhost:9090']
```

---

## Monitoring & Maintenance

### **Health Checks**

#### **Android**

**Via UI**: Check vitals card in app

**Via adb**:

```bash
adb logcat | grep "ORGANISM VITALS"
```

**Expected**:
```
💓 ORGANISM VITALS:
├─ Theta (θ): 0.750
├─ Lambda Score: 0.820
├─ Mesh Nodes: 3
├─ CPU Health: 85%
├─ Memory: 72%
├─ Thermal: 90%
└─ Battery: 80%
```

#### **Linux**

**Service status**:

```bash
systemctl --user status venom-*.service
```

**API health**:

```bash
curl http://127.0.0.1:8000/health
```

**Expected**:
```json
{
  "status": "healthy",
  "service": "venom-api"
}
```

**Mesh peers**:

```bash
cat ~/.venom_peers.json | jq '.[] | select(.healthy==true) | .addr'
```

### **Log Management**

**Rotate logs**:

```bash
# Create logrotate config
cat > ~/.config/logrotate/venom.conf << EOF
~/venom/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOF

# Add to crontab
crontab -e
# Add: 0 0 * * * /usr/sbin/logrotate ~/.config/logrotate/venom.conf
```

**View logs**:

```bash
# Fractal worker
journalctl --user -u venom-fractal.service -f

# API
journalctl --user -u venom-api.service -f

# Mesh discovery
journalctl --user -u venom-mesh-discovery.service -f

# Orchestrator
journalctl --user -u venom-mesh-orchestrator.service -f
```

### **Backup & Restore**

**Backup**:

```bash
#!/bin/bash
# backup_venom.sh

BACKUP_DIR=~/venom_backup_$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup Lambda code
cp -r ~/venom/lambda $BACKUP_DIR/

# Backup peer registry
cp ~/.venom_peers.json $BACKUP_DIR/

# Backup logs (last 7 days)
cp ~/venom/logs/*.log $BACKUP_DIR/

# Compress
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "✅ Backup created: $BACKUP_DIR.tar.gz"
```

**Restore**:

```bash
#!/bin/bash
# restore_venom.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore_venom.sh backup_file.tar.gz"
    exit 1
fi

# Stop services
systemctl --user stop venom-*.service

# Extract backup
tar -xzf $BACKUP_FILE -C ~/ 

# Move to correct location
cp -r ~/venom_backup_*/lambda ~/venom/
cp ~/venom_backup_*/.venom_peers.json ~/ 

# Start services
systemctl --user start venom-*.service

echo "✅ Restore complete"
```

### **Updates**

**Update Lambda code**:

```bash
# Pull latest changes
git pull origin main

# Reinstall Python dependencies
pip3 install --user -r requirements.txt --upgrade

# Regenerate gRPC stubs
cd lambda/core
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. venom.proto
cd ../..

# Restart services
systemctl --user restart venom-*.service
```

**Update Android app**:

```bash
# Build new APK
./gradlew assembleRelease

# Install update
adb install -r app/build/outputs/apk/release/app-release.apk
```

### **Troubleshooting**

**Issue: Mesh nodes not discovering each other**

```bash
# Check multicast routing
ip maddr show

# Check firewall
sudo ufw status

# Test multicast
# Terminal 1:
nc -u -l 19845

# Terminal 2:
echo "test" | nc -u 224.1.1.1 19845
```

**Issue: High CPU usage**

```bash
# Check which service
systemctl --user status venom-*.service | grep CPU

# View process tree
ps auxf | grep venom

# Reduce load
systemctl --user stop venom-fractal.service  # Temporarily stop worker
```

**Issue: gRPC connection failed**

```bash
# Test gRPC connectivity
grpcurl -plaintext 127.0.0.1:8443 list

# Check if port is open
netstat -tuln | grep 8443

# Restart API service
systemctl --user restart venom-api.service
```

---

## Scaling Guidelines

| Nodes | Use Case | Performance |
|-------|----------|-------------|
| 1 (Android only) | Personal use | Baseline |
| 2 (Android + PC) | Development | 2-3× faster |
| 3-5 nodes | Small team | 5-10× faster |
| 10+ nodes | Production | 10-50× faster |

**Optimal Configuration**:
- 1 Android (edge)
- 2-3 Linux PCs (compute)
- 1 Linux server (heavy tasks)

---

**Last Updated**: 2025-01-04  
**Version**: 1.0.0-alpha  
**Author**: manuelstellian-dev
