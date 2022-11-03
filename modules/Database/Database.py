from common.util import *
from modules.Database import Db
from modules.Database.Db import poll_db_status
from modules.Database.manager import host_icon, services_by_host, run_exploits


def controller(app):
    module_loaded("Database", app=app)

    if not poll_db_status(app):
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
    top_exploits = ["exploit/windows/smb/ms17_010_eternalblue",
                    "exploit/windows/smb/ms17_010_psexec",
                    "exploit/windows/postgres/postgres_payload"]

    module_loaded("Explore " + fa.icons['database'], app=app)

    hosts = app.rpc["Client"].db.workspaces.workspace('default').hosts.list

    actions = {}
    for i, host in enumerate(hosts):
        name = (f"{host_icon(host['name'])} {host['os_name']} at {host['address']}")
        actions[name] = host

    selection = options(actions, "Select", "Select an action")
    if not selection:
        return

    print("explore or exploit?")
    opts = {"Explore": services_by_host, "Exploit": run_exploits}
    Mode = options(opts, "Mode", "Select Mode")

    if not Mode:
        return

    Mode(app, selection, top_exploits)

