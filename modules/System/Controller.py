from typing import Any

from common.deps.pymetasploit3.msfrpc import MsfRpcClient, SessionManager
from common.util import module_loaded, print_header, options
import fontawesome as fa


def ListSessions(app):
    """"
    List active sessions
    """
    app.rpc["Client"]: MsfRpcClient
    manager: SessionManager = app.rpc["Client"].sessions
    sessions: dict = manager.list
    return sessions


def sid_logic(app, host):
    active: dict = ListSessions(app)
    active_sids = [int(key) for key in active.keys()]
    app_exploits: dict = app.exploits
    app_sids = [sid for sid in app.exploits[host]]
    # if in active_sids but not in app_sids
    not_found = [sid for sid in active_sids if sid not in app_sids]
    # if in app_sids but not in active_sids
    not_active = [sid for sid in app_sids if sid not in active_sids]
    # if in app_sids and in active_sids
    found = [sid for sid in app_sids if sid in active_sids]
    return found, app_sids, active_sids, not_active, not_found


def list_successful(app, host, found):
    opts = {}
    for sid in found:
        name = f"Session: {sid} + {app.exploits[host][sid][0]}"
        opts[name] = sid
    selection: Any | None = options(opts, "Select", "Select a session")
    if not selection:
        return
    return app, selection


def Controller(app, exploited=None, sid=None):
    """"
    Activate meterpreter sessions and control system
    """
    ico = ""
    if exploited is not None:
        ico = " " + fa.icons["plug"] + " "
        if sid is None:
            ico += sid

    module_loaded("Session Controller" + ico, app=app)
    # app_sids, active_sids, not_active, not_found = sid_logic(app)

    if exploited:
        found, app_sids, active_sids, not_active, not_found = sid_logic(app, exploited)

        print(f"{fa.icons['check']} Found {len(found)} active sessions for {exploited}")

        if sid is None:
            app, sid = list_successful(app, exploited, found)

        fullname = app.exploits[exploited][sid][0]
        state = app.exploits[exploited][sid][1]
        print(f"using Session {sid} with {fullname}")


        return app

    else:
        if app.exploits == {}:
            print(f"{fa.icons['exclamation-triangle']} No sessions recorded.")
            return

        opts = {}
        for host, body in app.exploits.keys(), app.exploits.values():
            name = f"Host: {host}"
            opts[name] = host
        selection = options(opts, "Select", "Select a host")
        if not selection:
            return
        app = Controller(app, selection)

    input("Press enter to continue")
    return app
