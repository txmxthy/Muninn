from common.util import *
from modules import Database, Bots
from modules.Scanning import Scan


def run():
    while True:
        opts = {"Scanner": Scan.Controller, "Database": Database.Controller, "Bots": Bots.Controller}
        selection = options(opts, "Select")
        if not selection:
            break
        selection()
        clear()
        print_header("Muninn")
    exit_quote()
