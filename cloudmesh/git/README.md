
cms git copy cloudmesh/cloudmesh-cloud cloudmesh/cloudmesh-admin cloudmesh/admin cloudmesh/check cloudmesh/management cloudmesh/source cloudmesh/start cloudmesh/stop


x.sh

remove files and history that are no longer in git

remove empty commits

not working?

git filter-branch --commit-filter 'git_commit_non_empty_tree "$@"' -f HEAD
rm -rf .git/refs/original/ && git reflog expire --all &&  git gc --aggressive --prune