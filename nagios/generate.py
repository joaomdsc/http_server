# generate.py - generate Centreon import data files for hosts and services

# Globals
user = 'admin'
pswd = 'centreon'

class Service:
    def __init__(self, host, svc_desc, notes):
        self.host = host
        self.svc_desc = svc_desc
        self.notes = notes

    def delete(self):
        """The command to delete this service"""
        return f'centreon -u {user} -p {pswd} -o service -a del -v "{self.host};{self.svc_desc}"\n'

    def gen_import(self):
        return f"""SERVICE;ADD;{self.host};{self.svc_desc};Joao-Template
SERVICE;setparam;{self.host};{self.svc_desc};check_command;check_server
SERVICE;setparam;{self.host};{self.svc_desc};service_is_volatile;2
SERVICE;setparam;{self.host};{self.svc_desc};service_active_checks_enabled;2
SERVICE;setparam;{self.host};{self.svc_desc};service_passive_checks_enabled;2
SERVICE;setparam;{self.host};{self.svc_desc};service_parallelize_check;2
SERVICE;setparam;{self.host};{self.svc_desc};service_obsess_over_service;2
SERVICE;setparam;{self.host};{self.svc_desc};service_check_freshness;2
SERVICE;setparam;{self.host};{self.svc_desc};service_event_handler_enabled;2
SERVICE;setparam;{self.host};{self.svc_desc};service_flap_detection_enabled;2
SERVICE;setparam;{self.host};{self.svc_desc};service_process_perf_data;2
SERVICE;setparam;{self.host};{self.svc_desc};service_retain_status_information;2
SERVICE;setparam;{self.host};{self.svc_desc};service_retain_nonstatus_information;2
SERVICE;setparam;{self.host};{self.svc_desc};service_notifications_enabled;2
SERVICE;setparam;{self.host};{self.svc_desc};contact_additive_inheritance;0
SERVICE;setparam;{self.host};{self.svc_desc};cg_additive_inheritance;0
SERVICE;setparam;{self.host};{self.svc_desc};service_inherit_contacts_from_host;1
SERVICE;setparam;{self.host};{self.svc_desc};service_use_only_contacts_from_host;0
SERVICE;setparam;{self.host};{self.svc_desc};service_locked;0
SERVICE;setparam;{self.host};{self.svc_desc};service_register;1
SERVICE;setparam;{self.host};{self.svc_desc};service_activate;1
SERVICE;setparam;{self.host};{self.svc_desc};notes;{self.notes}
"""

class Host:
    def __init__(self, host, alias, notes):
        self.host = host
        self.alias = alias
        self.notes = notes

    def delete(self):
        """The command to delete this host"""
        # Note: this fails if the line has a Windows-style line ending
        return f'centreon -u {user} -p {pswd} -o host -a del -v {self.host}\n'

    def gen_import(self):
        return f"""HOST;ADD;{self.host};{self.alias};127.0.0.1;;Central;
HOST;setparam;{self.host};check_command;base_host_alive
HOST;setparam;{self.host};check_period;24x7
HOST;setparam;{self.host};notification_period;24x7
HOST;setparam;{self.host};host_max_check_attempts;3
HOST;setparam;{self.host};host_check_interval;1
HOST;setparam;{self.host};host_retry_check_interval;1
HOST;setparam;{self.host};host_active_checks_enabled;2
HOST;setparam;{self.host};host_passive_checks_enabled;2
HOST;setparam;{self.host};host_checks_enabled;2
HOST;setparam;{self.host};host_obsess_over_host;2
HOST;setparam;{self.host};host_check_freshness;2
HOST;setparam;{self.host};host_event_handler_enabled;2
HOST;setparam;{self.host};host_flap_detection_enabled;2
HOST;setparam;{self.host};host_retain_status_information;2
HOST;setparam;{self.host};host_retain_nonstatus_information;2
HOST;setparam;{self.host};host_notifications_enabled;2
HOST;setparam;{self.host};contact_additive_inheritance;0
HOST;setparam;{self.host};cg_additive_inheritance;0
HOST;setparam;{self.host};host_locked;0
HOST;setparam;{self.host};host_register;1
HOST;setparam;{self.host};host_activate;1
HOST;setparam;{self.host};notes;{self.notes}
"""

class Config:
    def __init__(self):
        """Create all the hosts (12) and services."""
        self.hosts = []
        self.services = []

    def gen_import(self, filepath):
        """Generate the import data"""
        s = ''
        for h in self.hosts:
            s += h.gen_import()
        for svc in self.services:
            s += svc.gen_import()
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(s)

    def gen_delete(self, filepath):
        """Generate the delete script"""
        s = ''
        # First delete the services
        for svc in self.services:
            s += svc.delete()

        # Delete the hosts
        for h in self.hosts:
            s += h.delete()

        # Force unix-style newlines, otherwise del host fails
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(s)

    def populate(self):
        # Database servers
        self.hosts.append(Host('srvlnx001', 'lnx_db_server_01', 'linux db_server transaction'))
        self.hosts.append(Host('srvlnx002', 'lnx_db_server_02', 'linux db_server warehouse'))
        self.hosts.append(Host('srvwin001', 'win_db_server_01', 'windows db_server historical'))
        self.hosts.append(Host('srvwin002', 'win_db_server_02', 'windows db_server logging'))

        # # Backend
        # self.hosts.append(Host('srvlnx003', 'lnx_backend_01', 'linux backend core'))
        # self.hosts.append(Host('srvlnx004', 'lnx_backend_02', 'linux backend pricing'))
        # self.hosts.append(Host('srvwin003', 'win_backend_01', 'windows backend historical'))
        # self.hosts.append(Host('srvwin004', 'win_backend_02', 'windows backend logging'))

        # # Web servers
        # self.hosts.append(Host('srvlnx005', 'lnx_web_server_01', 'linux web_server'))
        # self.hosts.append(Host('srvlnx006', 'lnx_web_server_02', 'linux web_server'))
        # self.hosts.append(Host('srvlnx007', 'lnx_web_server_03', 'linux web_server'))
        # self.hosts.append(Host('srvlnx008', 'lnx_web_server_04', 'linux web_server'))

        # Database services
        for i in range(5):
            self.services.append(Service('srvlnx001', f'fct_transactional{i}', 'db_svc transactional'))
        for i in range(5):
            self.services.append(Service('srvlnx002', f'fct_data_warehouse{i}', 'db_svc data_warehouse'))
        for i in range(5):
            self.services.append(Service('srvwin001', f'fct_db_historical{i}', 'db_svc historical'))
        for i in range(5):
            self.services.append(Service('srvwin002', f'fct_db_logging{i}', 'db_svc logging'))

        # # Backend services
        # for i in range(5):
        #     self.services.append(Service('srvlnx003', f'fct_core{i}', 'backend_svc core'))
        # for i in range(5):
        #     self.services.append(Service('srvlnx004', f'fct_pricing{i}', 'backend_svc pricing'))
        # for i in range(5):
        #     self.services.append(Service('srvwin003', f'fct_historical{i}', 'backend_svc historical'))
        # for i in range(5):
        #     self.services.append(Service('srvwin004', f'fct_logging{i}', 'backend_svc logging'))

        # # Web services
        # k = 0
        # for i in range(5, 9):
        #     for j in range(5):
        #         self.services.append(Service(f'srvlnx00{i}', f'fct_web{k}', 'web_svc'))
        #         k += 1

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

c = Config()
c.populate()

filepath = 'import.txt'
c.gen_import(filepath)

filepath = 'delete.sh'
c.gen_delete(filepath)