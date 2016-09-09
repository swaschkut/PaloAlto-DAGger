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

import panwdagger.dag
import panwdagger.osdriver

# override default location of the config file
os.environ['OS_CLIENT_CONFIG_FILE'] = os.getcwd() + '/clouds.yaml'

__author__ = 'Ivan Bojer'


def main():
    dag = panwdagger.dag.DAG()
    os = panwdagger.osdriver.OpenStack()
    tags = os.get_tags()
    dag.register_tags_with_sync(tags)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s',
        datefmt='%Y%m%d %T',
        level=logging.INFO)

    main()
