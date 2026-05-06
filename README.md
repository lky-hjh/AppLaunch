# AppLauncher 🚀

一键软件启动器 — 带 GUI 的轻量级桌面工具，集中管理你常用的程序、脚本和项目，一键全部启动。

**One-click App Launcher** — A lightweight GUI tool to manage and launch all your frequently-used apps, scripts, and projects in one place.

## Features

- ⚡ **一键全部启动** — Launch all apps with a single click
- ▶ **单独启动** — Launch individual apps
- 🔍 **搜索过滤** — Quickly find apps by name or path
- ➕ **可视化增删改** — Add/edit/delete apps through the UI
- 💾 **自动保存** — Config persists to `apps.json`
- 🎨 **现代深色主题** — Modern Fluent dark theme with colored icons

## Screenshot

```
┌────────────────────────────────────────┐
│ 🚀  一键启动器              [＋ 添加软件] │
│────────────────────────────────────────│
│ 🔍 Search...                          │
│                                        │
│  🔷 Chrome                ▶ ✎ ✕       │
│  📝 VS Code               ▶ ✎ ✕       │
│  🐳 Docker Desktop        ▶ ✎ ✕       │
│  💻 Terminal              ▶ ✎ ✕       │
│                                        │
│ 共 4 个软件              [⚡ 一键全部启动] │
└────────────────────────────────────────┘
```

## Requirements

- **Python 3.x** (with tkinter, included by default on Windows)
- **Windows** (uses `os.startfile` — macOS/Linux support not yet implemented)

## Quick Start

```bash
# Clone or download
git clone https://github.com/yourname/AppLauncher.git
cd AppLauncher

# Run
python launcher.py
```

Or double-click **`launcher.bat`** (English) / **`启动器.bat`** (Chinese).

## Usage

### Adding an app
Click the **"＋ 添加软件"** button, enter the name and path, then click **确定**.

Supported file types:
- `.exe` — Windows executables
- `.bat` / `.cmd` — Batch scripts
- `.lnk` — Shortcuts
- `.ps1` — PowerShell scripts
- `.py` — Python scripts
- `http://` / `https://` — URLs (opens in browser)

### Config file
Apps are stored in `apps.json` (auto-generated). You can edit it manually:

```json
[
  { "name": "记事本", "path": "C:\\Windows\\System32\\notepad.exe" },
  { "name": "Chrome", "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" }
]
```

> **Tip:** Use **relative paths** for portable setups — the launcher resolves them relative to the script directory.

### Custom launch scripts
For apps that need command-line arguments (e.g., opening a specific project in Rider or CodeBuddy), create a `.bat` wrapper and add it to the list. See [`examples/`](./examples/) for templates.

```bat
@echo off
chcp 65001 >nul
start "" "C:\Program Files\JetBrains\Rider\bin\rider64.exe" "D:\Projects\MyGame\MyGame.sln"
```

## Project Structure

```
AppLauncher/
├── launcher.py              # Main application
├── launcher.bat             # Windows launcher (English)
├── 启动器.bat               # Windows launcher (Chinese)
├── apps.json                # App config (auto-generated)
├── examples/                # Example launch scripts
│   ├── launch_codebuddy.bat
│   └── launch_rider_template.bat
├── LICENSE                  # MIT License
└── README.md
```

## License

MIT
