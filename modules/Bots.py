from common.util import *


def controller(app):
    module_loaded("Bots", app)
    actions = {"Configure": Configure, "Run": Run}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    selection()


def Configure():
    print("Configure")
    input("Press enter to continue")


def Run():
    print("Run")
    input("Press enter to continue")