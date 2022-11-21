#!/usr/bin/python
import os
import subprocess
path_from = os.path.join(os.getcwd() + '/' + 'dz1_1.py')
path_to = os.path.join(os.getcwd() + '/' + 'dz1_run.py')

subprocess.call(f'cp {path_from} {path_to}', shell=True)
subprocess.call(['sudo', '-S', 'chmod', '400', f'{path_to}'])
subprocess.call(['sudo', '-S', 'chmod', '500', f'{path_to}'])
subprocess.call(["python3", "dz1_run.py"])
