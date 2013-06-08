#!/usr/bin/env python
#coding: utf8

import os
import subprocess
import platform


def sass_compile(args, **kwargs):
    sass_path = kwargs.get('sass_bin_dir')
    sass_path = os.path.join(sass_path, 'sass')
    format = kwargs.get('format', 'expanded')

    sass_compile = subprocess.Popen(
        [sass_path, '-s', '--scss', '--style', format],
        shell=(platform.system().lower() == 'windows'),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    sass_compiled = sass_compile.communicate(args)
    return sass_compiled


def main():
    pass

if __name__ == '__main__':
    main()
