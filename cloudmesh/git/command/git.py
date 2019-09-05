from __future__ import print_function
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.git.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter

class GitCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_git(self, args, arguments):
        """
        ::

          Usage:
                git create issue --repo=REPO --title=TITLE --file=FILE [--org=ORG]
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

          Examples:

               cms git list "Park"

                  Lists all repos with the name Park in it or its description

               cms git list "fa19-523"

                    Lists all repos with the string  fa19-523 in its name


        """
        # arguments.FILE = arguments['--file'] or None

        VERBOSE(arguments)

        map_parameters(arguments,
                       'repo',
                       'file',
                       'title')

        m = Manager()

        # if arguments.FILE:
        #    print("option a")
        #    m.list(path_expand(arguments.FILE))
        #
        if arguments.list:
            m.list(arguments.MATCH)
        elif arguments.create and arguments.repo is not None:
            """
            git create issue --repo=REPO --title=TITLE --file=FILE [--org=ORG]
            """
            file = arguments.file
            title = arguments.title
            repo = arguments.repo
            repos = Parameter.expand(repo)
            m.issue(repos=repos, title=title, file=file)


        return ""
