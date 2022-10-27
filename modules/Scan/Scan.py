from common.util import *
from nmap import nmap
from modules.Scan.Scanner import Scanner


def Controller(scanner=None):

    if scanner is None:
        module_loaded("New Scan")
        scanner = Scanner(hosts="127.0.0.1", ports=[22], args="-sV -O")
        print("Default Command: " + scanner.current_command)
    else:
        module_loaded("Scan with " + scanner.current_command)
    actions = {"Configure": scanner.Configure, "Run": scanner.Run}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    x = selection()
    if x == 1:
        Controller(scanner=scanner)





