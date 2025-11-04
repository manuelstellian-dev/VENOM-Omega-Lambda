#!/bin/bash
# VENOM Android Installation Script

set -e

echo "🌌 VENOM Ω-AIOS Android Installation"
echo "======================================"

# Build the APK
echo ""
echo "Building Android APK..."
./gradlew assembleDebug

APK_PATH="app/build/outputs/apk/debug/app-debug.apk"

if [ ! -f "$APK_PATH" ]; then
    echo "❌ APK not found at $APK_PATH"
    exit 1
fi

echo "✅ APK built successfully"

# Check for connected devices
echo ""
echo "Checking for connected Android devices..."
adb devices

# Install APK
echo ""
echo "Installing APK..."
adb install -r "$APK_PATH"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Granting permissions (optional):"
echo "  adb shell pm grant com.venom.aios android.permission.INTERNET"
echo "  adb shell pm grant com.venom.aios android.permission.WAKE_LOCK"
echo ""
echo "Launch with:"
echo "  adb shell am start -n com.venom.aios/.main.MainActivity"
