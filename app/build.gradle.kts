
// app/build.gradle.kts (Hibrid VENOM)
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.chaquo.python")
}

android {
    namespace = "com.venom.aios"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.venom.aios"
        minSdk = 26  // Android 8.0+ (NNAPI support)
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0-alpha"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        vectorDrawables {
            useSupportLibrary = true
        }

        // NDK configuration
        ndk {
            abiFilters += listOf("arm64-v8a", "armeabi-v7a")
        }

        // Python configuration (Chaquopy)
        ndk {
            abiFilters.addAll(listOf("arm64-v8a", "armeabi-v7a"))
        }

        python {
            buildPython("/usr/bin/python3")

            pip {
                // Install Lambda dependencies
                install("fastapi")
                install("uvicorn")
                install("grpcio")
                install("grpcio-tools")
                install("numpy")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            isMinifyEnabled = false
            isDebuggable = true
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.4"
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // Core Android
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.2")
    implementation("androidx.activity:activity-compose:1.8.1")

    // Compose UI
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")

    // TensorFlow Lite (Neural Network)
    implementation("org.tensorflow:tensorflow-lite:2.14.0")
    implementation("org.tensorflow:tensorflow-lite-gpu:2.14.0")
    implementation("org.tensorflow:tensorflow-lite-support:0.4.4")
    implementation("org.tensorflow:tensorflow-lite-metadata:0.4.4")

    // WorkManager (Background tasks)
    implementation("androidx.work:work-runtime-ktx:2.9.0")

    // Biometrics
    implementation("androidx.biometric:biometric:1.1.0")

    // JSON
    implementation("org.json:json:20231013")

    // Chaquopy (Python integration)
    implementation("com.chaquo.python:gradle:14.0.2")

    // Room Database (optional - for knowledge storage)
    val roomVersion = "2.6.1"
    implementation("androidx.room:room-runtime:$roomVersion")
    implementation("androidx.room:room-ktx:$roomVersion")

    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2023.10.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")

    // Debug tools
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}

// Chaquopy Python configuration
chaquopy {
    defaultConfig {
        buildPython("/usr/bin/python3")

        pip {
            // Lambda Core dependencies
            install("fastapi==0.104.1")
            install("uvicorn[standard]==0.24.0")
            install("grpcio==1.59.3")
            install("grpcio-tools==1.59.3")
            install("numpy==1.26.2")
            install("protobuf==4.25.1")
        }

        // Include Lambda Python source
        pyc {
            src = false
        }

        // Static proxy configuration
        staticProxy("lambda")
    }

    productFlavors {
        // Optional: different Python versions for different flavors
    }

    sourceSets {
        getByName("main") {
            srcDir("src/main/python")
        }
    }
}
