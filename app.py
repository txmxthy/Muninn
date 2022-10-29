from common import eop
from common.util import *
from modules.Database import Database
from modules import Bots
from modules.Scan import Scan
import os


class App:
    def __init__(self, db):
        self.db = db
        self.text = None
        self.root = eop.is_root()
        self.error = None

    def __repr__(self):
        db_status = "DB: " + ("ON" if self.db else "OFF")
        return f"{db_status} | Scan: {self.text}"

    def __str__(self):
        return self.__repr__()

    def status(self):
        d = {"db": self.db,
             "error": self.error,
             "text": self.text}
        return d

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
    def run(self):
        if not self.root:
            eop.root()

        while True:
            opts = {"Scanner": Scan.controller, "Database": Database.controller, "Bots": Bots.controller}
            selection = options(opts, "Select")
            if not selection:
                break
            updated = selection(self)
            clear()
            print_header("Muninn")
        exit_quote()
