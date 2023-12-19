from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand
from  pathlib import Path
import os
from cloudmesh.common.console import Console


class Git:

    @staticmethod
    def root (path):
        path = path.replace("file:", "")
        path = os.path.abspath(path)
        directory = os.path.dirname(path)
        r = Shell.run(f"cd {directory} && git rev-parse --show-toplevel").strip()
        return r

    @staticmethod
    def name(path):
        path = path.replace("file:", "")
        path = os.path.abspath(path)
        repo = Git.repo(path)
        repo = repo.replace("git@github.com:", "").replace(".git", "")
        repo = repo.replace("https://github.com:", "")
        return repo

    @staticmethod
    def repo(path):
        path = path.replace("file:", "")
        path = os.path.abspath(path)
        directory = os.path.dirname(path)
        r =  Shell.run(f"cd {directory} && git config --get remote.origin.url").strip()
        return r

    @staticmethod
    def branch(path):
        path = path.replace("file:", "")
        path = os.path.abspath(path)
        directory = os.path.dirname(path)
        return Shell.run(f"cd {directory} && git rev-parse --abbrev-ref HEAD").strip()

    @staticmethod
    def filename(path):
        name = Git.name(path)
        repo = Git.repo(path)
        root = Git.root(path)
        path = path.replace("file:", "")
        path = os.path.abspath(path)
        path = path.replace(root, "")
        return path

    @staticmethod
    def blob(path):
        name = Git.name(path)
        filename = Git.filename(path)
        branch = Git.branch(path)
        return f"https://github.com/{name}/blob/{branch}/{filename}"

    @staticmethod
    def contributions_by_line():
        r = Shell.run('git ls-files | while read f; do git blame -w -M -C -C --line-porcelain "$f" '
                      '| grep \'^author \'; done | sort -f | uniq -ic | sort -nr')
        r = r.replace(" author ", " ")
        result = {}
        i = 0
        for line in r.splitlines():
            count, author = line.strip().split(" ", 1)
            i = i + 1
            result[i] = {
                'author': author,
                'count': count
            }
        return result

    @staticmethod
    def comitters():
        r =  Shell.run("git log --all --format='%an <%ae>' -- `git grep -l \"search string\"` | sort -u").strip()
        return r

    def remove_tagged_version(tag, dryrun=False):
        """
        Removes a specified Git tag locally and pushes the deletion to the remote repository.

        Args:
            tag (str): The Git tag to be removed.
            dryrun (bool): Flag indicating whether to perform a dry run.

        Example:
            Manager.remove_tagged_version("v1.0", dryrun=True)
        """

        def add_prefix_to_lines(original_string, prefix):
            lines = original_string.split('\n')
            prefixed_lines = [prefix + line for line in lines]
            result_string = '\n'.join(prefixed_lines)
            return result_string

        found = Shell.run("git tag").strip().splitlines()

        if tag in found:
            print(f"Removing tag {tag}")

            script = [
                f"git tag -d {tag}",
                f"git push origin :refs/tags/{tag}"
            ]
            if dryrun:
                msg = "  " + '\n  '.join(script)
                print(add_prefix_to_lines(msg, "dryrun"))
            else:
                try:
                    for line in script:
                        os.system(line)
                    Console.ok(f"{tag} deleted")
                except:
                    Console.error("Deletion failed")
        else:
            Console.error(f"{tag} does not exist")
