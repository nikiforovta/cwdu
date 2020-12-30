#!/usr/bin/python3


def start():
    use_pool()
    print_dir_info(sum([sizes for names, sizes in files]))
    while True:
        key = input("\nEnter a command: ")
        result = action(key)
        if result == 0:
            break


def use_pool():
    pool = ThreadPool(cpu_count() + 1)
    file_list = os.listdir(os.getcwd())
    files[:] = []
    starting = time.time()
    pool.map(get_info, file_list)
    pool.close()
    pool.join()
    print(f"I spent {time.time() - starting} s to get directory info")


def get_info(f):
    try:
        if os.path.exists(f):
            if os.path.isfile(f):
                fp = os.path.join(os.getcwd(), f)
                info = (f, os.path.getsize(fp))
                files.append(info)
            elif os.path.isdir(f):
                dir_size = 0
                for dirpath, dirnames, filenames in os.walk(f):
                    for filein in filenames:
                        fp = os.path.join(dirpath, filein)
                        if not os.path.islink(fp):
                            dir_size += os.path.getsize(fp)
                info = (f, dir_size)
                files.append(info)
    except (PermissionError, FileNotFoundError, OSError):
        pass


def print_dir_info(total_size):
    out.clear_rows()
    out.add_row([">", f"{os.getcwd()}", f"{total_size}", ""])
    if os.path.dirname(os.path.dirname(os.getcwd())) != os.getcwd():
        out.add_row(["1", "..", "", ""])
    for i in range(len(files)):
        out.add_row([f"{i + 2}", f"{files[i][0]}", f"{files[i][1]}", f"{files[i][1] / total_size * 100:,.2f}"])
    print(out)


def print_help():
    print('\ncwdu Course Work Disk Usage 2020')
    print('List of options:\n')
    print('h - open/close Help (wow!)')
    print('q - quit the program')
    print('1+ - change directory')
    key = input("\nEnter a command: ")
    if key == "q":
        return 0
    elif key == "h":
        print_dir_info(sum([sizes for names, sizes in files]))


def action(key):
    global threads
    if key == "h":
        return print_help()
    elif key == "q":
        return 0
    else:
        try:
            dirch = int(key)
            if dirch == 1 and os.path.dirname(os.path.dirname(os.getcwd())) != os.getcwd():
                os.chdir('..')
                use_pool()
                print_dir_info(sum([sizes for names, sizes in files]))
            elif 2 <= dirch < len(files) + 2:
                p = files[dirch - 2][0]
                if os.path.isdir(p):
                    try:
                        os.chdir(p)
                        use_pool()
                    except PermissionError:
                        print("You don't have permission to go there =(")
                    finally:
                        print_dir_info(sum([sizes for names, sizes in files]))
        except ValueError:
            pass


if __name__ == '__main__':
    import os
    import time
    from multiprocessing import Manager, cpu_count
    from multiprocessing.dummy import Pool as ThreadPool

    from prettytable import PrettyTable

    manager = Manager()
    files = manager.list([])
    out = PrettyTable()
    out.title = 'cwdu Course Work Disk Usage 2020'
    out.field_names = [' ', '', 'Size in bytes', 'Size in %']
    out.align["Size in bytes"] = "c"
    out.align["Size in %"] = "c"
    start()
