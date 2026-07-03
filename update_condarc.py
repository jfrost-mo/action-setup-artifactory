#!/usr/bin/env python3
import argparse
import yaml

ARTIFACTORY_URL = "https://metoffice.jfrog.io/metoffice/api/conda"

DEFAULTS_CHANNELS = ["conda-main", "conda-free", "conda-r", "conda-msys2", "defaults"]


def remove_defaults(condarc: dict) -> None:
    """Remove any Anaconda default channels."""
    if "channels" in condarc:
        condarc["channels"] = list(
            filter(
                lambda channel: channel not in DEFAULTS_CHANNELS, condarc["channels"]
            )
        )


def add_conda_forge(condarc: dict) -> None:
    """Add the conda-forge channel and strict channel priority."""
    current_channels = condarc.get("channels", [])
    if "conda-forge" not in current_channels:
        print("[INFO] Adding conda-forge channel")
        condarc["channels"] = ["conda-forge"] + current_channels
    print("[INFO] Setting channel_priority to strict")
    condarc["channel_priority"] = "strict"


def add_artifactory_alias(condarc: dict) -> None:
    """Add the Artifactory channel alias."""
    if "channel_alias" in condarc:
        print(f"[WARN] Overriding previous channel_alias: {condarc['channel_alias']}")
    condarc["channel_alias"] = ARTIFACTORY_URL


if __name__ == "__main__":
    """ Entry point from command line. """
    parser = argparse.ArgumentParser(description="Update condarc file")
    parser.add_argument("condarc_file", help="Path to the condarc file")
    parser.add_argument(
        "--setup-conda-forge",
        action="store_true",
        default=False,
        help="Add conda-forge channel and remove defaults",
    )
    args = parser.parse_args()

    condarc_file = args.condarc_file
    setup_conda_forge = args.setup_conda_forge

    try:
        with open(condarc_file, "r", encoding="utf-8") as fd:
            condarc = yaml.safe_load(fd) or {}
    except FileNotFoundError:
        condarc = {}

    if not isinstance(condarc, dict):
        raise ValueError(
            f"Expected YAML mapping (dict) in {condarc_file}, got {type(condarc).__name__}"
        )

    # update the file
    add_artifactory_alias(condarc)
    if setup_conda_forge:
        remove_defaults(condarc)
        add_conda_forge(condarc)

    # write out:
    with open(condarc_file, "w") as fd:
        yaml.safe_dump(condarc, fd)
