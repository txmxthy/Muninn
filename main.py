from time import sleep

import app
from common import eop
from common.util import print_header, vert_center, module_loaded

if __name__ == '__main__':

    if not eop.is_root():
        vert_center("Please Run as Root. Required for scanner")
    else:
        module_loaded("Welcome to Muninn", sep="=")


    app.run()