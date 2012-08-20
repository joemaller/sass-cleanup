import sublime_plugin
import subprocess
import os
import re
from glob import glob

print "loaded Sassify"

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
#       Actual error handling


class SassifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.env = os.environ.copy()
        # Create a "default indentation string" which is either several spaces or a tab
        self.tabs_to_spaces = self.view.settings().get('translate_tabs_to_spaces')
        self.indentation = ["\t", " "][self.tabs_to_spaces]
        if self.tabs_to_spaces:
            self.indentation = self.indentation * self.view.settings().get('tab_size')

        # TODO look for a better way of accessing the user's environment variables
        paths = [
            self.env["PATH"],
            'usr/bin',  # default install Sass install location from `sudo gem install sass`
            os.path.expanduser('~/.rbenv/shims'),  # this and the following path are necessary to run Ruby from rbenv
            os.path.expanduser('~/.rbenv/bin'),
            '/opt/local/bin',
            ]

        # Homebrew-installed Ruby gems have a messy path
        paths.extend(glob('/usr/local/Cellar/ruby/*/bin'))
        self.env["PATH"] = os.pathsep.join(paths)

        for region in self.view.sel():
            if not region.empty():
                # Get the selected text
                s = self.view.substr(region)
                print self.view.sel()
                # print whole_region

                print "did we get here?"
            else:
                print 'empty region'
                # try expanding to enclosing brackets

                # run this twice to include brackets. Kludgy hack that totally fails with multiple selections:
                self.view.run_command("expand_selection", {"to": "brackets"})
                self.view.run_command("expand_selection", {"to": "brackets"})
                print self.view.sel()
                # for region in self.view.sel():
                #     s = self.view.substr(region)

            try:
                s = self.runSass(s, indentation=self.indentation)
                # Replace the selection with transformed text
                self.view.replace(edit, region, s)
            except Exception, e:
                print e


                # TODO capture the current CSS rule by:
                #       1. look for a bracket in the line, try to exand selection to bracket
                #          entend selection to beginning of line
                #       2. Or just search for this?  ^[^{]+[^}]

    def runSass(self, args, **kwargs):
        indent = kwargs.get('indentation', '    ')  # set default indent value
        print "indent: %s" % repr(indent)
        sass_convert = subprocess.Popen(
           # TODO need to make scss conditional based on the current file or scope
            # ['sass-convert', '-s', '-F', 'scss', '-T', 'scss', '--trace'],
            ['sass-convert', '-s', '-F', 'scss', '-T', 'scss'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env)
        sass_converted = sass_convert.communicate(args)
        if not sass_converted[0]:
            # there was an error
            # TODO handle this better
            print sass_converted[1]
            return False
        sass_converted = sass_converted[0]

        # TODO: make this replacement conditional based on a preference:
        sass_converted = self.bracket_outdenter(sass_converted)

        # use this as the basis of correcting indentation to match ST2's indentation settings
        sass_converted = re.sub(r'  ', indent, sass_converted)
        # clean up extra newlines
        sass_converted = re.sub(r"\n+", "\n", sass_converted)
        # add one additional newline and return
        return sass_converted + "\n"

    def bracket_outdenter(self, code):
        """
        outdents trailing brackets
        note the 2-space sass-convert default is hard coded for now
        """
        bracket_regex = r'^(?P<rule>(?P<indent> *)[^}\n]+)(?P<brackets>(?: \})+)$'
        bracket_regex = re.compile(bracket_regex, re.M)
        code = bracket_regex.sub(lambda m: "%s\n%s" % (
                            m.group('rule'),
                            ''.join([m.group('indent')[i * 2:-2] + '}\n' for i in range(len(m.group('brackets').split()))])),
                        code)
        return code.rstrip()
