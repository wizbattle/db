from enum import IntEnum


class Register(IntEnum):
    """Registers in the VM."""

    #: General Purpose Register 0
    REG0 = 0x00
    #: General Purpose Register 1
    REG1 = 0x01
    #: General Purpose Register 2
    REG2 = 0x02
    #: General Purpose Register 3
    REG3 = 0x03

    #: Zero Register.
    ZERO = 0x04
    #: Argument to spell
    ARG = 0x05
    #: Target of spell
    TGT = 0x06
    #: Additional Armor Piercing
    AP = 0x07


class CodeEmitter:
    """
    Interface for code emitter backends in the spell compiler.

    Implementors must treat all operands as 32-bit signed values.
    """

    def emit_mov(self, dest: Register, source: Register):
        """Moves a value from source to destination register."""
        raise NotImplementedError()

    def emit_load(self, dest: Register, value: int):
        """Loads a 32-bit constant from offset into destination register."""
        raise NotImplementedError()

    def emit_add(self, dest: Register, source: Register):
        """Adds two register values together."""
        raise NotImplementedError()

    def emit_addi(self, dest: Register, value: int):
        """Adds an immediate value to the destination register."""
        raise NotImplementedError()

    def emit_percentage(self, dest: Register, source: Register):
        """Calculates a percentage of the destination register."""
        raise NotImplementedError()

    def emit_mul(self, dest: Register, source: Register):
        """Multiplies two register values."""
        raise NotImplementedError()

    def emit_div(self, dest: Register, source: Register):
        """Divides destination by source register."""
        raise NotImplementedError()

    def emit_and(self, dest: Register, source: Register):
        """Bitwise ANDs two operands together."""
        raise NotImplementedError()

    def emit_or(self, dest: Register, source: Register):
        """Bitwise ORs two operands together."""
        raise NotImplementedError()

    def emit_xor(self, dest: Register, source: Register):
        """Bitwise XORs two operands together."""
        raise NotImplementedError()

    def emit_bset(self, dest: Register, bit: int):
        """Sets the given bit index in the destination register."""
        raise NotImplementedError()

    def emit_bclr(self, dest: Register, bit: int):
        """Clears the given bit index in the destination register."""
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

    def emit_drain(self):
        """Heals by the value in ARG without applying heal boosts to it."""
        raise NotImplementedError()

    def emit_reshuffle(self):
        """Reshuffles the spell deck and restores a player's hand."""
        raise NotImplementedError()
