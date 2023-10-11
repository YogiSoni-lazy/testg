import pkg_resources


def get_package_name(sku: str):
    """
    Return the course package name of a given sku
    """
    return "rht-labs-" + sku.lower()


def get_package_version(sku: str):
    """
    Return the installed version of a course-specific package,
    given a sku
    """
    package_name = get_package_name(sku)

    try:
        dependencies = pkg_resources.require(package_name)
    except pkg_resources.ResolutionError:
        return None

    if not dependencies:
        return None

    return dependencies[0].version
