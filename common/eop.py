import errno
import os
import sys


def is_root():
    return os.getuid() == 0


def root(graphical=True):
    if is_root():
        return
    sys.argv[0] = (os.getcwd() + "/" + sys.argv[0])
    args = [sys.executable] + sys.argv

    commands = []

    if graphical and sys.platform.startswith("linux") and os.environ.get("DISPLAY"):
        commands.append(["pkexec"] + args)
        commands.append(["gksudo"] + args)
        commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)

    for args in commands:
        try:
            os.execlp(args[0], *args)
        except OSError as e:
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
