from cx_Freeze import setup, Executable

setup(
    name = "Kalkulator",
    version = "1.1",
    description = "Kalkulator z funkcją przeliczania na liczby binarne",
    executables = [Executable("app1.py", base = "Win32GUI")]
)