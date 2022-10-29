import subprocess


from common.util import *


def controller(app, status):
    module_loaded("Database", app)
    actions = {"Configure": Configure, "Run": Run, "Init": init}
    selection = options(actions, "Select", "Select an action")
    if not selection:
        return
    selection()


def Configure():
    print("Configure")
    from pymetasploit3.msfrpc import MsfRpcClient
    client = MsfRpcClient('yourpassword', port=55552, ssl=True)
    mods = [m for m in dir(client) if not m.startswith('_')]
    print(mods)


    input("Press enter to continue")


def Run():
    print("Run")
    input("Press enter to continue")

def init():
    """
    Start the RPC server
    :return:
    """
    # Msfconsole
    #
    # This will start the RPC server on port 55552 as well as the Metasploit console UI
    #
    # $ msfconsole
    # msf> load msgrpc [Pass=yourpassword]

    # Run command

    # Spawn a new gnome shell
    # msf = subprocess.Popen(['gnome-terminal', '-e', 'msfconsole -q -x "load msgrpc Pass=yourpassword"'])


    input("Press enter to continue")