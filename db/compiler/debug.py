import io

from .emitter import CodeEmitter, Register, Stack


class DebugEmitter(CodeEmitter):
    """A code emitter which produces human-readable opcodes for debugging."""

    def __init__(self):
        super().__init__()

        self.instruction_count = 0
        self.buf = io.StringIO()

    def _write(self, opcode: str):
        self.buf.write(f"{self.instruction_count:>2}: ")
        self.buf.write(opcode)
        self.buf.write("\n")

        self.instruction_count += 1

    def get_value(self) -> str:
        return self.buf.getvalue()

    def emit_put(self, reg: Register, value: int):
        self._write(f"PUT ${reg.name}, {value}")

    def emit_add(self, dest: Register, source: Register):
        self._write(f"ADD ${dest.name}, ${source.name}")

    def emit_mul(self, dest: Register, source: Register):
        self._write(f"MUL ${dest.name}, ${source.name}")

    def emit_shr(self, dest: Register, source: Register):
        self._write(f"SHR ${dest.name}, ${source.name}")

    def emit_and(self, dest: Register, source: Register):
        self._write(f"AND ${dest.name}, ${source.name}")

    def emit_or(self, dest: Register, source: Register):
        self._write(f"OR ${dest.name}, ${source.name}")

    def emit_not(self, dest: Register, source: Register):
        self._write(f"NOT ${dest.name}, ${source.name}")

    def emit_push(self, source: Register, stack: Stack):
        self._write(f"PUSH {stack.name}, ${source.name}")

    def emit_pop(self, stack: Stack):
        self._write(f"POP {stack.name}")

    def emit_jmp(self, off: int):
        self._write(f"JMP {off}")

    def emit_jeq(self, a: Register, b: Register, off: int):
        self._write(f"JEQ ${a.name}, ${b.name}, {off}")

    def emit_rng(self, count: int):
        self._write(f"RNG {count}")

    def emit_attack(self):
        self._write("ATTACK")

    def emit_heal(self):
        self._write("HEAL")

    def emit_reshuffle(self):
        self._write("RESHUFFLE")
