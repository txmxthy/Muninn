from common import eop
from common.util import *
from modules.Database import Database
from modules import Bots
from modules.Scan import Scan
import os


def run():
    if not eop.is_root():
        eop.root()

    while True:
        opts = {"Scanner": Scan.Controller, "Database": Database.Controller, "Bots": Bots.Controller}
        selection = options(opts, "Select")
        if not selection:
            break
        selection()
        clear()
        print_header("Muninn")
    exit_quote()
