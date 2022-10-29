from pymetasploit3.msfrpc import MsfRpcClient
from common.util import *
from modules.Scan.Scanner import Scanner


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


def can_access_server(app):
    if not poll_db_status(app):
        app.error("Database not connected")
        print("Database not connected")

    elif app.rpc["Client"] is None:
        app.error("Client not configured")
        print("Client not configured")
    input("Press enter to continue")

    return app


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
    client.db.connect('msf', "yourpassword")

    print("Connected to DB")
    input("Press enter to continue")

    return app

def add_host(app):
    client: MsfRpcClient = app.rpc["Client"]
    client.db.workspaces.workspace('default').hosts.report(host='1.1.1.2')
    hosts = client.db.workspaces.workspace('default').hosts.list
    host_found = False
    for d in hosts:
        if d['address'] == '1.1.1.2':
            host_found = True
            break
    assert host_found == True


def list_hosts(app):
    """
    List all hosts in the database
    :return:
    """
    can_access_server(app)
    if app.error:
        return app


    workspace = "default"
    client: MsfRpcClient = app.rpc["Client"]
    workspace_hosts = client.db.workspaces.add("TEST")
    print_header(f"Workspace: {workspace} Hosts", sep=" ")
    for host in workspace_hosts:
        print(fa.icons["server"] + " " + host["address"])
