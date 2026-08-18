# New-File-Rename
# 🚀 Advanced File Rename & Stream Remover Bot

A powerful and high-speed Telegram Bot built with **Pyrogram**, **FFmpeg**, and **MongoDB**. This bot allows you to rename files, edit video metadata, remove specific audio/subtitle streams, and upload files directly to Telegram or GoFile.

---

## ✨ Features

* ⚡ **High-Speed Downloads/Uploads**: Integrated real-time progress bar with Speed, ETA, Percentage, and File size tracking.
* 🛠️ **Audio & Subtitle Stream Removal**:
  * Remove all audio streams (Mute Video).
  * Remove all subtitle tracks.
  * Dynamically detect and selectively delete specific stream tracks using `ffprobe`.
* 🏷️ **Custom Renaming**: Add custom Prefix, Suffix, and perform text replacements.
* 💾 **Database Integration**: MongoDB support for saving user settings permanently across app restarts.
* ☁️ **Third-Party Uploads**: Integrated GoFile support for uploading files outside Telegram.
* 🐳 **Railway & Docker Ready**: Pre-configured with Dockerfile and FFmpeg dependencies for seamless cloud deployment.

---

## 🛠️ Repository Structure

```text
telegram-rename-bot/
├── bot.py                  # Main Bot Logic & Process Handlers
├── config.py               # Environment Configuration Variables
├── database.py             # MongoDB Connection & User Storage Logic
├── plugins/
│   ├── progress.py         # Real-time Progress Bar Calculations
│   ├── stream_tools.py     # FFmpeg/FFprobe Video Stream Removal Tools
│   ├── rename.py           # Text Processing & File Renaming Functions
│   └── gofile.py           # GoFile Uploader API Integration
├── requirements.txt        # Required Python Libraries
├── Dockerfile              # Docker Configuration with FFmpeg
├── Procfile                # Worker Process Definition
└── README.md               # Documentation File
