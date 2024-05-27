import subprocess

# Lista de archivos a ejecutar
scripts = ['vcardGen.py', 'vcardGenV2.py', 'vcardGenV3.py']

for script in scripts:
    print (f"Generando {script}")
    subprocess.run(['python', script])