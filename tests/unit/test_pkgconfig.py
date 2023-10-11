from labs import pkgconfig


def test__can_load_config_file():
    cfg = pkgconfig.load()
    assert "rht.telemetry" in cfg.sections()
