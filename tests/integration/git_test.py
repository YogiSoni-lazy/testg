from src.labs.common.git import repository


def test_git_clone(tmpdir):
    """
    Clone a remote repository into a temp dir and check
    the local repository exists in the temp dir
    """

    localpath = tmpdir.join("iconfont")

    repository.clone(
        # A small repo makes the test quicker
        "https://github.com/RedHatOfficial/rh-iconfont",
        localpath
    )

    assert repository.exists(localpath)
