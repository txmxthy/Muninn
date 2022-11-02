from typing import List

import libnmap
from libnmap.parser import NmapParser, NmapParserException
from libnmap.objects import NmapHost, NmapService
from libnmap.objects.os import NmapOSClass, NmapOSMatch, NmapOSFingerprint
import fontawesome as fa
from tqdm import tqdm

# from common.deps.pymetasploit3
from common.deps.pymetasploit3.msfrpc import ServicesTable, HostsTable, ModuleManager, ExploitModule


def host_in_db(app, host):
    hosts = app.rpc["Client"].db.workspaces.workspace('default').hosts.list
    host_found = False
    for d in hosts:
        if d['address'] == host.address:
            host_found = True
            return 1
    return 0


def insert_services(app, host, services):
    """

    :param app:
    :param host:
    :param services: List of dicts containing {"proto": proto, "port": port, "name": name, "state": state}
    :return:
    """
    # Tqdm progress bar
    pbar = tqdm.tqdm(total=len(services), desc="Inserting services into database...", unit="services")
    for service in services:
        pbar.update(1)

        # """
        #         Record a service in the database.
        #
        #         Mandatory Arguments:
        #         - host : the host where this service is running.
        #         - port :  the port where this service listens.
        #         - proto : the transport layer protocol (e.g. tcp, udp).
        #
        #         Optional Keyword Arguments:
        #         - name : the application layer protocol (e.g. ssh, mssql, smb)
        #         - sname : an alias for the above
        #         """
        x: ServicesTable = app.rpc["Client"].db.workspaces.workspace('default').services.report(host=host,
                                                                                                port=service["port"],
                                                                                                proto=service["proto"],
                                                                                                state=service["state"],
                                                                                                name=service["name"])
    return app


def insert_host(app, host: NmapHost):
    # Check if host is in database
    # if not host_in_db(app, host):
    if True:
        addr = host.address

        os: list[NmapOSMatch] = host.os.osmatches

        best_os = {}
        best_accuracy = 0
        x: NmapOSMatch
        for x in os:
            c: list[NmapOSClass] = x.osclasses
            y: NmapOSClass
            for y in c:
                if y.accuracy > best_accuracy:
                    best_os = {
                        "vendor": y.vendor,
                        "osfamily": y.osfamily,
                        "osgen": y.osgen,
                        "accuracy": y.accuracy,
                        "type": y.type
                    }
                elif y.accuracy == best_accuracy:
                    best_os["osgen"] = best_os["osgen"] + " or " + y.osgen

        # Insert host
        print("Inserting host into database...")
        #  Mandatory Keyword Arguments:
        #         - host : an IP address or Host object reference.
        #
        #         Optional Keyword Arguments:
        #         - state : a host state.
        #         - os_name : an operating system.
        #         - os_flavor : something like 'XP or 'Gentoo'.
        #         - os_sp : something like 'SP2'.
        #         - os_lang : something like 'English', 'French', or 'en-US'.
        #         - arch : an architecture.
        #         - mac : the host's MAC address.
        #         - scope : interface identifier for link-local IPv6.
        #         - virtual_host : the name of the VM host software, e.g. 'VMWare', 'QEMU', 'Xen', etc.
        #         """

        # {'created_at': 1667409307, 'address': '192.168.86.66', 'mac': '', 'name': '', 'state': 'alive', 'os_name':
        # 'Unknown', 'os_flavor': '', 'os_sp': '', 'os_lang': '', 'updated_at': 1667409307, 'purpose': 'device',
        # 'info': ''}

        os_name = best_os["osfamily"] + " " + best_os["osgen"],
        x: HostsTable = app.rpc["Client"].db.workspaces.workspace('default').hosts.report(host=addr,
                                                                                          os_name=os_name,
                                                                                          name=best_os["osfamily"],
                                                                                          os_flavor=best_os["osgen"],
                                                                                          info="")

        # Insert services
        services = []
        service: NmapService
        for service in host.services:
            cpe = {}
            banner = ""
            if service.banner:
                banner = service.banner
            if len(service.cpelist):
                cpe['part'] = service.cpelist[0].get_part()
                cpe['vendor'] = service.cpelist[0].get_vendor()
                cpe['product'] = service.cpelist[0].get_product()
                cpe['version'] = service.cpelist[0].get_version()
                cpe['update'] = service.cpelist[0].get_update()
                cpe['edition'] = service.cpelist[0].get_edition()
                cpe['language'] = service.cpelist[0].get_language()
                print(cpe)
                input("checked")
            if service.state == "open":
                proto = service.protocol
                port = service.port
                name = service.service
                state = service.state
                services.append({"proto": proto,
                                 "port": port,
                                 "name": name,
                                 "state": state,
                                 "cpe": cpe,
                                 "banner": banner})
        print("Inserting services into database...")
        print(services)
        insert_services(app, addr, services)
        return app
    else:
        print("Host already in database")
    return app


