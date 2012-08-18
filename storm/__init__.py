"""
Provides an interface for desktop foam rocket launchers

For now this module is only being tested on the Dream Cheeky Storm
O.I.C Missle Launcher, however it should work on similar hardware. 
"""
import subprocess

def version():
    release = '0.1'
    p = subprocess.Popen('git describe --tags 2> /dev/null',
        shell=True,
        stdout=subprocess.PIPE)
    if p.wait() != 0:
        return release
    return p.stdout.read().strip('\n ')

if __name__ == '__main__':
    print version()
