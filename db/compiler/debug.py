import io
from typing import Optional

from .emitter import CodeEmitter, Label, Register


class DebugLabel(Label):
    def __init__(self, name: str, emitter: "DebugEmitter"):
        self.name = name
        self._emitter = emitter

    def bind(self):
        self._emitter._write(f"{self.name}:")


class DebugEmitter(CodeEmitter):
    """A code emitter which produces human-readable opcodes for debugging."""

    def __init__(self):
        super().__init__()

        self.instruction_count = 0
        self.label_count = 0
        self.buf = io.StringIO()

    def _write(self, opcode: str):
        self.buf.write(f"{self.instruction_count:>2}: ")
        self.buf.write(opcode)
        self.buf.write("\n")

        self.instruction_count += 1

    def get_value(self) -> str:
        return self.buf.getvalue()

    def _label(self) -> DebugLabel:
        label = DebugLabel(f"L{self.label_count}", self)
        self.label_count += 1

        return label

    def label(self, *, bind: bool = True) -> Label:
        label = self._label()
        if bind:
            label.bind()

        return label

    def emit_mov(self, dest: Register, source: Register):
        self._write(f"MOV ${dest.name}, ${source.name}")

    def emit_load(self, reg: Register, value: int):
        self._write(f"LOAD ${reg.name}, {value}")

    def emit_add(self, dest: Register, source: Register):
        self._write(f"ADD ${dest.name}, ${source.name}")

    def emit_addi(self, dest: Register, value: int):
        self._write(f"ADDI ${dest.name}, {value}")

    def emit_percentage(self, dest: Register, source: Register):
        """Calculates a percentage of the destination register."""
        self._write(f"PCT ${dest.name}, ${source.name}")

    def emit_mul(self, dest: Register, source: Register):
        self._write(f"MUL ${dest.name}, ${source.name}")

    def emit_div(self, dest: Register, source: Register):
        self._write(f"DIV ${dest.name}, ${source.name}")

    def emit_and(self, dest: Register, source: Register):
        self._write(f"AND ${dest.name}, ${source.name}")

    def emit_or(self, dest: Register, source: Register):
        self._write(f"OR ${dest.name}, ${source.name}")

    def emit_xor(self, dest: Register, source: Register):
        self._write(f"XOR ${dest.name}, ${source.name}")

    def emit_bset(self, dest: Register, bit: int):
        self._write(f"BSET ${dest.name}, {bit}")

    def emit_bclr(self, dest: Register, bit: int):
        self._write(f"BCLR ${dest.name}, {bit}")

    def emit_jr(self, reg: Register):
        self._write(f"JR ${reg.name}")

    def emit_jmp(self, label: Optional[Label]) -> Optional[Label]:
        if label is None:
            label = self._label()
            self._write(f"JMP #{label.name}")
            return label
        else:
            self._write(f"JMP #{label.name}")
            return None

    def emit_jeq(self, a: Register, b: Register, label: Optional[Label]) -> Optional[Label]:
        if label is None:
            label = self._label()
            self._write(f"JEQ ${a.name}, ${b.name}, #{label.name}")
            return label
        else:
            self._write(f"JEQ ${a.name}, ${b.name}, #{label.name}")
            return None

    def emit_rng(self, count: int):
        self._write(f"RNG {count}")

    def emit_attack(self):
        self._write("ATTACK")

    def emit_heal(self):
        self._write("HEAL")

    def emit_drain(self):
        self._write("DRAIN")

    def emit_reshuffle(self):
        self._write("RESHUFFLE")
