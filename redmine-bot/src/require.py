import importlib

def check_and_install(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} not instaled, install...")
        try:
            import pip
            pip.main(['install', package])
        except AttributeError:
            import subprocess
            subprocess.check_call(['pip', 'install', package])
        print(f"{package} has been installed successfully.")
 
with open('requirements.txt','r') as req:
    for line in req: check_and_install(line.strip())
