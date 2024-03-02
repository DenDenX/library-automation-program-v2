# Library Automation Program
An under development library automation program that writed in Python 3 with tkinter.

## The Modules Needed

- xlrd
- PIL
- sqlite3
- time
- datetime
- customtkinter

### For Linux
- `pip install xlrd Pillow sqlite3 time datetime customtkinter`

### For Windows
- `python -m pip install xlrd Pillow sqlite3 time datetime customtkinter`


## Convert to Executable File

### For Linux
- `pip install pyinstaller`
- `pyinstaller --onefile --hidden-import "PIL._tkinter_finder" --hidden-import "PIL.imagingtk" main_1.py`

### For Windows
- `python -m pip install PyInstaller`
- `python -m PyInstaller --onefile --hidden-import "PIL._tkinter_finder" --hidden-import "PIL.imagingtk" main_1.py`

#### Developers
- A. Genç
- E. E. Köroğlu
- Y. Karagöz
