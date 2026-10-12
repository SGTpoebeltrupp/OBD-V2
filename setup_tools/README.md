# OBD-V2 Build Tools

This directory contains comprehensive build and packaging tools for creating distributable OBD-V2 applications across different platforms.

## Overview

OBD-V2 uses modern Python packaging with `pyproject.toml` and provides automated build scripts for creating platform-specific installers:

- **Windows**: InnoSetup-based installer with embedded Python runtime
- **macOS**: PyInstaller-based DMG with universal binary support
- **Linux**: Native package support (development mode)

## Prerequisites

### Common Requirements
- **Python 3.8+** (3.10+ recommended)
- **Git** for version control
- **Development tools** for your platform

### Platform-Specific Requirements

#### Windows
- **InnoSetup 6.0+** - [Download Here](https://jrsoftware.org/isdl.php)
- **Microsoft Visual Studio Build Tools** (for some dependencies)
- **Windows SDK** (for installer signing, optional)

#### macOS
- **Xcode Command Line Tools**: `xcode-select --install`
- **PyInstaller**: `pip install pyinstaller`
- **create-dmg** (optional, for enhanced DMG creation): `brew install create-dmg`

#### Linux
- **Build essentials**: `sudo apt-get install build-essential`
- **Python development headers**: `sudo apt-get install python3-dev`

## Windows Build Process

### 1. Prepare Environment
```bash
# Clone repository
git clone https://github.com/sgtpoebeltrupp/obd-v2.git
cd obd_v2

# Create virtual environment
python -m venv ./venv
.\venv\Scripts\activate.bat

# Install dependencies
pip install -e .
```

### 2. Update Version Information
Edit `setup_tools/inno-win-setup/version.h`:
```c
#define __appname__ "OBD-V2"
#define __version__ "3.0.7"
#define __status__ "Kakapo"
#define __author__ "OBD-V2"
#define __copyright__ "Copyright ©2026"
#define __email__ ""
```

### 3. Build Installer
```bash
# Navigate to setup tools directory
cd setup_tools/inno-win-setup

# Compile with InnoSetup (GUI)
# Open wininstaller.iss in InnoSetup and compile

# Or compile via command line
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" wininstaller.iss
```

### 4. Output
- **Installer**: `OBD-V2-Windows-Installer-v3.0.7_Kakapo-x64.exe`
- **Location**: Same directory as the `.iss` file
- **Size**: ~150-200MB (includes Python runtime)

### Windows Installer Features
- **Embedded Python 3.13** runtime
- **Automatic dependency management**
- **Desktop shortcut creation**
- **Start menu integration**
- **Uninstaller with complete cleanup**
- **User permission management** for logs and data directories

## macOS Build Process

### 1. Prepare Environment
```bash
# Clone repository
git clone https://github.com/sgtpoebeltrupp/obd-v2.git
cd obd_v2

# Create virtual environment
python3 -m venv ./venv
source ./venv/bin/activate

# Upgrade packaging tools (recommended on macOS)
python3 -m pip install --upgrade pip setuptools wheel

# Install dependencies including PyInstaller
pip install -e ".[dev]"
pip install pyinstaller
```

### 2. Update Build Configuration
Edit `setup_tools/mac-os/main.spec` if needed:
- Update paths for new project structure
- Modify hidden imports for additional dependencies
- Adjust data files for new resource locations

### 3. Build Application
```bash
# Navigate to setup tools directory
cd setup_tools/mac-os

# Build using PyInstaller
pyinstaller main.spec

# Or use the build script
chmod +x builddmg.sh
./builddmg.sh
```

### 4. Create DMG (Optional Enhanced)
```bash
# Install create-dmg if not already installed
brew install create-dmg

# Create enhanced DMG with background and proper layout
create-dmg \
  --volname "OBD-V2" \
  --volicon "OBD-V2.app/Contents/Resources/icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "OBD-V2.app" 175 120 \
  --hide-extension "OBD-V2.app" \
  --app-drop-link 425 120 \
  "OBD-V2.dmg" \
  "dist/"
```

### 5. Output
- **Application**: `OBD-V2.app` (in `dist/` directory)
- **DMG**: `OBD-V2.dmg` (if using create-dmg)
- **Architecture**: Universal binary (Intel + Apple Silicon)
- **Size**: ~80-120MB

### macOS Build Features
- **Universal binary** support for Intel and Apple Silicon
- **Code signing** support (with appropriate certificates)
- **Notarization** ready (entitlements.plist included)
- **Standalone application** with embedded dependencies
- **Proper macOS integration** (dock, menus, etc.)

## Linux Build Process

### Development Installation (Recommended)
```bash
# Clone and install
git clone https://github.com/sgtpoebeltrupp/obd-v2.git
cd obd_v2

# Create virtual environment
python3 -m venv ./venv
source ./venv/bin/activate

# Install in development mode
pip install -e .

# Create desktop entry
cat > ~/.local/share/applications/obd_v2.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=OBD-V2
Comment=ECU diagnostic tool
Exec=$(pwd)/venv/bin/obd_v2
Icon=$(pwd)/src/obd_v2/resources/icons/obd.ico
Terminal=false
Categories=Development;Science;
EOF
```

### Package Building (Advanced)
```bash
# Install packaging tools
sudo apt-get install python3-stdeb dh-python

# Create Debian package
python setup.py --command-packages=stdeb bdist_deb

# Output in deb_dist/
```

## Version Management

### Automatic Version Sync
The build systems automatically sync version information from:
- `src/obd_v2/version.py` (primary source)
- `pyproject.toml` (package version)
- `setup_tools/inno-win-setup/version.h` (Windows installer)

### Version Update Process
1. Update `src/obd_v2/version.py`
2. Update `pyproject.toml` to match
3. Re-run build scripts

## Testing Built Applications

### Windows
```bash
# Test installer on clean system
# Run installer and verify:
# - Application launches correctly
# - All features work (connection, plugins, etc.)
# - Uninstaller removes all files
```

### macOS
```bash
# Test on both Intel and Apple Silicon if possible
# Verify:
# - Application launches without console
# - Gatekeeper accepts the app (if code signed)
# - All features work correctly
```

### Linux
```bash
# Test on multiple distributions
# Verify:
# - Desktop entry works
# - All dependencies are satisfied
# - Application functions correctly
```

## Troubleshooting

### Windows Build Issues
- **InnoSetup not found**: Install InnoSetup and add to PATH
- **Missing dependencies**: Ensure all requirements are installed
- **Permission errors**: Run as administrator
- **Python path issues**: Check embedded Python runtime path

### macOS Build Issues
- **PyInstaller fails**: Check for missing hidden imports
- **Editable install fails**: Upgrade tooling, then retry:
  `python3 -m pip install --upgrade pip setuptools wheel`
- **Code signing errors**: Ensure proper certificates installed
- **Universal binary issues**: Build on both architectures or use universal tools
- **Notarization failures**: Check entitlements and signing identity
- **`resources/projects.json not found or invalid` at startup**:
  Reinstall from repository root so package data is present:
  `python3 -m pip install --force-reinstall -e .`

### Linux Build Issues
- **Missing system dependencies**: Install development headers
- **Desktop entry not working**: Check paths and permissions
- **Virtual environment issues**: Ensure proper activation

## Advanced Configuration

### Custom Build Options
- **Branding**: Modify icons and splash screens
- **Dependencies**: Add/remove optional dependencies
- **Compression**: Adjust compression settings for installer size
- **Updates**: Configure automatic update mechanisms

### CI/CD Integration
Build scripts can be integrated into GitHub Actions or other CI/CD systems:
```yaml
# Example GitHub Actions workflow
- name: Build Windows Installer
  run: |
    cd setup_tools/inno-win-setup
    ISCC.exe wininstaller.iss

- name: Build macOS DMG
  run: |
    cd setup_tools/mac-os
    ./builddmg.sh
```

## Support

For build-related issues:
1. Check this documentation first
2. Review the main project README.md
3. Search existing GitHub issues
4. Create new issue with build logs and system information

## Contributing

When contributing build improvements:
1. Test on multiple platforms if possible
2. Update documentation for any changes
3. Ensure version synchronization
4. Follow existing code style and patterns