#!/usr/bin/env python
#coding: utf8

import zipfile
import os
import stat


def extract_sass_binaries(packages_dir=os.path.dirname(__file__)):
    libdir = os.path.join(packages_dir, 'Sassify_lib')
    os.makedirs(libdir, exist_ok=True)
    if os.path.splitext(os.path.dirname(__file__))[1] in ['.sublime-package']:
        package = zipfile.ZipFile(os.path.dirname(__file__))
        gemfiles = [i for i in package.namelist() if i.split('/')[0] in ['lib']]
        package.extractall(path=libdir, members=gemfiles)
        oldcwd = os.getcwd()
        print("oldcwd: ", oldcwd)
        os.chdir(os.path.join(libdir, 'lib', 'sass', 'bin'))
        for app in ['sass', 'sass-convert']:
            mode = os.stat(app).st_mode
            os.chmod(app, mode | stat.S_IXUSR)
    return libdir
