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

    def issues(self, assignee="@me", path=".", name=None):
        r = None
        directory = path_expand(path)
        if assignee is None:
            parameter = ""
        else:
            parameter = f'--assignee "{assignee}"'
        command = f'cd {directory} && gh issue list {parameter} --json=title,assignees,url,labels'
        try:
            r = Shell.run(command)
            r = json.loads(r)
        except Exception as e:
            print(e)
        return r

    def issues_to_table(self, entries, name=None):

        result = [
            f'<br><b>{name}</b><br><br>',
            '<table frame="border" rules="all" border-spacing="30px";>']
        line = f'<tr><th> repo </th><th> url </th><th> title </th><th> assignees</th><th> labels</th></tr>'
        result.append(line)

        if entries:
            for entry in entries:
                url = entry['url']
                title = entry['title']
                assignees = entry['assignees']
                labels = entry['labels']
                n = os.path.basename(url)
                repo = os.path.dirname(url)
                repo_url = os.path.dirname(repo)
                repo_name = repo_url.replace("https://github.com", "")
                entry['repo'] = f'<a href="{repo_url}"> {repo_name} </a>'
                entry['url'] = f'<a href="{url}"> {n} </a>'
                entry['title'] = f'<a href="{url}"> {title} </a>'
                entry['assignees'] = ",".join(
                    [f'<a href="https://github.com/{assignee["login"]}"> {assignee["name"] or assignee["login"]} </a>'
                     for assignee in assignees])
                if len(labels) > 0:
                    entry['labels'] = ",".join([label['name'].replace("PRIORITY ", "") for label in labels])
                else:
                    entry['labels'] = ""
                line = f'<tr>'\
                       f'<td> {entry["repo"]} </td>'\
                       f'<td> {entry["url"]} </td>'\
                       f'<td> {entry["title"]} </td>'\
                       f'<td> {entry["assignees"]}</td>'\
                       f'<td>{entry["labels"]}<td>'\
                       '</tr>'
                result.append(line)
            result.append("</table>")
            result = "\n".join(result)
        else:
            result = None
        return result