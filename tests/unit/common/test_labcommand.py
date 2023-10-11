import pytest
import shutil
import tempfile
import pathlib
import labs.common.labcommand as labcommand
import labs.lablog as lablog


class TestSshReturns:
    """
    check_sshkey()
    """

    def test_sshkey_filedoesnotexist(self):
        item = {
            'sshkey': '/home/student/.ssh/filedoesnotexist',
            }
        returned_sshkey = labcommand.check_sshkey(item)
        assert returned_sshkey == '/home/student/.ssh/lab_rsa'

    def test_sshkey_defaultfile(self):
        item = {
            'sshkey': '/home/student/.ssh/lab_rsa',
            }
        returned_sshkey = labcommand.check_sshkey(item)
        assert returned_sshkey == '/home/student/.ssh/lab_rsa'

    def test_ssh_key_notdict(self):
        with pytest.raises(TypeError):
            item = 100
            labcommand.check_sshkey(item)


@pytest.fixture()
def setup_test():
    temp_dir = tempfile.mkdtemp()
    config = {"rhtlab": {
        "logging": {"path": temp_dir},
        }
    }
    lab_name = "lab_01_1"
    shutil.rmtree(temp_dir, ignore_errors=True)
    expected_file =\
        pathlib.Path(config["rhtlab"]["logging"]["path"]) / lab_name
    config["rhtlab"]["logging"]["path"] += "/"
    config["rhtlab"]["logging"]["capture_output"] = True
    lablog.lablog_init(config, lab_name)

    yield expected_file


class TestLog:
    """
    log_stdin()
    log_stdout()
    log_stderr()
    log_errormsg()
    """

    def test_log_stdin(self, setup_test):
        """Test that stdin is captured."""

        labcommand.log_stdin("Test stdin")
        assert setup_test.is_file()
        with open(setup_test) as f:
            content = f.read()
        assert "\n\nSTDIN: \n\nTest stdin" in content

    def test_log_stdout(self, setup_test):
        """Test that stdout is captured."""

        labcommand.log_stdout("Test stdout")
        assert setup_test.is_file()
        with open(setup_test) as f:
            content = f.read()
        assert "\n\nSTDOUT: \n\nTest stdout" in content

    def test_log_stderr(self, setup_test):
        """Test that stderr is captured."""

        labcommand.log_stderr("Test stderr")
        assert setup_test.is_file()
        with open(setup_test) as f:
            content = f.read()
        assert "\n\nSTDERR: \n\nTest stderr" in content

    def test_log_errormsg(self, setup_test):
        """Test that errormsg is captured."""

        item = [{"msgs": "Test errormsg"}]
        labcommand.log_errormsg(item)
        assert setup_test.is_file()
        with open(setup_test) as f:
            content = f.read()
        assert "\n\nERROR MESSAGES: \n\nTest errormsg" in content
