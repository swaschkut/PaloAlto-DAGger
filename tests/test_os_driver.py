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
import unittest

import panwdagger.dag
import panwdagger.osdriver

__author__ = 'Ivan Bojer'


class OpenStackStatusTests(unittest.TestCase):
    def test_read_data(self):
        os = panwdagger.osdriver.OpenStack()
        projects = os.get_projects()
        nr_projects = sum(1 for _ in projects)
        self.assertGreater(nr_projects, 0)

        servers = os.get_servers()
        sec_groups = os.get_security_groups(fields=['name', 'id', 'tenant_id'])

    def test_register_address(self):
        dag = panwdagger.dag.DAG()
        dag.register_tags('1.2.3.4', 'testtag')
        dag.unregister_tags('1.2.3.4', 'testtag')

