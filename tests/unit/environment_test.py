import pytest
from src.labs import environment


def test_get_pypi_url_raises_exception():
    """
    get_pypi_url should raise an exception
    when the specified environment is not "test" or "prod"
    """
    # Given
    envname = "fake_env"

    # When
    with pytest.raises(KeyError) as error:
        environment.get_pypi_url(envname)

    # Then the envname is mentioned in the error message
    errormsg = str(error.value)
    assert "fake_env" in errormsg
