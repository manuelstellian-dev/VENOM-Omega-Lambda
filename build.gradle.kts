// Top-level build file (Hibrid VENOM)
// Poți adăuga opțiuni avansate pentru toate modulele/subproiectele
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.21" apply false
    id("com.chaquo.python") version "14.0.2" apply false
}

buildscript {
    // repositories moved to settings.gradle.kts
}

allprojects {
    // repositories moved to settings.gradle.kts
}

tasks.register("clean", Delete::class) {
    delete(rootProject.buildDir)
}
