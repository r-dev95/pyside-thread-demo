# build ui
pyside6-uic.exe .\lib\components\layout.ui -o .\lib\components\layout.py

# fix import
(Get-Content .\lib\components\layout.py) -replace 'import resources_rc', 'import lib.components.resources_rc' | Set-Content .\lib\components\layout.py