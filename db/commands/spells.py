import click

from db.cli import Config
from db.compiler import DebugEmitter, SpellCompiler
from db.op import make_bind_serializer


def handle(config: Config):
    """Implementation of the `build spells` CLI command."""

    serializer = make_bind_serializer(config.types)
    for file in config.archive.iter_glob("Spells/**/*.xml"):
        obj = config.archive.deserialize(file, serializer)
        click.echo(obj["m_name"])


def debug(config: Config, name: bytes):
    """Implementation of the `build show` CLI command."""

    serializer = make_bind_serializer(config.types)
    for file in config.archive.iter_glob("Spells/**/*.xml"):
        obj = config.archive.deserialize(file, serializer)
        if obj["m_name"] == name:
            print(file)
            emitter = DebugEmitter()

            compiler = SpellCompiler(emitter)
            compiler.compile(obj)

            click.echo(emitter.get_value())
            return

    raise click.UsageError(f"no spell named '{name.decode()}' found in archive")
