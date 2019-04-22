from multiprocessing import Process

import os

def run_porc(name):
    print('Run child process %s (%s) ...' %(name, os.getpid()))


if __name__ == '__main__':
    # print('Parent process %s.' % os.getpid())
#     # p = Process(target=run_porc('test'))
#     # print('Child process will start.')
#     # p.start()
#     # p.join()
#     # print('Child process end.')
    import subprocess

    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)