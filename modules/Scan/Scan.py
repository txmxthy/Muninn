from common.util import *
from nmap import nmap
from modules.Scan.Scanner import Scanner


def controller(app, scanner=None):
    if scanner is None:
        module_loaded("New Scan", status=app.status)
        scanner = Scanner(hosts="127.0.0.1", ports=[22], args="-sV -O")
        print("Default Command: " + scanner.current_command)
    else:
        module_loaded("Scan", status=app.status)
        print("Scan Command: " + scanner.current_command)
    actions = {"Configure": scanner.Configure, "Run": scanner.Run}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    s = selection()
    if s == 1:
        controller(scanner=scanner, app=app)

    return app





