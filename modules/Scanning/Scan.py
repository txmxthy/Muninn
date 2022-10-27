from common.util import *
from nmap import nmap
from modules.Scanning.Scanner import Scanner


def Controller(scanner=None):

    if scanner is None:
        module_loaded("New Scan")
    else:
        module_loaded("Scan with " + scanner.current_command)
    scanner = Scanner(hosts="127.0.0.1", ports=[22])
    actions = {"Configure": scanner.Configure, "Run": scanner.Run}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    x = selection()
    if x == 1:
        Controller(scanner=scanner)





