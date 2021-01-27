# generate.py - generate Centreon import data files for hosts and services

# Globals
user = 'admin'
# pswd = 'centreon'  # local
pswd = 'admin'  # remote

#-------------------------------------------------------------------------------

class Command:
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def gen_delete(self):
        """The command to delete this command"""
        return f'centreon -u {user} -p {pswd} -o cmd -a del -v "{self.name}"\n'

    def gen_import(self):
        return f'CMD;add;{self.name};2;{self.line}\n'

#-------------------------------------------------------------------------------

class SrvTemplate:
    def __init__(self, name, desc, use):
        self.name = name
        self.desc = desc
        self.use = use

    def gen_delete(self):
        """The command to delete this service template"""
        return f'centreon -u {user} -p {pswd} -o stpl -a del -v {self.name}\n'

    def gen_import(self):
        return f"""STPL;add;{self.name};{self.desc};{self.use}
STPL;setparam;{self.name};check_command;check_service
STPL;setparam;{self.name};check_period;24x7
STPL;setparam;{self.name};service_max_check_attempts;3
STPL;setparam;{self.name};service_normal_check_interval;1
STPL;setparam;{self.name};service_retry_check_interval;1
STPL;setparam;{self.name};service_register;0
"""

#-------------------------------------------------------------------------------

class Service:
    def __init__(self, host, svc_desc, notes):
        self.host = host
        self.svc_desc = svc_desc
        self.notes = notes

    def gen_delete(self):
        """The command to delete this service"""
        return f'centreon -u {user} -p {pswd} -o service -a del ' \
            f'-v "{self.host};{self.svc_desc}"\n'

    def gen_import(self):
        return f"""SERVICE;add;{self.host};{self.svc_desc};Joao-Template
SERVICE;setparam;{self.host};{self.svc_desc};notes;{self.notes}
"""

#-------------------------------------------------------------------------------

class Host:
    def __init__(self, host, alias, notes):
        self.host = host
        self.alias = alias
        self.notes = notes

    def gen_delete(self):
        """The command to delete this host"""
        # Note: this fails if the line has a Windows-style line ending
        return f'centreon -u {user} -p {pswd} -o host -a del -v {self.host}\n'

    def gen_import(self):
        return f"""HOST;add;{self.host};{self.alias};127.0.0.1;;Central;
HOST;setparam;{self.host};check_command;base_host_alive
HOST;setparam;{self.host};check_period;24x7
HOST;setparam;{self.host};notification_period;24x7
HOST;setparam;{self.host};host_max_check_attempts;3
HOST;setparam;{self.host};host_check_interval;1
HOST;setparam;{self.host};host_retry_check_interval;1
HOST;setparam;{self.host};notes;{self.notes}
"""

#-------------------------------------------------------------------------------

class Config:
    def __init__(self):
        """Create all the commands, service templates, hosts (12) and services."""
        self.cmds = []
        self.stpls = []
        self.hosts = []
        self.services = []

    def gen_import(self, filepath):
        """Generate the import data"""
        s = ''
        for x in self.cmds:
            s += x.gen_import()
        for x in self.stpls:
            s += x.gen_import()
        for x in self.hosts:
            s += x.gen_import()
        for x in self.services:
            s += x.gen_import()
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(s)

    def gen_delete(self, filepath):
        """Generate the delete script"""
        s = ''
        for x in self.services:
            s += x.gen_delete()
        for x in self.hosts:
            s += x.gen_delete()
        for x in self.stpls:
            s += x.gen_delete()
        for x in self.cmds:
            s += x.gen_delete()

        # Force unix-style newlines, otherwise del host fails
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(s)

    def populate(self):
        # Check command
        line = 'python3 $USER1$/check_service.py "$HOSTNAME$" $HOSTSTATE$' \
            ' "$SERVICEDESC$" $SERVICESTATE$'
        self.cmds.append(Command('check_service', line))

        # Service templates
        self.stpls.append(SrvTemplate('Joao-Template', 'Joao-Template-Alias', 'generic-active-service'))

        # Database servers
        self.hosts.append(Host('srvlnx001', 'lnx_db_server_01', 'linux db_server transaction'))
        self.hosts.append(Host('srvlnx002', 'lnx_db_server_02', 'linux db_server warehouse'))
        self.hosts.append(Host('srvwin001', 'win_db_server_01', 'windows db_server historical'))
        self.hosts.append(Host('srvwin002', 'win_db_server_02', 'windows db_server logging'))

        # Backend
        self.hosts.append(Host('srvlnx003', 'lnx_backend_01', 'linux backend core'))
        self.hosts.append(Host('srvlnx004', 'lnx_backend_02', 'linux backend pricing'))
        self.hosts.append(Host('srvwin003', 'win_backend_01', 'windows backend historical'))
        self.hosts.append(Host('srvwin004', 'win_backend_02', 'windows backend logging'))

        # Web servers
        self.hosts.append(Host('srvlnx005', 'lnx_web_server_01', 'linux web_server'))
        self.hosts.append(Host('srvlnx006', 'lnx_web_server_02', 'linux web_server'))
        self.hosts.append(Host('srvlnx007', 'lnx_web_server_03', 'linux web_server'))
        self.hosts.append(Host('srvlnx008', 'lnx_web_server_04', 'linux web_server'))

        # Database services
        for i in range(5):
            self.services.append(Service('srvlnx001', f'fct_transactional{i}', 'db_svc transactional'))
        for i in range(5):
            self.services.append(Service('srvlnx002', f'fct_data_warehouse{i}', 'db_svc data_warehouse'))
        for i in range(5):
            self.services.append(Service('srvwin001', f'fct_db_historical{i}', 'db_svc historical'))
        for i in range(5):
            self.services.append(Service('srvwin002', f'fct_db_logging{i}', 'db_svc logging'))

        # Backend services
        for i in range(5):
            self.services.append(Service('srvlnx003', f'fct_core{i}', 'backend_svc core'))
        for i in range(5):
            self.services.append(Service('srvlnx004', f'fct_pricing{i}', 'backend_svc pricing'))
        for i in range(5):
            self.services.append(Service('srvwin003', f'fct_historical{i}', 'backend_svc historical'))
        for i in range(5):
            self.services.append(Service('srvwin004', f'fct_logging{i}', 'backend_svc logging'))

        # Web services
        k = 0
        for i in range(5, 9):
            for j in range(5):
                self.services.append(Service(f'srvlnx00{i}', f'fct_web{k}', 'web_svc'))
                k += 1

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

c = Config()
c.populate()

filepath = 'c:/a/import.txt'
c.gen_import(filepath)

filepath = 'c:/a/delete.sh'
c.gen_delete(filepath)