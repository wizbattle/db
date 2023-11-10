from pathlib import Path

from katsuba import wad
from katsuba.op import TypeList


class Config:
    """
    Maintains the configuration state that was supplied to the root command.

    This object is passed around with the `@click.pass_obj` decorator and
    makes configuration accessible to subcommands on demand.
    """

    def __init__(self, verbose: bool):
        self.verbose = verbose

        self.archive = None
        self.types = None

    def load_root_archive(self, path: Path):
        """Opens and maps a KIWAD archive file into memory."""
        self.archive = wad.Archive.mmap(path, True)

    def load_types_json(self, path: Path):
        """Opens and deserializes a type list in JSON format."""
        self.types = TypeList.open(path)
