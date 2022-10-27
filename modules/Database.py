from common.util import *


def Controller():
    module_loaded("Database")
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