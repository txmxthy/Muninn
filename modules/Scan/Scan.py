from common.util import *
from nmap import nmap
from modules.Scan.Scanner import Scanner


def controller(app, scanner=None):
    if scanner is None:
        module_loaded("New Scan", app=app)
        scanner = Scanner(hosts="192.168.86.66", args="-sV -O --osscan-limit --osscan-guess -F")
        print("Default Command: " + scanner.current_command)
    else:
        module_loaded("Scan", app=app)
        print("Scan Command: " + scanner.current_command)
    actions = {"Configure": scanner.Configure, "Run": scanner.Run}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    app = selection(app)
    if app.flag == 1:
        print("Flag set to 1")
        controller(scanner=scanner, app=app)

    app.flag = 0
    return app





