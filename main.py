from time import sleep
import os
import app
from common import eop
from common.util import print_header, vert_center, module_loaded

if __name__ == '__main__':

    app = app.App(db=False)
    module_loaded("Welcome to Muninn", sep="=")
    print_header(str(app), " ")
    app.run()
