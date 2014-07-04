#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Alec Thomas
# Copyright (c) 2014 Alec Thomas
#
# License: MIT
#

"""This module exports the Errcheck plugin class."""

from os import listdir
from os.path import dirname
from SublimeLinter.lint import Linter, util, highlight


class Errcheck(Linter):

    """Provides an interface to errcheck (https://github.com/kisielk/errcheck)."""

    syntax = ('go', 'gosublime-go')
    cmd = 'errcheck'
    regex = r'^[^:]+?:(?P<line>\d+):(?P<col>\d+)(?P<message>.*)$'
    error_stream = util.STREAM_BOTH
    default_type = highlight.WARNING
    tempfile_suffix = '-'

    def split_match(self, match):
        split = super().split_match(match)
        if not split[0]:
            return split

        match, line, col, error, warning, message, near = split
        message = 'returned error not checked'
        return match, line, col, error, warning, message, near

    def run(self, cmd, code):
        files = [f for f in listdir(dirname(self.filename)) if f.endswith('.go')]
        return self.tmpdir(cmd, files, code)
