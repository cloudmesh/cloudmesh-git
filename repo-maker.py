import subprocess
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile

expanded = path_expand("~/cm")
command = f"cd {expanded}"
try:
    r = Shell.run(command)
except subprocess.CalledProcessError as e:
    if "The system cannot find the path" in str(e.output):
        command_make_dir = f"mkdir {expanded}"
        r = Shell.run(command)
try:
    r = Shell.run(f"mkdir {expanded}\my-project")
except subprocess.CalledProcessError as e:
    print(e.output)

filename = path_expand(f"{expanded}/my-project/easy-python-program.py")
writefile(filename, 'print("Hello World!")')
try:
    r = Shell.run(f"{command}/my-project; git init; git add easy-python-program.py; "
                  f"git commit -a --allow-empty-message -m ''; "
                  f"gh repo create my-project --public --source=. --remote=upstream --push"
                  f"; git push")
except subprocess.CalledProcessError as e:
    print(str(e.output))

#command = "cd ~/cm ; gh repo create my-cloudmesh-project --public --clone"
#r = Shell.run(command)