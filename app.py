from common import eop
from common.util import *
from modules.Database import Database
from modules.Database.Db import poll_db_status
from modules.Scan import Scan
import fontawesome as fa
import os


def handle_error(app):
    """
    Handle errors with options to debug
    :param app:
    :return:
    """
    module_loaded("Caught Error!", app=app)
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
        self.rpc = {"Client": None,
                    "Host": "127.0.0.1",
                    "Port": "55553",
                    "Pass": "yourpassword",
                    "User": "msf",
                    }
        self.db = {}

    def __repr__(self):
        self.db_status = poll_db_status(self)
        db_status = "DB: " + (fa.icons["check"] if self.db_status else fa.icons["times"])
        error = "Status: " + (fa.icons["thumbs-down"] if self.error else fa.icons["thumbs-up"])
        debug = (" | " + fa.icons["bug"] if self.debug else "")
        return f"{db_status} | {error} {debug}"

    def __str__(self):
        return self.__repr__()

    def toggle_debug(self, _):
        self.update(debug=not self.debug)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def run(self):
        if not self.root:
            vert_center("Please run as root")
            eop.root()

        while True:
            opts = {"Setup": auto_setup,
                    "Scanner": Scan.controller,
                    "System": Database.controller,
                    "Toggle Debug": self.toggle_debug,
                    "Error Demo": Scan.Scanner.format_args}
            selection = options(opts, "Select")
            if not selection:
                break

            try:
                selection(self)
                if self.error:
                    handle_error(self)
            except Exception as e:
                self.update(error=e)
                handle_error(app=self)

            module_loaded(fa.icons["eye"] + " Muninn", app=self)
        exit_quote()


def auto_setup(app):
    """
    Auto setup
    :return:
    """
    print("Auto setup")
    Database.Db.init(app)
    return app
