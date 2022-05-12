from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.util import str_bool
from cloudmesh.git.api.manager import Manager
from cloudmesh.git.copy import copy_dir
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters
from github import Github
import os
import requests
import json

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
                git list HANDLE [--forks=no] [--archived=no]
                git copy FROM TO DIRS... [--move=TMP]
                git set ssh [DIRS]
                cms git --refresh # redirects automatically to ~/cloudmesh/git/repo-list.txt
                cms git clone --all # uses automatically ~/cloudmesh/git/repo-list.txt

          This command does some useful things.

          Arguments:
              FILE           a file name
              ORG            [default: cloudmesh-community]
              MATCH          is a string that must occur in the repo name or description
              HANDLE         username or organization name on github
              --file=FILE    specify the file
              --repo=REPO    the repository


          Options:
              --forks=no     include forked repos in list. if no, then don't include forks [default: no]
              --archived=no  include archived repos in list. if no, then don't include archived [default: no]

          Description:

                The organization is set by default to
                cloudmesh-community

                cms git --refresh
                    finds all organizations and repositories the current user belongs to
                    redirects automatically to ~/cloudmesh/git/repo-list.txt

                cms git clone --all
                    uses all organizations and repositories of the user and
                    clones them into the current directory, while making each
                    organization in its own subdirectory
                    uses automatically ~/cloudmesh/git/repo-list.txt
                    which can be created with cms git --refresh

                git set ssh
                    switches the repository to use ssh

                git list HANDLE [--forks=no] [--archived=no]
                    lists the repos of the user and/or organization

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
                       'title',
                       'forks',
                       'archived')
        move = arguments.move or "move"

        VERBOSE(arguments)


        # if arguments.FILE:
        #    print("option a")
        #    m.list(path_expand(arguments.FILE))
        #
        if arguments.list:
            '''
            m = Manager()

            m.list(arguments.MATCH)
            '''

            req = requests.get(f'https://api.github.com/users/{arguments.HANDLE}')
            if req.status_code == 404:
                Console.error(f"User {arguments.HANDLE} does not exist!")
                return
            is_getting_forks = str_bool(arguments.forks)
            is_getting_archived = str_bool(arguments.archived)

            my_dir = os.path.expanduser('~/.cloudmesh/git/')
            if not os.path.isdir(my_dir):
                os.mkdir(my_dir)
            command = f"curl -o {my_dir}repo-list-{arguments.HANDLE}.json " \
                      f"https://api.github.com/users/{arguments.HANDLE}/repos"
            r = Shell.run(command)

            # open json file
            f = open(f'{my_dir}repo-list-{arguments.HANDLE}.json')
            # make a dictionary
            dict_data = json.load(f)

            repos = []
            # print repos
            for i in dict_data:
                if not is_getting_forks:
                    if (i["fork"]):
                        continue
                if not is_getting_archived:
                    if (i["archived"]):
                        continue
                repos.append(i["name"])
                print(i["name"])

            print(repos)
            with open(f'{my_dir}repo-list-{arguments.HANDLE}.txt', 'w') as file2:
                for item in repos:
                    file2.write("%s\n" % item)
            Console.ok(f'\nWritten list of repos to {my_dir}repo-list-{arguments.HANDLE}.txt')
            f.close()
            file2.close()

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
