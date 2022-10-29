from common import eop
from common.util import *
from modules.Database import Database
from modules import Bots
from modules.Scan import Scan
import fontawesome as fa
import os


def handle_error(app):
    """
    Handle errors with options to debug
    :param app:
    :return:
    """
    module_loaded("Caught Error!")
    print("Caught Error!")
    print_header(str(app.error), sep=" ")
    app.error = "Caught"

    if app.debug:
        # Dump fields
        print("Dumping Fields")
        for field in app.__dict__:
            print(fa.icons["arrow-right"] + " " + field + ": " + str(app.__dict__[field]))

    app.error = None
    print("Clearing Error...")
    input("Press enter to continue...")


class App:
    def __init__(self, db):
        self.db_status = db
        self.text = None
        self.root = eop.is_root()
        self.error = None
        self.flag = None
        self.debug = False

    def __repr__(self):
        db_status = "DB: " + ("ON" if self.db_status else "OFF")
        return f"{db_status} | Err: {self.error}"

    def __str__(self):
        return self.__repr__()

    def toggle_debug(self, _):
        self.debug = not self.debug
        print(f"Debug Mode: {self.debug}")
        input("Press enter to continue...")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def run(self):
        if not self.root:
            eop.root()

        while True:
            opts = {"Scanner": Scan.controller,
                    "Database": Database.controller,
                    "Bots": Bots.controller,
                    "Toggle Debug": self.toggle_debug,
                    "Error Demo": Scan.Scanner.format_args}
            selection = options(opts, "Select")
            if not selection:
                break
            selection(self)
            # try:
            #     selection(self)
            # except Exception as e:
            #     self.update(error=e)
            #     handle_error(app=self)
            clear()
            print_header(fa.icons["eye"] + " Muninn", app=self)
        exit_quote()
