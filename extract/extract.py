import os
import tkinter as tk
from tkinter import filedialog
 
root = tk.Tk()
root.withdraw()

pw_path = 'passwd.txt'
file_path = filedialog.askopenfilename()
out_path = file_path[:file_path.find('.')]

if file_path == '':
    print('NO FILE, EXIT!')
else:
    with open(pw_path, 'r', encoding='utf-8') as f:
        res = f.readlines()

    pws = [x.strip() for x in res]

    for pw in pws:
        cmd = '7z e "%s" -p"%s" -o"%s" -y' % (file_path, pw, out_path)
        print(cmd)
        ret = os.system(cmd)
        if ret == 0:
            break

os.system('pause')