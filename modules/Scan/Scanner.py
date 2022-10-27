from datetime import datetime

import nmap as nmap
from time import sleep
from tqdm import tqdm
import fontawesome as fa
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

from common.util import print_header
from common import eop

# https://libnmap.readthedocs.io/en/latest/process.html
# https://linux.die.net/man/1/nmap
class Scanner:
    def __init__(self, hosts="192.168.1.0/24", ports=None, args="-sV", safe_mode=True):
        if ports is None:
            ports = [1, 65535]
        self.hosts = hosts
        self.ports = ports
        self.args = args
        self.safe_mode = safe_mode
        self.known_hosts = {}
        self.current_command = "nmap " + self.hosts + " " + self.format_args()

    def Configure(self):
        print("Configure " + fa.icons['cog'])

        # Ports
        # --top-ports: Top
        # --port-ratio: Ratio
        # -p: Range/List

        print("Current Command: " + self.current_command)
        self.hosts = input("Hosts: ")
        self.ports = input("Ports: ")
        self.args = input("Args: ")
        input("Press enter to continue")
        return 1

    def Run(self):
        args = self.format_args()  # @TODO
        print(fa.icons['spinner'] + " Running " + self.current_command)

        nmproc = NmapProcess(targets=self.hosts, options=args, safe_mode=self.safe_mode)



        nmproc.sudo_run_background()

        if eop.is_root():
            progress = tqdm(total=100, desc="Scan", unit="percent")
            while nmproc.is_running():
                progress.update(int(float(nmproc.progress) - progress.n))
                progress.refresh()
                sleep(2)

            try:
                parsed = NmapParser.parse(nmproc.stdout)
                print_scan(parsed)
            except NmapParserException as e:
                print("Exception raised while parsing scan: {0}".format(e.msg))

    def format_args(self):
        ports = format_ports(scanner=self)
        return self.args + " " + ports


def format_ports(scanner):
    if len(scanner.ports) == 2:
        ports = str(scanner.ports[0]) + "-" + str(scanner.ports[1])
    # If more than two ports, set as a comma separated list
    elif len(scanner.ports) > 2:
        ports = ",".join(scanner.ports)
    # If only one port, set as a single port
    else:
        ports = str(scanner.ports[0])
    return "-p " + ports


def print_scan(parsed):
    print_header("Results", " ")
    unix_timestamp = parsed.started
    start = datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    print("Scan with Nmap {0} ( http://nmap.org )  at {1}".format(
        parsed.version,
        start))

    for host in parsed.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        if host.is_up():
            # Get OS
            if host.os_fingerprinted:
                print("Host: {0} ({1})".format(tmp_host, host.os_match_probabilities()))



            print("\nHost {0}/{1} {2}.".format(tmp_host, host.address, host.status))
            print("   PORT    STATE         SERVICE")

            for serv in host.services:
                pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
                if len(serv.banner):
                    pserv += " ({0})".format(serv.banner)
                print(pserv)
    print(parsed.summary)
    # @TODO add to database or file or something
    input("Press enter to continue")
