pyinstaller --windowed --clean --noconsole Pythonics_Unix.spec 
cp all_mine dist/Pythonics
cp libxmr-stak-backend.a dist/Pythonics
cp libxmr-stak-c.a dist/Pythonics
mkdir dist/Pythonics/translations
cp translations/*.qm dist/Pythonics/translations
cp translations/*.png dist/Pythonics/translations
mkdir dist/Pythonics/images
cp images/*.png dist/Pythonics/images

cp LICENSE dist/Pythonics
cp pools.txt dist/Pythonics
cp config.txt dist/Pythonics
cp cpu.txt dist/Pythonics
