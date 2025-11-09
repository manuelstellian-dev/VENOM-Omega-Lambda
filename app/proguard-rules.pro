# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.kts.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# --- EXTENSII HIBRIDE ---

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile

# Keep TensorFlow Lite classes
-keep class org.tensorflow.lite.** { *; }
-keep interface org.tensorflow.lite.** { *; }
-keep class org.tensorflow.** { *; }
-dontwarn org.tensorflow.**

# Keep Python/Chaquopy classes
-keep class com.chaquo.python.** { *; }
-dontwarn com.chaquo.python.**

# Keep VENOM classes
-keep class com.venom.aios.** { *; }
-keep class com.venom.omega.** { *; }
-keep class com.venom.integration.** { *; }
-keep class com.venom.main.** { *; }

# Keep Kotlin coroutines
-keepclassmembers class kotlinx.coroutines.** {
	volatile <fields>;
}
-dontwarn kotlinx.coroutines.**

# Keep data classes
-keep class com.venom.main.OrganismVitals { *; }
-keep class com.venom.main.ChatMessage { *; }

# Keep Compose
-keep class androidx.compose.** { *; }
-dontwarn androidx.compose.**

# Keep Material3
-keep class androidx.compose.material3.** { *; }

# Keep native methods
-keepclasseswithmembernames class * {
	native <methods>;
}

# Keep enums
-keepclassmembers enum * {
	public static **[] values();
	public static ** valueOf(java.lang.String);
}

# --- EXTENSII HIBRIDE ---
# Keep Python integration
-keep class com.chaquo.python.** { *; }
-dontwarn com.chaquo.python.**

# Keep TensorFlow Lite
-keep class org.tensorflow.** { *; }
-dontwarn org.tensorflow.**

# Keep Kotlin coroutines
-keepclassmembers class kotlinx.coroutines.** {
	volatile <fields>;
}
-dontwarn kotlinx.coroutines.**

# Keep data classes
-keep class com.venom.main.OrganismVitals { *; }
-keep class com.venom.main.ChatMessage { *; }

# Keep Compose
-keep class androidx.compose.** { *; }
-dontwarn androidx.compose.**

# Keep Material3
-keep class androidx.compose.material3.** { *; }

# Keep VENOM components
-keep class com.venom.omega.** { *; }
-keep class com.venom.integration.** { *; }
-keep class com.venom.main.** { *; }

# Keep native methods
-keepclasseswithmembernames class * {
	native <methods>;
}

# Keep enums
-keepclassmembers enum * {
	public static **[] values();
	public static ** valueOf(java.lang.String);
}
