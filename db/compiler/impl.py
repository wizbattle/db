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

    def __init__(self, emitter: CodeEmitter, register_limit: int = 4):
        super().__init__()

        self.emitter = emitter
        self.regalloc = RegisterAllocator(register_limit)

        self._effect_handlers = {
            5: self.steal_health,
        }

    def compile(self, spell: LazyObject):
        """Compiles a spell and emits code to the emitter object."""
        self.visit(spell)

    def emit_prologue(self, effect: LazyObject):
        arg = effect["m_effectParam"]
        ap = effect["m_armorPiercingParam"]

        if arg != 0:
            self.emitter.emit_load(Register.ARG, arg)
        if ap != 0:
            self.emitter.emit_load(Register.AP, ap)

    def apply_heal_modifier(self, effect: LazyObject):
        modifier = int(effect["m_healModifier"] * 100)

        with self.regalloc.borrow() as tmp:
            self.emitter.emit_load(tmp, modifier)
            self.emitter.emit_percentage(Register.ARG, tmp)

    def attack(self, *, no_crit = False):
        if no_crit:
            self.emitter.emit_bset(Register.TGT, 6)
        self.emitter.emit_attack()

    def heal(self, effect: LazyObject):
        self.apply_heal_modifier(effect)
        self.emitter.emit_heal()

    def drain(self, effect: LazyObject):
        self.apply_heal_modifier(effect)
        self.emitter.emit_drain()

    def steal_health(self, effect: LazyObject):
        self.attack()
        self.drain(effect)

    def visit_spell_effect(self, obj: LazyObject):
        effect_type = obj["m_effectType"]
        if handler := self._effect_handlers.get(effect_type):
            self.emit_prologue(obj)
            handler(obj)
        else:
            raise NotImplementedError(f"encountered unsupported effect type '{effect_type}'")
