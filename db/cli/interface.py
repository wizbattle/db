from pathlib import Path

import click

from db import commands

from .config import Config


@click.group()
@click.pass_context
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose logging")
def cli(ctx: click.Context, verbose: bool):
    """Database management tool for wizbattle."""
    ctx.obj = Config(verbose)


@cli.group(chain=True)
@click.pass_obj
@click.argument(
    "root_wad",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.argument(
    "types_json",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def build(config: Config, root_wad: Path, types_json: Path):
    """
    Builds the database from files in the given Root.wad archive.

    The provided type list will be used for deserializing the required
    ObjectProperty state.

    The individual subcommands are responsible for parts of the workload
    and can be chained together in a single command invocation as needed.
    """

    config.load_root_archive(root_wad)
    config.load_types_json(types_json)


@build.command()
@click.pass_obj
def spells(config: Config):
    """Assembles spell data in the database."""
    commands.handle_spells(config)

@build.command()
@click.pass_obj
@click.argument("spell_name")
def show(config: Config, spell_name: str):
    """Shows code generation for a particular spell."""
    commands.handle_debug(config, spell_name.encode())
