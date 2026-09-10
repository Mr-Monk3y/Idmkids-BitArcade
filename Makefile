run:
	python src\main.py
exe:
	pyinstaller --clean --onefile --windowed --icon "src/assets/icono.ico" --add-data "src/assets;assets" --name BitArcade src/main.py