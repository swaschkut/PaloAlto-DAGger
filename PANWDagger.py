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

import logging
import os
import time
import sys

import yaml

import panwdagger.dag
import panwdagger.osdriver

__author__ = 'Ivan Bojer'

# override default location of the config file
os.environ['OS_CLIENT_CONFIG_FILE'] = os.getcwd() + '/clouds.yaml'
LOG = logging.getLogger(__name__)
with open(os.environ['OS_CLIENT_CONFIG_FILE'], 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def main():
    dag = panwdagger.dag.DAG()
    openstack = panwdagger.osdriver.OpenStack()

    refresh_in_seconds = int(cfg['clouds']['refresh_in_seconds'])

    try:
        while True:
            LOG.info('Refreshing tags...')
            tags = openstack.get_tags()
            added, removed = dag.register_tags_with_sync(tags)
            LOG.info('Added: %s adr, removed: %s adr. Next refresh in: %ss', added, removed, refresh_in_seconds)
            time.sleep(refresh_in_seconds)
    except KeyboardInterrupt:
        LOG.info('Exit!')


if __name__ == "__main__":

    if sys.version_info[0] > 2:
        sys.exit("Python 2 is required and you are running %s." % sys.version)

    logging.getLogger("requests").setLevel(logging.WARNING)
    if bool(cfg['clouds']['debug']):
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s',
            datefmt='%Y%m%d %T',
            level=logging.DEBUG)
    else:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y%m%d %T',
            level=logging.INFO)
    main()
