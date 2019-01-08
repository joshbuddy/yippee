from contextlib import contextmanager


@contextmanager
def group(name):
    config._config_state["previous_group"] = config._config_state["current_group"]
    config._config_state["current_group"] = []
    config._config_state["groups"][name] = config._config_state["current_group"]
    yield
    config._config_state["current_group"] = config._config_state["previous_group"]


def pip(name, version=None):
    if version:
        if (
            not version.startswith("=")
            and not version.startswith(">")
            and not version.startswith("!")
            and not version.startswith("~")
        ):
            version = "==" + version
        config._config_state["current_group"].append((name, version))
    else:
        config._config_state["current_group"].append((name,))
