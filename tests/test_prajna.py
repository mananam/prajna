# -*- coding: utf-8 -*-
"""Tests for the main module."""

import click
import logging
import os
import pytest
import prajna.main

from click.testing import CliRunner


@pytest.fixture
def config(fs):
    user_config = os.path.join(click.get_app_dir("prajna"), "config.ini")
    fs.CreateFile(user_config)
    config = """
[dict]
dict1=/tmp/prajna_test/dict1"""
    with open(user_config, "w") as f:
        f.write(config)
    return {}


def test_prajna_cli_debug_option_enables_verbose_log(caplog):
    with caplog.at_level(logging.INFO):
        result = _run_command(prajna.main.cli, ["--debug", "info"])

    debug = ("prajna", logging.INFO, "Verbose messages are enabled.")
    assert result.exception is None
    assert result.exit_code is 0
    assert debug in caplog.record_tuples


def test_prajna_should_read_per_user_config(fs, config):
    result = _run_command(prajna.main.cli, ["info"], config)

    assert config['dict'] == {'dict1': "/tmp/prajna_test/dict1"}
    assert result.exception is None
    assert result.exit_code is 0


def _run_command(command, args=[], config={}):
    return _run_command_with_stdin(command, args, config)


def _run_command_with_stdin(command, args, config):
    runner = CliRunner()
    result = runner.invoke(command, args=args, obj=config)

    print(result.output)
    print(result.exc_info)

    return result
