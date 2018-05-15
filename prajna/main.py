# -*- coding: utf-8 -*-
"""Command line for prajna."""
import click
import configparser
import logging
import os

logger = logging.getLogger("prajna")


@click.group()
@click.option("--debug", is_flag=True, help="Enable verbose messages.")
@click.pass_context
def cli(ctx, debug):
    """Prajna - tools for sanskrit books."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.info("Verbose messages are enabled.")

    user_config = os.path.join(click.get_app_dir("prajna"), "config.ini")
    if os.path.exists(user_config):
        parser = configparser.ConfigParser()
        with open(user_config, "r", encoding="utf-8") as f:
            parser.read_file(f)
            ctx.obj['dict'] = dict(parser.items("dict"))
    else:
        logger.debug("Skip user configuration. Didn't find '{}'."
                     .format(user_config))
    pass


@cli.command()
@click.pass_context
def info(ctx):
    """List properties of current configuration."""
    if 'dict' not in ctx.obj:
        return

    dicts = ctx.obj['dict']
    if len(dicts) > 0:
        click.echo("Available dictionaries:")
        for k, v in dicts.items():
            click.echo("{}: {}".format(k, v))


if __name__ == '__main__':
    cli(obj={})
