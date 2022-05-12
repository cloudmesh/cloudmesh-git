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

    def test_help(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_git_newlist_all(self):
        "git newlist [--all]"
        HEADING()
        Benchmark.Start()
        result = Shell.execute("git newlist --all", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "No help on wrong" in result

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="git")
