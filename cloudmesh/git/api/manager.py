from github import Github
from cloudmesh.configuration.Config import Config
from pprint import pprint
import requests
from textwrap import dedent
from pathlib import Path
import time
import csv
from cloudmesh.common.util import readfile
from cloudmesh.common.console import Console
import os
class Manager(object):

    def __init__(self, organization="cloudmesh-community"):
        config = Config()

        try:
            g = Github(config["cloudmesh.github.user"],
                       config["cloudmesh.github.password"])
        except KeyError:
            Console.error("Make sure the cloudmesh.yaml file defines both \n"
                          "         cloudmesh.github.user\n"
                          "         cloudmesh.github.password")
            raise ValueError("cloudmesh.github")

        if organization != "cloudmesh-community":
            raise ValueError(
                "currently we support only organization cloudmesh-community")

        self.org = g.get_organization(organization)
        self.ta_team = self.org.get_team(2631498)

    def list(self, match=None, verbose=False):
        Manager._list(self.org, match=match, verbose=verbose)

    @staticmethod
    def _list(org, match=None, verbose=False):
        if verbose:
            Console.msg(f"Organization: {org}")
        for r in org.get_repos():
            if match is None:
                print(r.name, r.description)
            else:
                name = r.name or ""
                description = r.description or ""
                if match in name or match in description:
                    print(r.name, r.description)



    @staticmethod
    def _create_empty_repo(
                          org,
                          name,
                          source="",
                          ):
        try:
            repo = org.create_repo(name)
        except Exception as e:
            msg = e._GithubException__data["message"] + "  " + \
                  e._GithubException__data["errors"][0]["message"].capitalize() +"."
            Console.error (msg)
            raise e
        #mirror = dedent(f'''
        #                ---
        #                 mirror:
        #                   org: "{org.__dict__}"
        #                   source: "{source}"
        #                   name: "{name}"
        #                 ''').strip()
        #print(mirror)


    @staticmethod
    def mirror(
             orgfrom=None,
             orgto=None,
             repo=None,
             verbose=False,
             force=False):

        config = Config()
        g = Github(config["cloudmesh.github.token"])

        org = g.get_organization(orgto)

        print (org)
        #  Manager._list(org)

        #print ("KKKK")
        try:
            Manager._create_empty_repo(org, repo, source=orgfrom)
        except:
            Console.error(f"mirror failed: {orgfrom}/{repo} -> {orgto}/{repo}")
            if not force:
                return ""

        script = dedent(f"""
        cd /tmp; rm -rf {repo}.git
        cd /tmp; git clone --mirror https://github.com/{orgfrom}/{repo}.git
        cd /tmp/{repo}.git
        cd /tmp/{repo}.git; git remote set-url --push origin https://github.com/{orgto}/{repo}
        cd /tmp/{repo}.git; git fetch -p origin
        cd /tmp/{repo}.git; git push --mirror
        cd /tmp; rm -rf {repo}.git
        """).strip()
        for line in script.split("\n"):
            os.system(line)




    def create_repo(self,
                    firstname=None,
                    lastname=None,
                    name=None,
                    community=None,
                    semester="fa19",
                    githubid=None
                    ):

        description = f"{firstname} {lastname}"
        repo = self.org.create_repo(name,
                                    description=description,
                                    license_template="apache-2.0")
        readme = dedent(f"""
                    ---
                    owner:
                      firstname: "{firstname}"
                      lastname: "{lastname}"
                      hid: "{name}"
                      community: "{community}"
                      semester: "{semester}"
                    """).strip()

        print(readme)
        print("Add README.yml")
        repo.create_file("README.yml",
                         "Create the Readme.yml",
                         readme,
                         branch="master")

        print("Add .gitignore")

        # bug find file within distribution

        with open(Path(".gitignore").resolve()) as file:
            gitignore = file.read()

        repo.create_file(".gitignore", "create the .gitignore", gitignore,
                         branch="master")

        try:
            repo.add_to_collaborators(githubid, permission="write")
        except Exception as e:
            pass
        self.ta_team.add_to_repos(repo)
        self.ta_team.set_repo_permission(repo, "write")

    def create_repos(self, filename=None):

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')

            for row in reader:
                firstname = row['firstname']
                lastname = row['lastname']
                githubid = row['githubid']
                community = row['community']
                semester = row['semester']
                name = row['repo']
                print(f"Create: {name} {firstname} {lastname} {githubid}")
                self.create_repo(
                    firstname=firstname,
                    lastname=lastname,
                    name=name,
                    community=community,
                    semester=semester,
                    githubid=githubid
                )

    def issue(self, repos=None, title=None, file=None):
        pprint(repos)
        for repo in repos:
            if file is not None:
                content = readfile(file).strip()

                if title is None:
                    title = content.splitlines()[0]
                    title = title.replace("#", "").strip()

                repository_obj = self.org.get_repo(repo)
                repository_obj.create_issue(title=title, body=content)
