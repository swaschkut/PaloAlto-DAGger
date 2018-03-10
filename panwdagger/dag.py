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
import collections
import logging

import yaml

from pandevice.base import PanDevice

__author__ = 'Ivan Bojer'

LOG = logging.getLogger(__name__)


class DAG(object):

    def __init__(self):
        import os
        LOG.info('Loading configuration file...%s', os.environ['OS_CLIENT_CONFIG_FILE'])
        with open(os.environ['OS_CLIENT_CONFIG_FILE'], 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        vmcfg = cfg['clouds']['the_cloud']['vmseries']
        self.device = PanDevice.create_from_device(vmcfg['hostname'],
                                                   vmcfg['username'],
                                                   vmcfg['password'])

        self.PREFIX = cfg['clouds']['the_cloud']['tag']['prefix']
        self.PREFIX += '-'

        self.__clear_stale_tags()

    def register_tags_with_sync(self, tags):
        """Function that will register tags and remove the ones that are not
        present in the tags list. The assumption is that if tags are not present
        they must have been removed. In order to register a single tag no matter
        what @see register_tag function
        """
        if not isinstance(tags, dict):
            raise ValueError('Argument is not of the type dict')

        cur_addr = self.device.userid.get_all_registered_ip()
        if (tags and cur_addr) and cmp(tags.viewkeys(), cur_addr.viewkeys()) == 0:
            LOG.info('No tag additions detected')
            return 0, 0
        else:
            for tag_id in tags:
                project_name = tags[tag_id]['project_name']
                self.register_tags(tag_id, project_name)

            LOG.info('Added %s tags', len(tags))

        added = 0
        removed = 0
        delta_addresses = self.get_delta(tags, cur_addr)
        if delta_addresses:
            for ip, tags in delta_addresses.iteritems():
                for tag in tags:
                    if not isinstance(tag, list):
                        tag = [tag]
                    self.unregister_tags(ip, tag)

            added = len(tags)
            removed = len(delta_addresses)
        else:
            LOG.info('No deltas detected')

        return added, removed

    def register_tags(self, ip, tags):
        if not isinstance(tags, list):
            tags = [tags]

        for tag in tags:
            comp_tag = self.PREFIX + tag
            LOG.debug('Tag %s --> %s', ip, comp_tag)
            self.device.userid.register(ip, comp_tag)

    def unregister_tags(self, ip, tags):
        if not isinstance(tags, list):
            tags = [tags]

        for tag in tags:
            LOG.debug('Untag %s --> %s', tag, ip)
            self.device.userid.unregister(ip, tag)

    def get_delta(self, new_addresses, cur_addr):
        """
        Function returns all addresses with the PREFIX that are
        not present in the given dict. These are most likely ones that got removed.

        :type new_addresses: dictionary of the newest addresses pulled from nova service
        :param tags:
        :return: list of addresses that are potentially orphaned
        """

        # self.device.userid.register('1.1.1.1', ['ivan-admin'])
        # self.device.userid.register('1.1.1.2', ['ivan-admin'])
        # self.device.userid.register('0.0.0.0', ['craze'])

        # if none registered return
        if cur_addr:
            addresses_with_prefix = collections.defaultdict(dict)
            for ip, tags in cur_addr.iteritems():
                for tag in tags:
                    if self.PREFIX in tag:
                        addresses_with_prefix[ip] = tags

            # intersection = new_addresses.viewkeys() & addresses_with_prefix.viewkeys()
            delta = addresses_with_prefix.viewkeys() - new_addresses.viewkeys()

            delta_adr = collections.defaultdict(dict)
            for key in delta:
                delta_adr[key] = addresses_with_prefix[key]

            return delta_adr
        return None

    def __clear_stale_tags(self):
        addresses = self.device.userid.get_all_registered_ip()
        # if none registered return
        if not addresses:
            return

        LOG.debug('Clearing tags from %s', self.device)
        for ip, tags in addresses.iteritems():
            for tag in tags:
                if self.PREFIX in tag:
                    self.unregister_tags(ip, tags)
