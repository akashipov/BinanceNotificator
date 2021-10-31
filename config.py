import json
import os
import pathlib


def load_config():
    with open(
        os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json"),
        "r",
    ) as f:
        config = json.load(f)
    return config


def write_config(config):
    with open(
        os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json"),
        "w",
    ) as f:
        json.dump(config, f, indent=4, sort_keys=True)
