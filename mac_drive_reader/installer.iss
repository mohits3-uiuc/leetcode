; ─────────────────────────────────────────────────────────────────────
;  Mac Drive Reader – Inno Setup Script
;  Single-page, one-click installer (no wizard pages shown to the user)
;
;  Build:  ISCC.exe installer.iss   (or build.bat)
; ─────────────────────────────────────────────────────────────────────

#define AppName      "Mac Drive Reader"
#define AppVersion   "1.0.0"
#define AppPublisher "mohits3-uiuc"
#define AppURL       "https://github.com/mohits3-uiuc/leetcode"
#define AppExeName   "MacDriveReader.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

; ── Output ────────────────────────────────────────────────────────────
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=dist
OutputBaseFilename=MacDriveReader_Setup
SetupIconFile=assets\icon.ico

; ── One-page experience: hide every wizard page except the progress ───
DisableWelcomePage=no          ; show a single welcome/install page
DisableDirPage=yes             ; no "where to install" page
DisableProgramGroupPage=yes    ; no "Start Menu group" page
DisableReadyPage=yes           ; no "Ready to install" confirmation page
DisableFinishedPage=no         ; show "Finished" page with Launch button

; ── Appearance ────────────────────────────────────────────────────────
WizardStyle=modern
WizardSizePercent=100
WizardResizable=no

; ── Compression ───────────────────────────────────────────────────────
Compression=lzma2/ultra64
SolidCompression=yes

; ── Privileges ────────────────────────────────────────────────────────
; Admin required to access physical drives on Windows
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; ── Minimum Windows version: Windows 10 ──────────────────────────────
MinVersion=10.0

; ── Auto-launch after install ─────────────────────────────────────────
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
english.WelcomeLabel1=Install Mac Drive Reader
english.WelcomeLabel2=This will install Mac Drive Reader %1 on your computer.%n%nClick Install to continue.
english.ButtonInstall=Install

; Override wizard button label to say "Install" on the welcome page
[Messages]
english.WizardReady=Ready
english.ReadyLabel1=Click Install to begin installation.
english.ButtonNext=Install

[Files]
; Main executable (single .exe, all dependencies bundled)
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Assets
Source: "assets\*"; DestDir: "{app}\assets"; \
        Flags: ignoreversion recursesubdirs createallsubdirs; \
        Check: DirExists(ExpandConstant('{src}\assets'))

; README
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu
Name: "{group}\{#AppName}";           Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
; Desktop
Name: "{autodesktop}\{#AppName}";    Filename: "{app}\{#AppExeName}"

[Run]
; Launch the app immediately after installation finishes
Filename: "{app}\{#AppExeName}";
  Description: "Launch {#AppName}";
  Flags: nowait postinstall skipifsilent runasoriginaluser

[UninstallRun]
; Nothing extra to clean up – single .exe, no registry entries

[Code]
// Customise the welcome page button text to "Install" instead of "Next"
procedure InitializeWizard;
begin
  WizardForm.NextButton.Caption := 'Install';
  WizardForm.WelcomeLabel2.Caption :=
    'This will install Mac Drive Reader ' + '{#AppVersion}' + ' on your computer.' +
    #13#10 + #13#10 +
    'Supports: APFS  •  HFS+  •  HFS  •  exFAT  •  FAT32' +
    #13#10 + #13#10 +
    'Click Install to continue.';
end;

  Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
