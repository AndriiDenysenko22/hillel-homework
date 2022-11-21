#!/usr/bin/python
import subprocess
import os
import random
from calendar import monthrange


print(subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])
current_dir = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE, universal_newlines=True).\
    communicate()[0].strip()
subprocess.Popen(["mkdir dz1"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
ba = subprocess.check_output(["date", "+%d-%m-%Y"])
mymonth = int(ba.decode().split('-')[1])
myyear = int(ba.decode().split('-')[2])

# a = datetime.date.today()


def allDays(y, m):
    for day in range(1, monthrange(y, m)[1] + 1):
        yield f'{day}-{m}-{y}'
        day += 1


days = []
for item in allDays(myyear, mymonth):
    days.append(item)
for day in days:
    subprocess.call(['touch', f'{current_dir}/dz1/{day}.log'])

subprocess.call(["sudo", "-S", "chown", "-R", "root", f"{current_dir}/dz1"])

subprocess.call(['pwd'])
subprocess.call(['cd', f'{current_dir}/dz1'], shell=True)
for i in range(5):
    name_2_delete = random.choice(os.listdir(f"{current_dir}/dz1"))
    subprocess.call([f"rm -rf {current_dir}/dz1/{name_2_delete}"], shell=True)
    i += 1
