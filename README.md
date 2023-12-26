Documentation
=============


[![GitHub Repo](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/cloudmesh/cloudmesh-git)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-git.svg)](https://pypi.org/project/cloudmesh-git)
[![image](https://img.shields.io/pypi/v/cloudmesh-git.svg)](https://pypi.org/project/cloudmesh-git/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![General badge](https://img.shields.io/badge/Status-Production-<COLOR>.svg)](https://shields.io/)
[![GitHub issues](https://img.shields.io/github/issues/cloudmesh/cloudmesh-git.svg)](https://github.com/cloudmesh/cloudmesh-git/issues)
[![Contributors](https://img.shields.io/github/contributors/cloudmesh/cloudmesh-git.svg)](https://github.com/cloudmesh/cloudmesh-git/graphs/contributors)
[![General badge](https://img.shields.io/badge/Other-repos-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh)


[![Linux](https://img.shields.io/badge/OS-Linux-orange.svg)](https://www.linux.org/)
[![macOS](https://img.shields.io/badge/OS-macOS-lightgrey.svg)](https://www.apple.com/macos)
[![Windows](https://img.shields.io/badge/OS-Windows-blue.svg)](https://www.microsoft.com/windows)

see cloudmesh.cmd5

* https://github.com/cloudmesh/cloudmesh.cmd5


## Installation

```bash
pip install cloudmesh-git
```

## Development Intsllation

```bash
git clone https://github.com/cloudmesh/cloudmesh-git.git
git clone https://github.com/cloudmesh/cloudmesh-common.git
cd cloudmesh-git
```

To create a while instalation you can say

```bash
make local
```

To create an editable instalation with pip use

```bash
make pip
```



## TODO

* create gh class
* develop api for most useful things for us

What is most useful

* create repo given name in csv file with
  * firstname, lastname, githubid, hid (hid we define and is incremental number, hid<number>) 
  * add README.md
  * add LICENSE
  * add a directory copy from a sample repo
    * latex document
    * markdown document
    * cloudmesh dir with small readme how to create a cms command
  
## Acknowledgments

Continued work was in part funded by the NSF
CyberTraining: CIC: CyberTraining for Students and Technologies
from Generation Z with the awadrd numbers 1829704 and 2200409. 



## Manual Page

<!-- START-MANUAL -->
```
Command git
===========

::

  Usage:
        git contribution
        git committers
        git create issue --repo=REPO --file=FILE [--title=TITLE] [--org=ORG]
        git create repository FIRSTNAME LASTNAME GITHUBID [--org=ORG]
        git create repository --file=FILE [--org=ORG]
        git list all [--exclude=ORG]
        git list --org=ORG [MATCH]
        git copy FROM TO DIRS... [--move=TMP]
        git set ssh [DIRS]
        git --refresh
        git clone all [--force=no]
        git pull all [--dryrun]
        git pull [--dryrun] DIRS...
        git status [--dryrun] [--changed] [--verbose] DIRS...
        git upload
        git log
        git versions [--repo=REPO]
        git issues [--repo=REPO] [--assignee=ASSIGNEE] [--format=HTML] [--out=a.html] [--refresh]
        git delete [--tag=TAG] [--dryrun]

  This command does some useful things.

  Arguments:
      FILE   a file name
      ORG    [default: cloudmesh-community]
      MATCH  is a string that must occur in the repo name or description
      --file=FILE   specify the file
      --repo=REPO   a parameterized list of repo links. If cloudmesh- is the prefix it will be
                    automatically replaced by the repo url. REPO is a parameterized list with
                    comma separated so that multiple repos can be used.
                    If REPO is a filename, each line specifies a repo. the cloudmesh prefix
                    replacement is applied on each line
                    If repo is . or the parameter is omitted, all directories in the current
                    directory are used to list their issues
     --assignee=ASSIGNEE  a list of assignees so only issues for these users are displayed
                          if it is ommitted all issues for assignees are displayed.
     --refresh  only download the GitHub issue list if --refresh is uses, otherwise it uses a local cache in
                ~/.cloudmesh/issuelist.json
     --tag=TAG  A list of tags that can be specified with number ranges.
                E.g. v100.0.[4-6] will give the tags v100.0.4, v100.0.5, v100.0.6
     --dryrun  onyl disply, but do not run the deletion
     --changed  only display repos that have changes
     --verbose  prints verbose information

  Options:
      --force=no    pull the repository if it already exists in current working directory [default: no]

  Description:

        The organization is set by default to
        cloudmesh-community

        git --refresh
            Finds all organizations and repositories the current user belongs to
            redirects automatically to ~/cloudmesh/git/repo-list.txt

        git clone all [--force=no]
            Uses all organizations and repositories of the user and
            clones them into the current directory, while making each
            organization in its own subdirectory
            uses automatically ~/cloudmesh/git/repo-list.txt
            which can be created with cms git list all.
            if force is yes then it pulls preexisting directories.

        git set ssh
            Switches the repository to use ssh

        git list --org=ORG
            Lists the repos of the organization

        git list all [--exclude=ORG]
            Gets info of all repos of the current in user. It puts
            the result in ~/.cloudmesh/gitcache.txt.
            To exclude an organization, add it to the end of exclude
            parameter.

        git create issue --repo=REPO FILE
           Create an issue in the given repos.
           Note that the repos is a string defined as
           cloudmesh.Parameter, E.g. fa19-516-[100-103,105]
           effects the repos ending with 100, 101, 102,
           103, and 105

           The bundle is defined in cloudmesh-installer

        git create repo NAME FIRSTNAME LASTNAME GITHUBID
            Creates the repo

        git create repo --file=repos.csv
            Creates repos from a file in csv format
            the format in th csv file is

            reponame,lastname,firstname,githubid

        git copy FROM TO
            Copies a directory from one repo to the other.

        git pull cloudmesh-*
            Assuming in your directory there are cloudmesh source repositories
            this command does a git pull on all of them. Using . as the directory
            will pull all repos in the current directory.

        git issuelist
            Creates html file of all issues assigned to logged-in
            user. assumes that the user is standing in cm
            directory

        git log
            A very short log sorted by date

  Examples:

       git copy FROM TO

            git copy cloudmesh/cloudmesh-cloud cloudmesh/cloudmesh-db admin

            Creates a script move.sh that copies the directory admin
            with history to the cloudmesh-db repo into a folder move

            From there you can use git mv to place the content where you
            like. The reason we put it in move is that there may be another
            dir already in it with tha name.

       git list Park
            Lists all repos with the name Park in it or its description

       git list fa19-523
            Lists all repos with the string  fa19-523 in its name

        cms git versions
            returns information about the versions of the current repo. An example is

            > Checking versions for .
            > current_branch   : main
            > latest_tag       : v5.0.5
            > VERSION          : 5.0.5
            > github_version   : 5.0.5
            > pypi_version     : 5.0.5
            > last_commit_hash : aa29c031f22af42f8e54af44afbf5d8ca4d801fe
            > last_version_hash: d82b47cc62c6149d4d14b471a38d85dd5a43a93a
            > last_commit_date : 2023-12-22 21:08:13 -0500
            > last_version_date: 2023-12-22 21:05:29 -0500
            > time_difference  : 2m 44s
            > commits_after_tag: 1

```
<!-- STOP-MANUAL -->