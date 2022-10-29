from pymetasploit3.msfrpc import MsfRpcClient
from common.util import *
from modules.Scan.Scanner import Scanner


def controller(app):
    module_loaded("Database", app=app)
    actions = {"Init": init, "Configure": Configure, "Run": Run}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    selection(app)
    return app


def Configure(app):
    module_loaded("Configure DB" + fa.icons['cog'], app=app)

    if input("Change the server settings? (y/n): ").lower() == "y":
        for key in app.rpc:
            if key is not "Client":
                app.rpc[key] = input(f"{key}: {app.rpc[key]}:")

    input("Press enter to continue")


def Run():
    print("Run")
    input("Press enter to continue")


def check_db_service(app):
    """
    Hard check with scanner through localhost
    :param app:
    :return:
    """
    os.system("msfdb")


def poll_db_status(app):
    if app.rpc["Client"] is not None:
        if app.rpc["Client"].db.status:
            return True
    return False


def check_msf_net_service(app):
    scanner = Scanner(hosts="127.0.0.1", ports=[app.rpc["Port"]], args="-sV -O")
    scanner.Run(app)


def init(app):
    """
    Run the rpc server
    :return:
    """

    def launch_server(app):
        os.system(f"msfrpcd -P {app.rpc['Pass']} {app.rpc['SSL']} -p {app.rpc['Port']}")

    def launch_db():
        os.system("systemctl start postgresql")
        os.system("msfdb init -n")

    # Load
    if app.rpc["Client"] is None:
        try:
            print("Connecting to RPC server....")
            app.rpc["Client"] = MsfRpcClient(app.rpc["Pass"], port=app.rpc["Port"], ssl=app.rpc["SSL"])
            app.rpc["Manager"] = app.rpc["Client"].consoles.console()
            app.db_status = True
        except Exception as e:
            print("Error: Could not Connect to RPC server")
            print("Attempting to start RPC Server...")
            launch_server(app)
            input("Launched: Press enter to proceed once the server is running...")
            app.rpc["Client"] = MsfRpcClient(app.rpc["Pass"], port=app.rpc["Port"], ssl=app.rpc["SSL"])
    # Print


    client: MsfRpcClient = app.rpc["Client"]
    mods = [m for m in dir(client) if not m.startswith('_')]
    print("Available Modules: " + str(mods))
    input("Press enter to continue")

    # List aux modules
    aux_mods = [m for m in client.modules.auxiliary if not m.startswith('_')]

    # Grep for db
    client.db.connect('msf', "yourpassword")
    print("Connected to DB")

    # Get stau
    print(client.db.status)
    print(client.db.workspaces)

    input("Press enter to continue")

    return app
