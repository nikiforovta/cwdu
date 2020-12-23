import os
import time

from prettytable import PrettyTable

files = []
out = PrettyTable()
out.title = 'cwdu Course Work Disk Usage 2020'
out.field_names = [' ', '', 'Size in bytes', 'Size in %']
out.align["Size in bytes"] = "c"
out.align["Size in %"] = "c"


def start():
    dir_info()
    while True:
        key = input("\nEnter a command: ")
        result = action(key)
        if result == 0:
            break


def dir_info():
    files.clear()
    out.clear_rows()
    file_list = os.listdir(os.getcwd())
    start_time = time.time()
    for f in file_list:
        if os.path.exists(f):
            if os.path.isfile(f):
                fp = os.path.join(os.getcwd(), f)
                try:
                    info = (f, os.path.getsize(fp))
                    files.append(info)
                except PermissionError:
                    pass
            elif os.path.isdir(f):
                try:
                    dir_size = 0
                    for dirpath, dirnames, filenames in os.walk(f):
                        for filein in filenames:
                            fp = os.path.join(dirpath, filein)
                            if not os.path.islink(fp):
                                dir_size += os.path.getsize(fp)
                    info = (f, dir_size)
                    files.append(info)
                except (PermissionError, OSError):
                    pass
    print(f"I spent {time.time() - start_time} s to get directory info")
    size = sum([sizes for names, sizes in files])
    out.add_row([">", f"{os.getcwd()}", f"{size}", ""])
    if os.path.dirname(os.path.dirname(os.getcwd())) != os.getcwd():
        out.add_row(["1", "..", "", ""])
    for i in range(len(files)):
        out.add_row([f"{i + 2}", f"{files[i][0]}", f"{files[i][1]}", f"{files[i][1] / size * 100:,.2f}"])
    print(out)


def print_help():
    print('\ncwdu Course Work Disk Usage 2020')
    print('List of options:\n')
    print('h - open/close Help (wow!)')
    print('q - quit the program\n1+ - change directory')
    key = input("\nEnter a command: ")
    if key == "q":
        return 0
    elif key == "h":
        dir_info()


def action(key):
    if key == "h":
        return print_help()
    elif key == "q":
        return 0
    else:
        try:
            dirch = int(key)
            if dirch == 1 and os.path.dirname(os.path.dirname(os.getcwd())) != os.getcwd():
                os.chdir('..')
                dir_info()
            elif 2 <= dirch < len(files) + 2:
                p = files[dirch - 2][0]
                if os.path.isdir(p):
                    try:
                        os.chdir(p)
                    except PermissionError:
                        pass
                    dir_info()
        except ValueError:
            pass


if __name__ == '__main__':
    start()
