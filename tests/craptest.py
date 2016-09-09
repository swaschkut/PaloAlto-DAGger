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
from pandevice.base import PanDevice
import yaml
import logging

__author__ = 'Ivan Bojer'

LOG = logging.getLogger()

__author__ = 'Ivan Bojer'

with open("clouds.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
vmcfg = cfg['clouds']['the_cloud']['vmseries']
device = PanDevice.create_from_device( vmcfg['hostname'],
                                       vmcfg['username'],
                                       vmcfg['password'] )

# device.userid.clear_all_registered_ip()
device.userid.register('1.1.1.2', ['ivan-admin'])

# addresses = device.userid.get_all_registered_ip()
# for ip, tags in addresses.iteritems():
#     for tag in tags:
#         print ip, tag

# adr = device.userid.unregister('1.1.1.2', 'b')
# print adr
#
# addresses2 = device.userid.get_all_registered_ip()
# for ip, tags in addresses2.iteritems():
#     print ip, tags