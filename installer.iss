[Setup]
AppName=Мой Кликер
AppVersion=1.0
DefaultDirName={autopf}\MyClickerGame
DefaultGroupName=Мой Кликер
UninstallDisplayIcon={app}\main.exe
OutputDir=Output
OutputBaseFilename=ClickerSetup
Compression=lzma
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на Рабочем столе"; GroupDescription: "Дополнительно:"

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Мой Кликер"; Filename: "{app}\main.exe"
Name: "{autodesktop}\Мой Кликер"; Filename: "{app}\main.exe"; Tasks: desktopicon
