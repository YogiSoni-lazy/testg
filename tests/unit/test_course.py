from labs import course


def test__get_package_version__no_dependencies_found():
    """
    If get_package_version() can't find the installed version
    of the course library for the given sku, then it should return None
    """
    version = course.get_package_version("dev-null")

    assert version is None
