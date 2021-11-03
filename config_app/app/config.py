import json
import os
import pathlib


def load_config():
    with open(
        os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json"),
        "r",
    ) as f:
        lines = f.read().split("\n")
        with open(
            os.path.join(
                pathlib.Path(__file__).parent.resolve(),
                "config_without_comments.json",
            ),
            "w",
        ) as g:
            for line in lines:
                print_line = (
                    line[: line.find("#")] if line.find("#") != -1 else line
                )
                g.write(print_line + "\n")
        with open(
            os.path.join(
                pathlib.Path(__file__).parent.resolve(),
                "config_without_comments.json",
            ),
            "r",
        ) as g:
            config = json.load(g)
    return config


def write_config(config):
    with open(
        os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json"),
        "w",
    ) as f:
        json.dump(config, f, indent=4, sort_keys=True)
