import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Chat Noise 0.11",
        version = "0.11",
        description = "Electric Boogaloo Chat Noise Client",
        options = {"build_exe": build_exe_options},
        executables = [Executable("NewBoogaloo.py", base=base,icon=r"C:\Users\InventorX\Desktop\chaticon.ico")])