def host_icon(family):
    # Get first item if list
    if isinstance(family, list):
        family = family[0]

    family = family.lower()
    if "win" in family:
        icon = fa.icons["windows"]
    elif "linux" in family:
        icon = fa.icons["linux"]
    elif "mac" in family:
        icon = fa.icons["apple"]
    else:
        icon = fa.icons["question"]
    return icon


def check_exploitable(app, host, service):
    """
    Check if vulnerabilities exist for the service on the host
    :param app:
    :param service:
    :return:
    """
    # OPTIONS:
    #
    #     -h, --help                      Help banner
    #     -I, --ignore                    Ignore the command if the only match has the same name as the search
    #     -o, --output <filename>         Send output to a file in csv format
    #     -r, --sort-descending <column>  Reverse the order of search results to descending order
    #     -S, --filter <filter>           Regex pattern used to filter search results
    #     -s, --sort-ascending <column>   Sort search results by the specified column in ascending order
    #     -u, --use                       Use module if there is one result
    #
    # Keywords:
    #   aka              :  Modules with a matching AKA (also-known-as) name
    #   author           :  Modules written by this author
    #   arch             :  Modules affecting this architecture
    #   bid              :  Modules with a matching Bugtraq ID
    #   cve              :  Modules with a matching CVE ID
    #   edb              :  Modules with a matching Exploit-DB ID
    #   check            :  Modules that support the 'check' method
    #   date             :  Modules with a matching disclosure date
    #   description      :  Modules with a matching description
    #   fullname         :  Modules with a matching full name
    #   mod_time         :  Modules with a matching modification date
    #   name             :  Modules with a matching descriptive name
    #   path             :  Modules with a matching path
    #   platform         :  Modules affecting this platform
    #   port             :  Modules with a matching port
    #   rank             :  Modules with a matching rank (Can be descriptive (ex: 'good') or numeric with comparison operators (ex: 'gte400
    #   ref              :  Modules with a matching ref
    #   reference        :  Modules with a matching reference
    #   target           :  Modules affecting this target
    #   type             :  Modules of a specific type (exploit, payload, auxiliary, encoder, evasion, post, or nop)
    #
    # Supported search columns:
    #   rank             :  Sort modules by their exploitabilty rank
    #   date             :  Sort modules by their disclosure date. Alias for disclosure_date
    #   disclosure_date  :  Sort modules by their disclosure date
    #   name             :  Sort modules by their name
    #   type             :  Sort modules by their type
    #   check            :  Sort modules by whether or not they have a check method
    #
    # Examples:
    #   search cve:2009 type:exploit
    #   search cve:2009 type:exploit platform:-linux
    #   search cve:2009 -s name
    #   search type:exploit -s type -r

    queryA = service["name"] + " type:exploit"
    queryB = "port:" + str(service["port"])+ " type:exploit"

    exploitA: list = app.rpc["Client"].modules.search(match=queryA)
    exploitB: list = app.rpc["Client"].modules.search(match=queryB)
    exploits = exploitA + exploitB

    applicable = []

    if not exploits:
        return applicable
    else:
        # {'type': 'exploit', 'name': 'Centreon Web Useralias Command Execution', 'fullname':
        # 'exploit/linux/http/centreon_useralias_exec', 'rank': 'excellent', 'disclosuredate': '2016-02-26'}
        for exploit in exploits:
            if host["name"].lower() in exploit["fullname"].lower() or host["os"].lower() in exploit["name"].lower():
                applicable.append(exploit)
    return applicable


def services_by_host(app, host):
    services = app.rpc["Client"].db.workspaces.workspace('default').services.list
    for service in services:
        if service['host'] == host['address']:
            applicable = check_exploitable(app, host, service)

            if applicable:
                viability = fa.icons["exclamation"]
            else:
                viability = fa.icons["lock"]

            print(f"\t{fa.icons['tasks']} "
                  f"{viability} "
                  f"{service['name']} "
                  f"{service['state']} on port "
                  f"{service['port']} using "
                  f"{service['proto']}")
            if applicable:
                if service['port'] not in [80, 443] and service['name'] not in ["http", "https"]:
                    for exploit in applicable:
                        # Ignore 80 and 443

                            print(f"\t {exploit['name']} with rank {exploit['rank']}")
                else:
                    print("Software running on http/80/https/443 is not as easy to determine, "
                          "prioritize other services")
