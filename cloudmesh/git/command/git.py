from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.git.api.manager import Manager
from cloudmesh.git.copy import copy_dir
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters
import os

class GitCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_git(self, args, arguments):
        """
        ::

          Usage:
                git create issue --repo=REPO --file=FILE [--title=TITLE] [--org=ORG]
                git create repository FIRSTNAME LASTNAME GITHUBID [--org=ORG]
                git create repository --file=FILE [--org=ORG]
                git list [MATCH] [--org=ORG]
                git copy FROM TO DIRS... [--move=TMP]
                git set ssh [DIRS]

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

                git set ssh
                    switches the repository to use ssh

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

                git copy FROM TO
                    copies a directory from one repo to the other

          Examples:

               git copy FROM TO

                    git copy cloudmesh/cloudmesh-cloud cloudmesh/cloudmesh-db admin

                    creates a script move.sh that copies the directory admin
                    with history to the cloudmesh-db repo into a folder move

                    from there you can use git mv to place the content wher eyou
                    like. The reason we put it in move is that there may be another
                    dir already in it with tha name.


               cms git list "Park"

                  Lists all repos with the name Park in it or its description

               cms git list "fa19-523"

                    Lists all repos with the string  fa19-523 in its name


        """
        # arguments.FILE = arguments['--file'] or None

        map_parameters(arguments,
                       'fetch',
                       'move',
                       'repo',
                       'file',
                       'title')
        move = arguments.move or "move"

        VERBOSE(arguments)


        # if arguments.FILE:
        #    print("option a")
        #    m.list(path_expand(arguments.FILE))
        #
        if arguments.list:

            m = Manager()

            m.list(arguments.MATCH)

        elif arguments.create and arguments.repo is not None:
            """
            git create issue --repo=REPO --title=TITLE --file=FILE [--org=ORG]
            """
            m = Manager()

            file = arguments.file
            title = arguments.title
            repo = arguments.repo
            repos = Parameter.expand(repo)
            m.issue(repos=repos, title=title, file=file)

        elif arguments.repository and arguments.file and not arguments.issue:

            m = Manager()
            filename = arguments.file
            m.create_repos(filename=filename)

        elif arguments.copy:

            dirs = arguments.DIRS
            original = arguments.FROM
            destination = arguments.TO
            move = arguments.move

            copy_dir(original=original,
                     destination=destination,
                     directories=dirs,
                     move=move)

        elif arguments.ssh and arguments.set:

            dirs = arguments["DIRS"] or "."
            org = "get the org from the current dir in .git"
            repo = "get the repo from the current dir in .git"


            for d in dirs:
                if d == ".":
                    location = ""
                else:
                    location = "cd {d}; "
            os.system(f"{location} git remote set-url origin git@github.com:{org}/{repo}.git")

        return ""
