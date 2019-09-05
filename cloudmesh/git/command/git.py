from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.git.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE

class GitCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_git(self, args, arguments):
        """
        ::

          Usage:
                git create issue BUNDLE --file=FILE [--org=ORG]
                git create issue --repo=REPO FILE [--org=ORG]
                git create repo NAME FIRSTNAME LASTNAME GITHUBID [--org=ORG]
                git create repo --file=FILE [--org=ORG]
                git list [MATCH] [--org=ORG]


          This command does some useful things.

          Arguments:
              FILE   a file name
              ORG    [default: cloudmesh-community]
              MATCH  is a string that must occur in the repo name or description
              --file=FILE   specify the file
              --repo=REPO   the repository

          Options:

          Description:

                The organization is set by default to
                cloudmesh-community

                git list

                    lists the repos of the organization

                git create issue BUNDLE FILE

                   Create an issue in the given bundle.
                   The bundle is defined in cloudmesh-installer
                   The content of the issue is specified in the file

                git create issue --repo=REPO FILE
                   Create an issue in the given repos.
                   Note that the repos is a string defined as
                   cloudmesh.Parameter, E.g. fa19-516-[100-103,105]
                   effects the repos ending with 100, 101, 102,
                   103, and 105

                   The bundle is defined in cloudmesh-installer

                git create repo NAME FIRSTNAME LASTNAME GITHUBID
                    creates the repo

                git create repo --file=repos.csv
                    creates repos from a file in csv format
                    the format in th csv file is

                    reponame,lastname,firstname,githubid

        """
        # arguments.FILE = arguments['--file'] or None

        VERBOSE(arguments)

        m = Manager()

        # if arguments.FILE:
        #    print("option a")
        #    m.list(path_expand(arguments.FILE))
        #
        if arguments.list:
            m.list(arguments.MATCH)
        return ""
