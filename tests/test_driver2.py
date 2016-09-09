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
import panwdagger.osdriver
import logging
import panwdagger.dag

__author__ = 'Ivan Bojer'

# def collect_all_vm_addrs():


def main():
    dag = panwdagger.dag.DAG()
    os = panwdagger.osdriver.OpenStack()
    tags = os.get_tags()
    dag.register_tags(tags)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(name)s %(message)s',
        datefmt='%Y%m%d %T',
        level=logging.INFO)

    main()
