from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand
from  pathlib import Path
import os
from cloudmesh.common.console import Console
import time
import subprocess
import os
import os
import requests
from cloudmesh.common.util import banner

class Git:

    @staticmethod
    def execute_git_command(dirs, command, dryrun=False):
        """
        Execute a git command on the specified directories.

        Args:
            dirs (list): The list of directories the commandis run in.
            command (str): The git command to execute.
        """
        if dirs == ['.']:
            directories = Git.find_git_directories(".")
        else:
            directories = dirs

        for path in directories:
            git_command = f"git -C {path} {command}"
            if dryrun:
                print(git_command)
            else:
                banner(git_command)
                os.system(git_command)

    @staticmethod
    def reponame(repo):
        """
        Returns the repository name. If it starts with 'cloudmesh-', prefix 'cloudmesh/' is added.

        Args:
            repo (str): The name of the repository.

        Returns:
            str: The modified repository name.
        """
        if repo.startswith('cloudmesh-'):
            return f'cloudmesh/{repo}'
        else:
            return repo

    @staticmethod
    def fetch_latest_release_version(repo):
        # repo = cloudmesh/cloudmesh-git
        repo = Git.reponame(repo)

        url = f"https://api.github.com/repos/{repo}/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latest_version = data["tag_name"]
            return latest_version
        else:
            return None
    
    @staticmethod
    def fetch_version_from_git_repo(repo):
        repo = Git.reponame(repo)
        
        url = f"https://raw.githubusercontent.com/{repo}/main/VERSION"
        response = requests.get(url)
        if response.status_code == 200:
            version = response.text.strip()
            return version
        else:
            return None
            
    @staticmethod
    def fetch_latest_pypi_version(package_name):
        """
        Fetch the latest version of a package from PyPI.

        Args:
            package_name (str): The name of the package.

        Returns:
            str: The latest version of the package, or None if the package was not found.
        """
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latest_version = data["info"]["version"]
            return latest_version
        else:
            return None
    
    @staticmethod
    def get_versions(package_name):
        """
        Compares the versions of a Git repository with the versions available on PyPI.

        Args:
            repo (str): The URL of the Git repository.

        Returns:
            bool: True if the Git repository versions match the PyPI versions, False otherwise.
        """
        print(f"Checking versions for {package_name}")

        if package_name == ".":
            package_name = os.path.basename(os.getcwd())
        repo = Git.reponame(package_name)
        github_version = Git.fetch_version_from_git_repo(repo)
        pypi_version = Git.fetch_latest_pypi_version(package_name=package_name)
        
        VERSION = None

        if os.path.isfile("VERSION"):
            VERSION = Path("VERSION").read_text().strip()   

        return {
            "VERSION": VERSION,
            "github_version": github_version, 
            "pypi_version": pypi_version}
        
    @staticmethod
    def find_git_directories(directory):
        git_directories = []
        
        for subdir in os.listdir(directory):
            subdir_path = os.path.join(directory, subdir)
            if os.path.isdir(subdir_path):
                if Git.is_git_repository(subdir_path):
                    git_directories.append(subdir_path)
                
        return git_directories

    @staticmethod
    def is_git_repository(directory):
        try:
            subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'], cwd=directory)
            return True
        except subprocess.CalledProcessError:
            return False
            
    @staticmethod
    def upload(repo_url=None, commit_message='Initial_commit'):
        """
        Create a new Git repository, add the code from the current directory, and push it to a remote repository.

        Args:
            repo_url (str): The URL of the remote repository.
            commit_message (str, optional): The commit message. Defaults to 'Initial commit'.
        """

        if repo_url is None:
            repo_name = os.path.basename(os.getcwd())
            repo_url = f"git@github.com:cloudmesh/{repo_name}.git"

        commands = f"""
            git init
            git add .
            git commit -m {commit_message}
            git remote add origin {repo_url}
            git push -u origin main
        """.strip()

        commands_list = commands.strip().split('\n')

        for command in commands_list:
            try:
                subprocess.run(command.split(), check=True)
            except:
                pass    

        #for command in commands:
        #    subprocess.run(command, check=True)

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
