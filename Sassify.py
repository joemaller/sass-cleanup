#coding: utf8

import sublime
import sublime_plugin
import os
import re
# import importlib
#import zipfile
# from pprint import pprint

from . sass_compile_wrapper import sass_compile
from . sass_convert_wrapper import sass_convert
from . sass_installer import SassInstaller


print("loaded Sassify")

# importlib.invalidate_caches()
# TODO:
#       get scope/language/global indentation settings
#       use a settings file for choosing scss or css
#
#       Offer option to compact pure css
#          this might work by running sass and sass-convert
#          on the same text, then comparing the two
#          if there are no differences, then nothing was parsed
#          and the block is pure css. If that's true, use the
#          output from sass instead of sass-convert
#

APP_NAME = "Sass Beautifier"
SASS_BIN_DIR = ''


def plugin_loaded():
    global APP_NAME, SASS_BIN_DIR, SETTINGS
    print('*************************PLUGIN_LOADED*******************')
    SETTINGS = sublime.load_settings('Sassify.sublime-settings')

    print(SETTINGS.get('sass_bin_dir'))
    print('settings has', SETTINGS.has('sass_bin_dir'))

    print("__file__\n", __file__)
    print("os.path.dirname(__file__)\n",
          os.path.dirname(__file__))
    print("os.path.dirname(os.path.abspath(__file__))\n",
          os.path.dirname(os.path.abspath(__file__)))

    print("sublime.installed_packages_path())\n",
          sublime.installed_packages_path())

    # TODO: Clean this mess up
    # TODO: Check for existing sass version to see if we need an update

    # Initialize the Sass Installer
    sass = SassInstaller(sublime.installed_packages_path())
    SASS_BIN_DIR = sass.bindir
    SASS_BIN_DIR = SETTINGS.get('sass_bin_dir', SASS_BIN_DIR)
    print('SASS_BIN_DIR', SASS_BIN_DIR)
    sass.make_it_work()

# TODO: Add the sass_installer here.

class SassBaseCommand(sublime_plugin.TextCommand):
    def update(self, edit, result):
        output, error = result
        if output and not error:
            output = output.strip()
            self.view.replace(edit, self.view.sel()[0], output)
        else:
            msg = "** {}: {}".format(APP_NAME, error)
            print(repr(msg))  # print error to console for debugging
            sublime.status_message(msg)

    def process(self, **kwargs):
        app = kwargs.get('app', sass_convert)
        defaults = {'sass_bin_dir': SASS_BIN_DIR}
        defaults.update(kwargs)
        dest = error = ''
        try:
            src = self.view.substr(self.view.sel()[0])
            dest, error = app(src, **defaults)
        except Exception as e:
            sublime.status_message("*!* {}: {}".format(APP_NAME, e))
            error = str(e)
            raise e
        error = re.sub("\s*Use .*backtrace\.?\s*", '', error)
        return dest, error

    def format_and_replace(self, edit, **kwargs):
        self.view.run_command("expand_selection_to_css_rule")
        self.update(edit, self.process(**kwargs))


class SassConvertCommand(SassBaseCommand):
    def run(self, edit):
        self.format_and_replace(edit, app=sass_convert)


class SassCompileCompactCommand(SassBaseCommand):
    def run(self, edit):
        print('hallooo!')
        self.format_and_replace(edit, app=sass_compile, format="compact")


class ExpandSelectionToCssRuleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.expand_selection_to_rule()

    def expand_selection_to_rule(self):
        """
        Selects the parent rule, if there's nesting
        returns either a sublime.selection object or False
        """
        # TODO: Make multiple selections work right...
        #           for region in self.view.sel():

        # TODO: pre-check line for last-character or first-char next line is "{"
        # if that's true, select hte line before doing anything else.
        old_sel = self.view.sel()[0]
        rule = self.view.substr(old_sel)

        # if we've got brackets, reduce the selection down to just the brackets
        # so Expand Selection to Brackets will grab the parent.
        if re.search(r"\{[^}]+\}", rule):
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(
                old_sel.begin() + rule.index('{'),
                old_sel.begin() + rule.rindex('}') + 1))

        # special case for opening line of a css/scss rule
        if rule.count('{') > rule.count('}'):
            self.view.sel().clear()
            p = old_sel.begin() + rule.rindex('{')
            self.view.sel().add(sublime.Region(p, p))

        self.view.run_command("expand_selection", {"to": "brackets"})
        self.view.sel().add(self.view.line(self.view.sel()[0]))
