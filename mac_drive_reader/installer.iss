; ─────────────────────────────────────────────────────────────────
;  Mac Drive Reader – Inno Setup Script
;  Produces a professional Windows installer (.exe)
;
;  Prerequisites:
;    - Build the .exe first with build.bat
;    - Inno Setup 6: https://jrsoftware.org/isdl.php
;
;  Compile:
;    ISCC.exe installer.iss
;    (or open in Inno Setup IDE and press Ctrl+F9)
; ─────────────────────────────────────────────────────────────────

#define AppName      "Mac Drive Reader"
#define AppVersion   "1.0.0"
#define AppPublisher "Your Name"
#define AppURL       "https://github.com/mohits3-uiuc/leetcode"
#define AppExeName   "MacDriveReader.exe"

[Setup]
; Basic info
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

; Output
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=dist
OutputBaseFilename=MacDriveReader_Setup
SetupIconFile=assets\icon.ico

; Appearance
WizardStyle=modern
Compression=lzma
SolidCompression=yes

; Privileges — Admin needed to access physical drives
PrivilegesRequired=admin

; Minimum Windows version: Windows 10
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";  Description: "{cm:CreateDesktopIcon}"; \
      GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunch"; Description: "Create a Quick Launch shortcut"; \
      GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable (built by PyInstaller)
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Any bundled assets
Source: "assets\*"; DestDir: "{app}\assets"; \
        Flags: ignoreversion recursesubdirs createallsubdirs

; README
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu shortcut
Name: "{group}\{#AppName}";          Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional, only if task ticked)
Name: "{autodesktop}\{#AppName}";    Filename: "{app}\{#AppExeName}"; \
      Tasks: desktopicon

[Run]
; Offer to launch the app after install
Filename: "{app}\{#AppExeName}"; \
  Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; \
  Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
