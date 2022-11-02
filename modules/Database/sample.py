from time import sleep

fromcommon.deps.pymetasploit3.msfrpc import MsfRpcClient, MsfRpcMethod
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


def init(app):
    """
    Run the rpc server
    :return:
    """
    s = None
    clhost = app.rpc["Host"]
    clport = app.rpc["Port"]
    clpasswd = app.rpc["Pass"]
    clusr = "msf"

    cl_cfg = [clhost, clport, clusr]

    s = MsfRpcClient(password=clpasswd, server=cl_cfg[0], port=cl_cfg[1], username=cl_cfg[2])

    if 'db' not in s.db.status:
        s.db.connect(

        )

    dbname = "tmp"
    dbhost = "tmp"
    dbport = "tmp"
    dbpasswd = "tmp"
    dbusr = "msf"

    db_cfg = [dbname, dbhost, dbport, dbpasswd, dbusr]

    if 'db' not in s.db.status:
        s.db.connect(
            username=dbusr,
            database=dbname,
            host=dbhost,
            port=dbport,
            password=dbpasswd
        )

