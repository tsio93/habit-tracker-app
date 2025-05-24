; Inno Setup Script for Habit Tracker from dist folder

[Setup]
AppName=Habit Tracker
AppVersion=1.0
DefaultDirName={pf}\Habit Tracker
DefaultGroupName=Habit Tracker
UninstallDisplayIcon={app}\main.exe
OutputDir=C:\Users\tsio9\OneDrive\Desktop\Habbit_Tracker
OutputBaseFilename=HabitTrackerSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\tsio9\OneDrive\Desktop\Habbit_Tracker\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\tsio9\OneDrive\Desktop\Habbit_Tracker\dist\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Habit Tracker"; Filename: "{app}\main.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\Habit Tracker"; Filename: "{app}\main.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
