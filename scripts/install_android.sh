
#!/bin/bash
# scripts/install_android.sh
# Supreme Hybrid VENOM Ω-Λ Android Installation Script
# ---------------------------------------------------
# Păstrează tot codul workspace și adaugă incremental funcționalități avansate

set -e

echo "📱 VENOM Ω-Λ Android Installation Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if adb is installed
if ! command -v adb &> /dev/null; then
    echo -e "${RED}❌ Error: adb not found. Please install Android SDK Platform Tools.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ adb found${NC}"

# Check if device is connected
if ! adb devices | grep -q "device$"; then
    echo -e "${RED}❌ Error: No Android device connected.${NC}"
    echo "Please connect your device and enable USB debugging."
    exit 1
fi

echo -e "${GREEN}✅ Device connected${NC}"

# Build APK (both debug and release)
echo ""
echo "Building Android APK (debug & release)..."
./gradlew assembleDebug
./gradlew assembleRelease

APK_PATH_DEBUG="app/build/outputs/apk/debug/app-debug.apk"
APK_PATH_RELEASE="app/build/outputs/apk/release/app-release.apk"

if [ ! -f "$APK_PATH_RELEASE" ]; then
    echo -e "${YELLOW}⚠️  APK release not found. Using debug APK.${NC}"
    APK_PATH="$APK_PATH_DEBUG"
else
    APK_PATH="$APK_PATH_RELEASE"
fi

if [ ! -f "$APK_PATH" ]; then
    echo -e "${RED}❌ Error: APK not found at $APK_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✅ APK found: $APK_PATH${NC}"

# Install APK
echo ""
echo "📦 Installing APK..."
adb install -r "$APK_PATH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ APK installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install APK${NC}"
    exit 1
fi

# Grant permissions (supreme set)
echo ""
echo "🔐 Granting permissions..."
PACKAGE_NAME="com.venom.aios"
adb shell pm grant $PACKAGE_NAME android.permission.INTERNET || true
adb shell pm grant $PACKAGE_NAME android.permission.ACCESS_NETWORK_STATE || true
adb shell pm grant $PACKAGE_NAME android.permission.WAKE_LOCK || true
adb shell pm grant $PACKAGE_NAME android.permission.FOREGROUND_SERVICE || true
adb shell pm grant $PACKAGE_NAME android.permission.POST_NOTIFICATIONS || true
adb shell pm grant $PACKAGE_NAME android.permission.USE_BIOMETRIC || true

echo -e "${GREEN}✅ Permissions granted${NC}"

# Create directories on device (supreme set)
echo ""
echo "📁 Creating directories on device..."
adb shell "mkdir -p /sdcard/venom/models"
adb shell "mkdir -p /sdcard/venom/knowledge"
adb shell "mkdir -p /sdcard/venom/logs"
adb shell "mkdir -p /sdcard/venom/cache"
adb shell "mkdir -p /sdcard/venom/quarantine"

echo -e "${GREEN}✅ Directories created${NC}"

# Launch app
echo ""
echo "🚀 Launching VENOM Ω-Λ..."
adb shell am start -n $PACKAGE_NAME/.main.MainActivity

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "The organism is now breathing on your device."
echo ""
echo "Useful commands:"
echo "  - View logs: adb logcat | grep VENOM"
echo "  - Uninstall: adb uninstall $PACKAGE_NAME"
echo "  - Clear data: adb shell pm clear $PACKAGE_NAME"
echo ""
# Workspace legacy commands (păstrate):
echo "Granting permissions (optional):"
echo "  adb shell pm grant com.venom.aios android.permission.INTERNET"
echo "  adb shell pm grant com.venom.aios android.permission.WAKE_LOCK"
echo ""
echo "Launch with:"
echo "  adb shell am start -n com.venom.aios/.main.MainActivity"
