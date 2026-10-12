# -*- mode: python ; coding: utf-8 -*-

# OBD-V2 PyInstaller specification for macOS
# Supports both Intel and Apple Silicon (M1/M2) architectures

import os
import sys

# Add the project root to the path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Core application files
main_script = os.path.join(project_root, 'src', 'obd_v2', 'main.py')

# Data files to include
datas = [
    # Icons and resources
    (os.path.join(project_root, 'resources', 'icons'), 'resources/icons'),
    
    # Translation files
    (os.path.join(project_root, 'locales'), 'locales'),
    
    # Plugin files
    (os.path.join(project_root, 'src', 'obd_v2', 'plugins'), 'ddtplugins'),
    
    # Style files
    (os.path.join(project_root, 'resources', 'styles'), 'resources/styles'),
    
    # Documentation
    (os.path.join(project_root, 'license.txt'), '.'),
    (os.path.join(project_root, 'README.md'), '.'),
]

# Add QSS files explicitly
styles_dir = os.path.join(project_root, 'resources', 'styles')
if os.path.exists(styles_dir):
    for file in os.listdir(styles_dir):
        if file.endswith('.qss'):
            datas.append((os.path.join(styles_dir, file), 'resources/styles'))

a = Analysis(
    [main_script],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # PyQt5 modules
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'PyQt5.QtNetwork',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtSvg',
        'PyQt5.QtWebEngineWidgets',
        
        # Serial communication
        'serial',
        'serial.tools',
        'serial.tools.list_ports',
        
        # USB support
        'usb',
        'usb.core',
        'usb.util',
        
        # Cryptographic functions
        'crcmod',
        'crcmod.crcmod',
        
        # Platform-specific modules
        'platform',
        'subprocess',
        'threading',
        'queue',
        'json',
        'xml.etree.ElementTree',
        'xml.dom.minidom',
        
        # OBD-V2 specific modules
        'ecu',
        'elm',
        'options',
        'parameters',
        'dataeditor',
        'displaymod',
        'sniffer',
        'uiutils',
        'usbdevice',
        'version',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce bundle size
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'cv2',
        'jupyter',
        'notebook',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OBD-V2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',  # Support both Intel and Apple Silicon
    codesign_identity=None,  # Set to your Developer ID for distribution
    entitlements_file='entitlements.plist',  # Use entitlements for hardware access
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OBD-V2',
)

app = BUNDLE(
    coll,
    name='OBD-V2.app',
    icon=os.path.join(project_root, 'resources', 'icons', 'obd.icns'),
    bundle_identifier='com.github.sgtpoebeltrupp.obd-v2',
    version='3.0.7',
    info_plist={
        'CFBundleName': 'OBD-V2',
        'CFBundleDisplayName': 'OBD-V2 Diagnostic Tool',
        'CFBundleShortVersionString': '3.0.7',
        'CFBundleVersion': '3.0.7',
        'CFBundleExecutable': 'OBD-V2',
        'CFBundleIdentifier': 'com.github.sgtpoebeltrupp.obd-v2',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'DDT4',
        'LSMinimumSystemVersion': '10.13.0',  # macOS High Sierra minimum
        'LSApplicationCategoryType': 'public.app-category.developer-tools',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        'NSHumanReadableCopyright': 'Copyright ©2026 OBD-V2',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeExtensions': ['ddt'],
                'CFBundleTypeName': 'OBD-V2 Project File',
                'CFBundleTypeRole': 'Editor',
                'LSHandlerRank': 'Owner',
            }
        ],
        # Hardware access permissions
        'NSBluetoothAlwaysUsageDescription': 'OBD-V2 needs Bluetooth access to communicate with OBD adapters.',
        'NSBluetoothPeripheralUsageDescription': 'OBD-V2 needs Bluetooth access to communicate with OBD adapters.',
        'NSLocationWhenInUseUsageDescription': 'OBD-V2 may use location services for enhanced diagnostic features.',
        'NSUSBDeviceUsageDescription': 'OBD-V2 needs USB access to communicate with OBD adapters.',
    },
)
