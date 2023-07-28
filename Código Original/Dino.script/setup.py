import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("Dino.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = ["pygame","sys","random","pickle"],
        include_files = ["./Dino_Functions.py","./Dino_Sprites.py","./Imagens/SpriteSheet.png","./Sons/Death.wav","./Sons/Jump.wav","./Sons/Score.wav"],
        excludes = []
)




setup(
    name = "Dino Game",
    version = "2.0",
    description = "Dino Game refeito",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
