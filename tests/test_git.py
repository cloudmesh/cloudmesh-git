###############################################################
# pytest -v --capture=no tests/test_git.py
# pytest -v  tests/test_git.py
# pytest -v --capture=no  tests/test_git..py::test_git::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING


@pytest.mark.incremental
class TestGit:

    # export GITUSER=laszewski
    # gituser = os.environ["GITUSER"]
    def test_help(self):
        HEADING()
        Benchmark.Start()
        result = Shell.run("cms help")
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_remove_cache(self):
        HEADING()
    # if cache exists, remove
    #    assert not existance of cache
        raise NotImplementedError
        assert False

    def test_issues(self):
        "git newlist [--all]"
        HEADING()
        Benchmark.Start()
        result = Shell.run("cms git issues")
        Benchmark.Stop()
        VERBOSE(result)

        # assert existance of cache
        assert "No help on wrong" in result

    def test_git_newlist_all(self):
        "git newlist [--all]"
        HEADING()
        Benchmark.Start()
        result = Shell.run("cms git newlist --all")
        Benchmark.Stop()
        VERBOSE(result)

        assert "No help on wrong" in result

    # gh issue list --assignee "laszewsk" --assignee "dkkolli" --json=title,assignees,url,labels


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="git")
