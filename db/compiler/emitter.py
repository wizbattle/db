from enum import IntEnum


class Register(IntEnum):
    """Special-purpose registers in the VM."""

    #: Argument to spell
    ARG = 0x00
    #: Target of spell
    TGT = 0x01
    #: Incoming Damage Multiplier
    IDM = 0x02
    #: Outgoing Damage Multiplier
    ODM = 0x03
    #: Outgoing Damage Flat
    ODF = 0x04
    #: Incoming Damage Cap
    IDC = 0x05
    #: Incoming Heal Multiplier
    IHM = 0x06
    #: Outgoing Heal Multiplier
    OHM = 0x07
    #: Outgoing Heal Flat
    OHF = 0x08
    #: Incoming Heal Cap
    IHC = 0x09
    #: Outgoing Armor Piercing
    OAP = 0x0A


class Stack(IntEnum):
    """VM stacks to operate on."""

    #: Stack for a player's charms.
    CHARMS = 0x00
    #: Stack for a player's wards.
    WARDS = 0x01


class CodeEmitter:
    """
    Interface for code emitter backends in the spell compiler.

    Implementors must treat all operands as 32-bit signed values.
    """

    def emit_put(self, operand: int):
        """Puts an value on the operand stack."""
        raise NotImplementedError()

    def emit_add(self):
        """Adds two operands together."""
        raise NotImplementedError()

    def emit_mul(self):
        """Multiplies two operands and leaves the result on the stack."""
        raise NotImplementedError()

    def emit_and(self):
        """Bitwise ANDs two operands together."""
        raise NotImplementedError()

    def emit_or(self):
        """Bitwise ORs two operands together."""
        raise NotImplementedError()

    def emit_not(self):
        """Calculates the bitwise complement of an operand."""
        raise NotImplementedError()

    def emit_push(self, stack: Stack):
        """Pushes an operand onto the selected stack."""
        raise NotImplementedError()

    def emit_pop(self, stack: Stack):
        """Removes an element from the selected stack."""
        raise NotImplementedError()

    def emit_load(self, reg: Register):
        """Loads a value from register to stack."""
        raise NotImplementedError()

    def emit_store(self, reg: Register):
        """Stores an operand in the selected register."""
        raise NotImplementedError()

    def emit_jmp(self, off: int):
        """Unconditionally jumps over off instructions."""
        raise NotImplementedError()

    def emit_jeq(self, off: int):
        """Compares two operands and jumps over off instructions if equal."""
        raise NotImplementedError()

    def emit_rng(self, count: int):
        """Randomly executes only one out of the next count instructions."""
        raise NotImplementedError()

    def emit_reshuffle(self):
        """Reshuffles the spell deck and restores a player's hand."""
        raise NotImplementedError()
