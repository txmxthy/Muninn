import os

from common.deps.pymetasploit3.msfrpc import MsfRpcClient, MsfRpcMethod
import subprocess
import time


def poll_db_status(app):
    if app.rpc["Client"] is not None:
        if "db" in app.rpc["Client"].db.status:
            return True
    return False


def connect_to_msf(start_time, max_time, app, depth=0):
    try:
        client = MsfRpcClient(app.rpc["Pass"], port=int(app.rpc["Port"]))

    except Exception:
        if start_time + max_time > time.time():
            print("waiting for msfrpcd to start")
            time.sleep(5)
            return connect_to_msf(start_time, max_time, app=app, depth=depth + 1)
        else:
            raise TimeoutError("Could not connect to msfrpcd")
    return client


def client_status(client):
    print("Creating console")
    client.call(MsfRpcMethod.ConsoleCreate)
    print("\t" + "Console created")
    print("\t" + "Console id:", client.call(MsfRpcMethod.ConsoleList))


def connect_client(app):
    print("Client Connecting")
    try:
        client = MsfRpcClient(app.rpc["Pass"], port=int(app.rpc["Port"]))

    except:
        print("Starting msfrpcd")

        p = subprocess.Popen(["msfrpcd",
                              "-P", app.rpc["Pass"],
                              "-U", app.rpc["User"],
                              "-S", "-f",
                              "-p", app.rpc["Port"],
                              "-a", app.rpc["Host"]],
                             stdout=subprocess.PIPE)

        print("Polled:", p.poll())
        client = connect_to_msf(time.time(), 60, app=app)
        print("Polled:", p.poll())
    return client

def connect(app):
    app.rpc["Client"].db.connect(username=app.db["DbUser"],
                                 database=app.db["DbName"],
                                 host=app.db["DbHost"],
                                 port=app.db["DbPort"],
                                 password=app.db["DbPass"])
    return app
def connect_db(app):
    print("Setting up DB connection. This Takes a while.")

    if "db" not in app.rpc["Client"].db.status:
        # Get current file path
        path = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(path, "msfdb.sh")
        # Run script
        os.system(script)


    # Check cfg of server
    # os.system("cat /usr/share/metasploit-framework/config/database.yml")
    # Read password field from /usr/share/metasploit-framework/config/database.yml and set it to app.rpc["DbPass"]
    # file = "/usr/share/metasploit-framework/config/database.yml"
    file = "/home/kali/.msf4/database.yml"
    # Read
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "database" in line:
                app.db["DbName"] = line.split(": ")[1].strip()
            if "username" in line:
                app.db["DbUser"] = line.split(": ")[1].strip()
            if "password:" in line:
                app.db["DbPass"] = line.split(": ")[1].strip()
            if "host" in line:
                app.db["DbHost"] = line.split(": ")[1].strip()
            if "port" in line:
                app.db["DbPort"] = line.split(": ")[1].strip()
            if "pool" in line:
                break

    #
    print("CFG:", app.db)
    if "db" not in app.rpc["Client"].db.status:
        print("Launching DB")
        try:
            app = connect(app)
            if "db" not in app.rpc["Client"].db.status:


                newPort = int(app.db["DbPort"]) + 1
                print("Port doesn't match config, retrying with port:", newPort)
                print("Check against service and override if needed")
                os.system("ps aux | grep msf4")
                override = input("Input a port to override the new port if needed:")
                if override != "":
                    newPort = override
                app.db["DbPort"] = newPort
                app = connect(app)
            print(app.rpc["Client"].db.status)
        except Exception as e:
            app.error = e
            return app


        input("Press enter to continue")

    return app


def init(app):
    app.rpc["Client"] = connect_client(app)
    client_status(app.rpc["Client"])
    print("Client Connected")

    app = connect_db(app)
    print(app.rpc["Client"].db.workspaces.list)
    print(app.rpc["Client"].sessions.list)

    return app
