from db.cli import Config

from db.op import make_bind_deserializer


def handle(config: Config):
    """Implementation of the `build spells` CLI command."""

    serializer = make_bind_deserializer(config.types)
    for file in config.archive.iter_glob("Spells/**/*.xml"):
        obj = config.archive.deserialize(file, serializer)
        print(obj["m_name"])
