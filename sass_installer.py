#!/usr/bin/env python
#coding: utf8

from zipfile import ZipFile
import os
import sys
import re
import platform
import stat
import subprocess
import urllib.request
# from urllib.request import urlopen
from io import BytesIO
from distutils.version import StrictVersion


# TODO: Rename this to SassLoader
#

library_folder = "Sassify_lib"
sass_archive_url = 'https://github.com/nex3/sass/archive/stable.zip'

# package = ZipFile(os.path.dirname(__file__))
# gemfiles = [i for i in package.namelist() if i.split('/')[0] in ['lib']]
# package.extractall(path=libdir, members=gemfiles)


class SassInstaller():
    """Installs Sass and checks for version updates"""
    def __init__(self, install_location):
        print('********************  INIT SassInstaller  ******************')
        self.libdir = os.path.join(install_location, library_folder)
        self.bindir = os.path.join(self.libdir, 'sass-stable', 'bin')

    def make_it_work(self):
        if self.needs_upgrade() and (platform.system().lower() != 'windows'):
            self.install()

    def is_installed(self):
        try:
            sass = subprocess.Popen(
                [os.path.join(self.bindir, 'sass'), '-v'],
                shell=(platform.system().lower() == 'windows'),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)

            sass_out = sass.communicate()
            print(sass_out)
            if not sass_out[1]:
                return True
        except Exception as e:
            print(e)
            # raise e
        return False

    def needs_upgrade(self):
        """ BEcause of how local_version works, this will do the right thing
        whether Sass is installed or not. Supercedes is_installed.
        """
        if (StrictVersion(self.remote_version()) >
                StrictVersion(self.local_version())):
            return True
        return False

    def remote_version(self):
        sass_version_url = 'https://raw.github.com/nex3/sass/stable/VERSION'
        # d = Downloader()
        version = Downloader().get_file(sass_version_url)
        version = version.decode('utf-8').strip()
        return version

    def local_version(self):
        try:
            with open(os.path.join(self.libdir, 'sass-stable', 'VERSION')) as f:
                version = f.read().strip()
        except Exception as e:
            print(e)
            version = '0.0'  # for use by StrictVersion, everything will be newer
        return version

    def install(self):
        # TODO: This should be threaded....
        # TODO: Add a .inprogress file while installation is in progress, remove when complete
        os.makedirs(self.libdir, exist_ok=True)
        sass_zip_url = 'https://github.com/nex3/sass/archive/stable.zip'
        # github_url = Downloader.get_file(sass_zip_url)
        github_zip = ZipFile(BytesIO(Downloader().get_file(sass_zip_url)))
        github_zip.extractall(path=self.libdir)

        oldcwd = os.getcwd()
        os.chdir(self.bindir)
        for app in ['sass', 'sass-convert']:
            mode = os.stat(app).st_mode
            os.chmod(app, mode | stat.S_IXUSR)
        os.chdir(oldcwd)


class Downloader():
    """
    Class for retrieving remote files, should workaround vanilla Ubuntu
    missing SSL and CURL
    """
    def __init__(self):
        self.timeout = 45
        self.has_ssl = ('ssl' in sys.modules and
                        hasattr(urllib.request, 'HTTPSHandler'))

    def urlopen(self, url):
        try:
            cmd = urllib.request.urlopen(url)
            result = cmd.read()
            return result
        except Exception as e:
            print(e)
            return False

    def wget(self, url):
        timeout = str(int(self.timeout))
        cmd = subprocess.Popen(
            ['wget', '-q', '--timeout=' + timeout, '-O', '-', url],
            shell=(platform.system().lower() == 'windows'),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        result = cmd.communicate()
        if result[0]:
            return result[0]
        return False

    def curl(self, url):
        timeout = str(int(self.timeout))
        cmd = subprocess.Popen(
            ['curl', '-connect-timeout', timeout, url],
            shell=(platform.system().lower() == 'windows'),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        result = cmd.communicate()
        if result[0]:
            return result[0]
        return False

    def get_file(self, url):
        """ heavily inspired by Emmet's PyV8loader """
        is_ssl = re.search('^https://', url) is not None
        if (is_ssl and self.has_ssl) or not is_ssl:
            contents = self.urlopen(url)
        else:
            for tool in [self.curl, self.wget]:
                try:
                    contents = tool(url)
                    break
                except Exception as e:
                    print(e)
                    pass
        return contents


if __name__ == '__main__':

    sass = SassInstaller('/tmp/NEW_TESTING')
    # sass.install()
    print('Local Version', sass.local_version())
    print('Remote Version', sass.remote_version())
    print("sass", sass.is_installed())
    print("sass.needs_upgrade", sass.needs_upgrade())

    sass.make_it_work()
    # Is Sass installed?
    print(sass.bindir)
    #   What version of Sass is installed?
    # If get_installed_version is False
        # install libraru
    # else if
