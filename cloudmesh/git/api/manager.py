from github import Github
from cloudmesh.configuration.Config import Config
from pprint import pprint
import requests
from textwrap import dedent
from pathlib import Path
import time
import csv

class Manager(object):

    def __init__(self, organization="cloudmesh-community"):
        config = Config()

        g = Github(config["cloudmesh.github.user"],
                   config["cloudmesh.github.password"])


        if organization != "cloudmesh-community":
            raise ValueError("currently we support only organization cloudmesh-community")

        self.org = g.get_organization(organization)
        self.ta_team = self.org.get_team(2631498)

    def list(self, match=None):
        for r in self.org.get_repos():
            if match is None:
                print (r.name, r.description)
            else:
                name = r.name or ""
                description = r.description or ""
                if match in name or match in description:
                    print (r.name, r.description)

    def create_repo(self,
                     firstname=None,
                     lastname=None,
                     repo=None,
                     community=None,
                     semester="fa19",
                     githubid=None,
                     ):

        description = f"{firstname} {lastname}"
        repo = self.org.create_repo(repo,
                               description=description,
                               license_template="apache-2.0")
        readme = dedent(f"""
                    ---
                    owner:
                      firstname: "{firstname}"
                      lastname: "{lastname}"
                      hid: "{repo}"
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

        with open(Path("../.gitignore").resolve()) as file:
            gitignore = file.read()

        repo.create_file(".gitignore", "create the .gitignore", gitignore,
                         branch="master")

        try:
            repo.add_to_collaborators(githubid, permission="write")
        except Exception as e:
            pass
        self.ta_team.add_to_repos(repo)
        self.ta_team.set_repo_permission(repo, "write")


    def create_repos(self, filename):

        with open('names.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')

            
            for row in reader:
                print(row['first_name'], row['last_name'])

        print ("create Repos")
        '''
        for r in repos:
            name = r[0]
            description = r[1]
            firstname, lastname = description.split(" ", 1)
            username = r[2]
            print("creating", name, description)
            repo = org.create_repo(name,
                                   description=description,
                                   license_template="apache-2.0")
            readme = dedent(f"""
                ---
                owner:
                  firstname: "{firstname}"
                  lastname: "{lastname}"
                  hid: "{name}"
                  community: "523"
                  semester: "fa19"
                """).strip()

            print(readme)
            print("Add README.yaml")
            repo.create_file("README.yml", "create the Readme.yaml", readme,
                             branch="master")

            print("Add .gitignore")

            with open(Path("../.gitignore").resolve()) as file:
                gitignore = file.read()

            repo.create_file(".gitignore", "create the .gitignore", gitignore,
                             branch="master")

            try:
                repo.add_to_collaborators(username, permission="write")
            except Exception as e:
                pass
            ta_team.add_to_repos(repo)
            ta_team.set_repo_permission(repo, "write")
        '''