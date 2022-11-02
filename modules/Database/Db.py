from time import sleep

from pymetasploit3.msfrpc import MsfRpcClient, MsfRpcMethod
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

        command = f"msfrpcd -P {app.rpc['Pass']} -p {app.rpc['Port']}"
        print("Running", command)
        launch_db()
        os.system(command)

    def launch_db():
        os.system("systemctl start postgresql")
        os.system("msfdb init -a 127.0.0.1 -p 5433 ")
        os.system("msfdb start")

    # Load
    if app.rpc["Client"] is None:
        use_ssl = False
        if app.rpc["SSL"] is not None:
            use_ssl = True
        try:
            print("Connecting to RPC server....")
            app.rpc["Client"] = MsfRpcClient(password=app.rpc["Pass"],
                                             server="0.0.0.0",
                                             port=app.rpc["Port"],
                                             ssl=use_ssl)
        except Exception as e:
            print("Error: Could not Connect to RPC server")
            print("Attempting to start RPC Server...")
            launch_server(app)
            input("Launched: Press enter to proceed once the server is running...")
            app.rpc["Client"] = MsfRpcClient(password=app.rpc["Pass"],
                                             server="0.0.0.0",
                                             port=app.rpc["Port"],
                                             ssl=use_ssl)
    # Print

    client: MsfRpcClient = app.rpc["Client"]
    dbname = "msf"
    dbhost = "127.0.0.1"
    dbport = "5433"
    dbpasswd = app.rpc["Pass"]
    dbusr = "msf"

    db_cfg = [dbname, dbhost, dbport, dbpasswd, dbusr]

    if 'db' not in client.db.status:
        client.db.connect(
            username=dbusr,
            database=dbname,
            host=dbhost,
            port=dbport,
            password=dbpasswd
        )

    print(client.db.status)

    # Create default workspace
    client.call(MsfRpcMethod.DbAddWorkspace, "TEST")
    # workspace_list = client.db.workspaces.add("TEST")
    workspace_list = client.call(MsfRpcMethod.DbWorkspaces)
    print("LIST ", workspace_list)


    input("Press enter to continue")

    return app

def add_host(app):
    client: MsfRpcClient = app.rpc["Client"]
    client.db.workspaces.workspace('default').hosts.report(host='1.1.1.2')
    hosts = client.db.workspaces.workspace.hosts.list
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
