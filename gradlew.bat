@rem Gradle startup script for Windows
@rem SPDX-License-Identifier: Apache-2.0

@if "%DEBUG%"=="" @echo off
set APP_BASE_NAME=%~n0
set APP_HOME=%~dp0

set GRADLE_USER_HOME=%USERPROFILE%\.gradle
"%APP_HOME%\gradle\wrapper\gradle-wrapper.jar" %*
