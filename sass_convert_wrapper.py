#!/usr/bin/env python
#coding: utf8

import os
import subprocess


def sass_convert(args, **kwargs):
    # defaults = {}
    # defaults.update(kwargs)
    sass_path = kwargs.get('sass_bin_dir')
    try:
        sass_path = os.path.join(kwargs['sass_bin_dir'], 'sass-convert')
    except Exception as e:
        raise e
        return ('', "Unable to create application path for sass-convert")
    src = kwargs.get('src', 'scss')
    dest = kwargs.get('dest', 'scss')
    indent = kwargs.get('indentation', 't')
    # should pretty much always leave indentation as 't' because ST3
    #   will translates tabs correctly without any nastly fiddling
    sass_convert = subprocess.Popen(
        [sass_path, '-s', '-F', src, '-T', dest, '--indent', indent],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    sass_converted = sass_convert.communicate(args)
    return sass_converted


def main():
    pass

if __name__ == '__main__':
    main()
