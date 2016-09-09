#  Copyright 2016 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from openstack import connection
from openstack import profile
import logging
import os_client_config
import collections

__author__ = 'Ivan Bojer'


LOG = logging.getLogger(__name__)
CLOUD_NAME = 'the_cloud'

# utils.enable_logging(True, stream=sys.stdout)


class Opts(object):
    def __init__(self, cloud_name, debug=False):
        self.cloud = cloud_name
        self.debug = debug
        # Use identity v2 API for examples.
        self.identity_api_version = '2'


class OpenStack(object):

    conn = None

    def __init__(self):
        self.conn = self.create_connection_from_config(CLOUD_NAME)

    def get_projects(self):
        projects = self.conn.identity.tenants()
        return projects

    def get_ports(self, p):
        ports = self.conn.network.ports()
        return ports

    def get_servers(self):
        servers = self.conn.compute.servers()
        return servers

    def get_security_groups(self, **filter_args):
        sec_groups = self.conn.network.security_groups(**filter_args)
        return sec_groups

    def get_tags(self):
        """Assemble tags based on the internal logic. We currently monitor only
        tenant and create IP tags as composite of PREFIX + TENANT_NAME

        :return: dictionary of tags using IP as the key
        """
        tags = collections.defaultdict(dict)
        projects = collections.defaultdict(dict)

        all_projects = self.get_projects()

        # create lookup table project.id to project.name
        for project in all_projects:
            projects[project.id] = project.name
            LOG.debug('Name: %s [%s]' % (project.name, project.id))
        #
        #     ports = os.get_ports(project)
        #     for port in ports:
        #         print("For project: %s port is %s" % (project.name, port))
        #
        servers = self.get_servers()
        for server in servers:
            for addr_key in server.addresses.keys():
                for ip_object in server.addresses.get(addr_key):
                    LOG.debug("For server: %s addresses are %s" % (server.name, ip_object['addr']))
                    tags[ip_object['addr']]['server'] = server.name
                    tags[ip_object['addr']]['project_id'] = server.project_id
                    tags[ip_object['addr']]['project_name'] = projects[project.id]
                    tags[ip_object['addr']]['sec_grp'] = []
                    for sec_grp in server.security_groups:
                        tags[ip_object['addr']]['sec_grp'].append( sec_grp)

        # sec_groups = os.get_security_groups(fields=['name', 'id', 'tenant_id'])
        # for sec_grp in sec_groups:
        #     print (sec_grp)

        return tags

    @staticmethod
    def create_connection_from_config(cloud_name):
        opts = Opts(cloud_name=cloud_name)
        occ = os_client_config.OpenStackConfig()
        cloud = occ.get_one_cloud(opts.cloud, argparse=opts)
        return connection.from_config(cloud_config=cloud, options=opts)

    @staticmethod
    def create_connection(auth_url, region, project_name, username, password):
        prof = profile.Profile()
        prof.set_region(profile.Profile.ALL, region)

        return connection.Connection(
            profile=prof,
            user_agent='examples',
            auth_url=auth_url,
            project_name=project_name,
            username=username,
            password=password
    )
