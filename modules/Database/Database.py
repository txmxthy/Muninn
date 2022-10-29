from pymetasploit3.msfrpc import MsfRpcClient
from common.util import *
from modules.Database import Db
from modules.Scan.Scanner import Scanner


def controller(app):
    module_loaded("Database", app=app)

    if not app.db_status:
        warn("Database is not running")
        actions = {"Init": Db.init, "Configure": Configure}
        selection = options(actions, "Select", "Select an action")
        if not selection:
            return
        selection(app)
    else:
        explore(app)

    return app


def Configure(app):
    module_loaded("Configure DB" + fa.icons['cog'], app=app)

    if input("Change the server settings? (y/n): ").lower() == "y":
        for key in app.rpc:
            if key is not "Client":
                app.rpc[key] = input(f"{key}: {app.rpc[key]}:")

    input("Press enter to continue")


def explore(app):
    actions = {"List Hosts": Db.list_hosts,
               "Add Host":Db.add_host}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    selection(app)



