from katsuba.op import LazyObject

from db.op import EffectVisitor

from .emitter import CodeEmitter, Register
from .regalloc import RegisterAllocator


class SpellCompiler(EffectVisitor):
    """
    The compiler that turns the effects of spells into a portable bytecode
    representation for the wizbattle VM.

    A reference to an emitter object is managed and modified internally,
    giving the caller control over the implementation and how to consume
    the output.
    """

    def __init__(self, emitter: CodeEmitter, register_limit: int = 10):
        super().__init__()

        self.emitter = emitter
        self.regalloc = RegisterAllocator(register_limit)

    def compile(self, spell: LazyObject):
        """Compiles a spell and emits code to the emitter object."""
        self.visit(spell)

    def steal_health(self):
        # Attack with the current configuration.
        self.emitter.emit_attack()

        # Heal half of the base damage back.
        with self.regalloc.borrow() as tmp:
            self.emitter.emit_put(tmp, 1)
            self.emitter.emit_shr(Register.ARG, tmp)
            self.emitter.emit_heal()


    def visit_spell_effect(self, obj: LazyObject):
        match obj["m_effectType"]:
            case 5:
                self.steal_health()

            case _:
                raise NotImplementedError()
