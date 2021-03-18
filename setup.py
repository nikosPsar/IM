#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import sys
import os
from setuptools import setup, find_packages
from setuptools.command.install import install


class Install_osm_im(install):
    """Generation of .py files from yang models"""
    model_dir = "models/yang"
    im_dir = "osm_im"

    def pipinstall(self, package):
        """pip install for executable dependencies"""
        subprocess.call([sys.executable, "-m", "pip", "install", package])

    def run(self):
        self.pipinstall('pyang')
        self.pipinstall('pyangbind')
        import pyangbind
        print("Using dir {}/{} for python artifacts".format(os.getcwd(), self.im_dir))
        path = "{}/{}".format(os.getcwd(), self.im_dir)
        for files_item in ['vnfd', 'nsd', 'nst']:
            protoc_command = ["pyang",
                              "-Werror",
                              "--plugindir",
                              "{}/plugin".format(os.path.dirname(pyangbind.__file__)),
                              "--path",
                              self.model_dir,
                              "-f", "pybind",
                              "-o",
                              "{}/{}.py".format(self.im_dir, files_item),
                              "{}/{}.yang".format(self.model_dir, files_item)]
            print("Generating {}.py from {}.yang".format(files_item, files_item))
            if subprocess.call(protoc_command) != 0:
                sys.exit(-1)
        # To ensure generated files are copied to the python installation folder
        self.copy_tree(self.im_dir, "{}{}".format(self.install_lib, self.im_dir))
        install.run(self)


setup(
    name='osm_im',
    description='OSM Information Model',
    long_description=open('README.rst').read(),
    version_command=('v8.0.3-0-g03c9aaf-dirty-PAAS'),
    # author='Mike Marchetti',
    # author_email='mmarchetti@sandvine.com',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['setuptools-version-command'],
    install_requires=['pyang', 'pyangbind'],
    test_suite='nose.collector',
    # url='https://osm.etsi.org/gitweb/?p=osm/IM.git;a=summary',
    license='Apache 2.0',
    cmdclass={'install': Install_osm_im},
)
