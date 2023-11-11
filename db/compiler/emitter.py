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

    #: General Purpose Register 0
    REG0 = 0x16
    #: General Purpose Register 1
    REG1 = 0x17
    #: General Purpose Register 2
    REG2 = 0x18
    #: General Purpose Register 3
    REG3 = 0x19
    #: General Purpose Register 4
    REG4 = 0x1A
    #: General Purpose Register 5
    REG5 = 0x1B
    #: General Purpose Register 6
    REG6 = 0x1C
    #: General Purpose Register 7
    REG7 = 0x1D
    #: General Purpose Register 8
    REG8 = 0x1E
    #: General Purpose Register 9
    REG9 = 0x1F


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

    def emit_put(self, reg: Register, value: int):
        """Puts an value into a register."""
        raise NotImplementedError()

    def emit_add(self, dest: Register, source: Register):
        """Adds two register values together."""
        raise NotImplementedError()

    def emit_mul(self, dest: Register, source: Register):
        """Multiplies two register values."""
        raise NotImplementedError()

    def emit_shr(self, dest: Register, source: Register):
        """Shifts the destination register to the right by source register."""
        raise NotImplementedError()

    def emit_and(self, dest: Register, source: Register):
        """Bitwise ANDs two operands together."""
        raise NotImplementedError()

    def emit_or(self, dest: Register, source: Register):
        """Bitwise ORs two operands together."""
        raise NotImplementedError()

    def emit_not(self, dest: Register, source: Register):
        """Calculates the bitwise complement of an operand."""
        raise NotImplementedError()

    def emit_push(self, source: Register, stack: Stack):
        """Pushes a register value onto the selected stack."""
        raise NotImplementedError()

    def emit_pop(self, stack: Stack):
        """Removes an element from the selected stack."""
        raise NotImplementedError()

    def emit_jmp(self, off: int):
        """Unconditionally jumps over off instructions."""
        raise NotImplementedError()

    def emit_jeq(self, a: Register, b: Register, off: int):
        """Compares two registers and jumps over off instructions if equal."""
        raise NotImplementedError()

    def emit_rng(self, count: int):
        """Randomly executes only one out of the next count instructions."""
        raise NotImplementedError()

    def emit_attack(self):
        """Attacks with the current configuration of special-purpose registers."""
        raise NotImplementedError()

    def emit_heal(self):
        """Heals with the current configuration of special-purpose registers."""
        raise NotImplementedError()

    def emit_reshuffle(self):
        """Reshuffles the spell deck and restores a player's hand."""
        raise NotImplementedError()
