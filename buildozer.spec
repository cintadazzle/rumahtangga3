[app]

# (str) Title of your application
title = FinanceManager

# (str) Package name
package.name = financemanager

# (str) Package domain (needed for android/ios packaging)
package.domain = org.rumahtangga

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
# CATATAN: sqlite3 dihapus karena merupakan bawaan python3, python3 dihapus versi spesifiknya.

requirements = python3, kivy==2.3.0, kivymd==1.2.0, opencv, pyrebase4, python-dateutil, requests, urllib3, certifi, chardet, idna, openssl

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use
# Menggunakan versi 25b yang sangat stabil untuk Kivy 2.3.0 + API 33
android.ndk = 28c

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = main.py

# (list) Pattern to exclude from the image
# android.exclude_src = *.pyc,*/.git/*

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# Secara default Buildozer akan membuat versi armeabi-v7a (32-bit)
android.archs = armeabi-v7a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1