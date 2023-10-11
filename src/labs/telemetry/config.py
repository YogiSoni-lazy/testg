from labs import pkgconfig


def is_enabled():
    """
    Is telemetry feature enabled?
    """
    return all().getboolean("enabled")


def get_api_endpoint():
    return all().get("api_endpoint")


def get_uploader():
    return all().get("uploader")


def all():
    """
    Get all telemetry package config values
    """
    cfg = pkgconfig.load()
    return cfg["rht.telemetry"]
