_config_state = {}


def reset_state():
    global _config_state
    _config_state = {
        "groups": {},
        "current_group": None,
        "previous_group": None,
        "exclude": ["wheel", "distribute", "pip", "setuptools"],
    }
    _config_state["groups"]["_top_level_group"] = []
    _config_state["current_group"] = _config_state["groups"]["_top_level_group"]


class Config:
    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        reset_state()
        with open(self.path, "r") as fh:
            exec(fh.read())
        self.state = _config_state.copy()
