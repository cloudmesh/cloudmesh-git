from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand
import json
import os

class Gh:

    def __int__(self):
        pass

    def run(self, command, path="."):
        directory = path_expand(path)
        command = f'cd {directory} && {command}'
        try:
            r = Shell.run(command)
        except Exception as e:
            print(str(e.output))

    def issues(self, assignee="@me", path="."):
        r = None
        directory = path_expand(path)
        if assignee is None:
            parameter = ""
        else:
            parameter = f'--assignee "{assignee}"'
        command = f'cd {directory} && gh issue list {parameter} --json=title,assignees,url'
        try:
            r = Shell.run(command)
            r = json.loads(r)
        except Exception as e:
            print(str(e.output))
        return r


    def issues_to_table(self, entries):
        result = ['<table frame="border" rules="all">']
        line = f'<tr><th> url </th><th> title </th><th> assignees</th></tr>'
        result.append(line)

        for entry in entries:
            url = entry['url']
            title = entry['title']
            assignees = entry['assignees']
            n = os.path.basename(url)
            repo = os.path.dirname(url)
            repo_url = os.path.dirname(repo)
            repo_name = repo_url.replace("https://github.com", "")
            entry['repo'] = f'<a href="{repo_url}"> {repo_name} </a>'
            entry['url'] = f'<a href="{url}"> {n} </a>'
            entry['title'] = f'<a href="{url}"> {title} </a>'
            entry['assignees'] = ",".join([f'<a href="github.com/{assignee["login"]}"> {assignee["name"]} </a>'
                                           for assignee in assignees])
            line = f'<tr><td> {entry["repo"]} </td> <td> {entry["url"]} </td><td> {entry["title"]} </td><td> {entry["assignees"]}</td></tr>'
            result.append(line)
        result.append("</table>")
        result = "\n".join(result)

        return result