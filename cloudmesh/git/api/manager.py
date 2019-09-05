from github import Github
from cloudmesh.configuration.Config import Config
from pprint import pprint
import requests
from textwrap import dedent
from pathlib import Path
import time

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
