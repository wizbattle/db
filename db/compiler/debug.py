import io

from .emitter import CodeEmitter, Register, Stack


class DebugEmitter(CodeEmitter):
    """A code emitter which produces human-readable opcodes for debugging."""

    def __init__(self):
        self.instruction_count = 0
        self.buf = io.StringIO()

    def _write(self, opcode: str):
        self.buf.write(f"{self.instruction_count:>2}: ")
        self.buf.write(opcode)
        self.buf.write("\n")

        self.instruction_count += 1

    def get_value(self) -> str:
        return self.buf.getvalue()

    def emit_put(self, operand: int):
        self._write(f"PUT {operand}")

    def emit_add(self):
        self._write("ADD")

    def emit_mul(self):
        self._write("MUL")

    def emit_and(self):
        self._write("AND")

    def emit_or(self):
        self._write("OR")

    def emit_not(self):
        self._write("NOT")

    def emit_push(self, stack: Stack):
        self._write(f"PUSH {stack.name}")

    def emit_pop(self, stack: Stack):
        self._write(f"POP {stack.name}")

    def emit_load(self, reg: Register):
        self._write(f"LOAD {reg.name}")

    def emit_store(self, reg: Register):
        self._write(f"STORE {reg.name}")

    def emit_jmp(self, off: int):
        self._write(f"JMP {off}")

    def emit_jeq(self, off: int):
        self._write(f"JEQ {off}")

    def emit_rng(self, count: int):
        self._write(f"RNG {count}")

    def emit_reshuffle(self):
        self._write("RESHUFFLE")
