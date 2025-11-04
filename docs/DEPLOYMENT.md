# VENOM Deployment Guide

## Android Deployment

### Development
```bash
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

### Production
1. Configure signing in `app/build.gradle.kts`
2. Build release: `./gradlew assembleRelease`
3. Sign APK with your keystore
4. Distribute via Play Store or direct download

## Linux Deployment

### Single Node
```bash
bash scripts/install_linux.sh
systemctl --user enable --now venom-api
systemctl --user enable --now venom-mesh-discovery
```

### Multi-Node Mesh
1. Edit `scripts/mesh_nodes.txt`
2. Add node hostnames/IPs
3. Run: `bash scripts/deploy_mesh.sh`
4. Start services on each node

## Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY venom_lambda/ ./venom_lambda/
CMD ["python", "-m", "lambda.core.venom_api"]
```

## Systemd Configuration

Services installed to `~/.config/systemd/user/`

Check status:
```bash
systemctl --user status venom-api
journalctl --user -u venom-api -f
```
