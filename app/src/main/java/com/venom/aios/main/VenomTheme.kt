
package com.venom.aios.main

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// --- Paleta workspace ---
private val WorkspaceDarkColorScheme = darkColorScheme(
    primary = Color(0xFF00E5FF),
    secondary = Color(0xFF64FFDA),
    tertiary = Color(0xFFFF6E40),
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    onPrimary = Color(0xFF000000),
    onSecondary = Color(0xFF000000),
    onTertiary = Color(0xFF000000),
    onBackground = Color(0xFFE0E0E0),
    onSurface = Color(0xFFE0E0E0),
)

private val WorkspaceLightColorScheme = lightColorScheme(
    primary = Color(0xFF0097A7),
    secondary = Color(0xFF00897B),
    tertiary = Color(0xFFFF5722),
    background = Color(0xFFFAFAFA),
    surface = Color(0xFFFFFFFF),
    onPrimary = Color(0xFFFFFFFF),
    onSecondary = Color(0xFFFFFFFF),
    onTertiary = Color(0xFFFFFFFF),
    onBackground = Color(0xFF212121),
    onSurface = Color(0xFF212121),
)

// --- Paleta avansată (din varianta ta) ---
private val VenomPurple = Color(0xFF6200EE)
private val VenomPurpleVariant = Color(0xFF3700B3)
private val VenomTeal = Color(0xFF03DAC5)
private val VenomBlack = Color(0xFF000000)
private val VenomWhite = Color(0xFFFFFFFF)
private val VenomDarkGray = Color(0xFF121212)
private val VenomLightGray = Color(0xFFE0E0E0)

private val AdvancedDarkColorScheme = darkColorScheme(
    primary = VenomPurple,
    secondary = VenomTeal,
    tertiary = VenomPurpleVariant,
    background = VenomDarkGray,
    surface = Color(0xFF1E1E1E),
    onPrimary = VenomWhite,
    onSecondary = VenomBlack,
    onBackground = VenomWhite,
    onSurface = VenomWhite,
)

private val AdvancedLightColorScheme = lightColorScheme(
    primary = VenomPurple,
    secondary = VenomTeal,
    tertiary = VenomPurpleVariant,
    background = VenomWhite,
    surface = VenomLightGray,
    onPrimary = VenomWhite,
    onSecondary = VenomBlack,
    onBackground = VenomBlack,
    onSurface = VenomBlack,
)

/**
 * Tema hibridă VENOM: poți alege rapid între paleta workspace și cea avansată
 */
@Composable
fun VenomTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    useAdvancedPalette: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        useAdvancedPalette && darkTheme -> AdvancedDarkColorScheme
        useAdvancedPalette && !darkTheme -> AdvancedLightColorScheme
        darkTheme -> WorkspaceDarkColorScheme
        else -> WorkspaceLightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography(),
        content = content
    )
}
