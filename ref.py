#!/usr/bin/python3


def get_info(f):
    try:
        if os.path.exists(f):
            if os.path.isfile(f):
                fp = os.path.join(os.getcwd(), f)
                file_info = (f, os.path.getsize(fp))
                files.append(file_info)
            elif os.path.isdir(f):
                dir_size = 0
                for dirpath, dirnames, filenames in os.walk(f):
                    for filein in filenames:
                        fp = os.path.join(dirpath, filein)
                        if not os.path.islink(fp):
                            dir_size += os.path.getsize(fp)
                file_info = (f, dir_size)
                files.append(file_info)
    except (PermissionError, FileNotFoundError):
        pass


if __name__ == '__main__':
    import operator
    import os
    import time
    from multiprocessing import Manager
    from multiprocessing.dummy import Pool as ThreadPool

    manager = Manager()
    files = manager.list([])
    res = ([])
    for i in range(1, 101):
        for _ in range(3):
            os.chdir('..')
            pool = ThreadPool(i)
            fileslist = os.listdir(os.getcwd())
            files[:] = []
            start = time.time()
            pool.map(get_info, fileslist)
            pool.close()
            pool.join()
            timed = time.time() - start
            print(f"{i} threads: {timed} s")
            info = (i, timed)
            res.append(info)
            os.chdir("./cwdu")

    res.sort(key=operator.itemgetter(1))
    print(res[:50])
