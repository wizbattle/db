from katsuba.op import LazyObject
from katsuba.utils import string_id

_TYPE_HASH_TO_VISITOR = {
    string_id("class SpellEffect"): "visit_spell_effect",
    string_id("class ShadowSpellEffect"): "visit_shadow_spell_effect",
    string_id("class CountBasedSpellEffect"): "visit_count_based_spell_effect",
    string_id("class RandomSpellEffect"): "visit_random_spell_effect",
    string_id("class RandomPerTargetSpellEffect"): "visit_random_per_target_spell_effect",
    string_id("class VariableSpellEffect"): "visit_variable_spell_effect",
    string_id("class ConditionalSpellEffect"): "visit_conditional_spell_effect",
    string_id("class EffectListSpellEffect"): "visit_effect_list_spell_effect",
    string_id("class DelaySpellEffect"): "visit_delay_spell_effect",
    string_id("class HangingConversionSpellEffect"): "visit_hanging_conversion_spell_effect",
}


class EffectVisitor:
    """
    Visitor interface for processing different types of effects.

    Subclasses should override the methods to implement custom behavior for
    the effect types they want to support.

    The visit method serves as an entrypoint to processing a spell's effects.
    Users should not call any of the visit_* methods manually.
    """

    def visit(self, spell: LazyObject):
        """
        Visits a SpellTemplate object by processing all its effects on this
        visitor instance.
        """

        for effect in spell["m_effects"]:
            fn = getattr(self, _TYPE_HASH_TO_VISITOR[effect.type_hash])
            fn(effect)

    def visit_spell_effect(self, obj: LazyObject):
        """Visits a `class SpellEffect` object."""
        raise NotImplementedError()

    def visit_shadow_spell_effect(self, obj: LazyObject):
        """Visits a `class ShadowSpellEffect` object."""
        raise NotImplementedError()

    def visit_count_based_spell_effect(self, obj: LazyObject):
        """Visits a `class CountBasedSpellEffect` object."""
        raise NotImplementedError()

    def visit_random_spell_effect(self, obj: LazyObject):
        """Visits a `class RandomSpellEffect` object."""
        raise NotImplementedError()

    def visit_random_per_target_spell_effect(self, obj: LazyObject):
        """Visits a `class RandomPerTargetSpellEffect` object."""
        raise NotImplementedError()

    def visit_variable_spell_effect(self, obj: LazyObject):
        """Visits a `class VariableSpellEffect` object."""
        raise NotImplementedError()

    def visit_conditional_spell_effect(self, obj: LazyObject):
        """Visits a `class ConditionalSpellEffect` object."""
        raise NotImplementedError()

    def visit_effect_list_spell_effect(self, obj: LazyObject):
        """Visits a `class EffectListSpellEffect` object."""
        raise NotImplementedError()

    def visit_delay_spell_effect(self, obj: LazyObject):
        """Visits a `class DelaySpellEffect` object."""
        raise NotImplementedError()

    def visit_hanging_conversion_spell_effect(self, obj: LazyObject):
        """Visits a `class HangingConversionSpellEffect` object."""
        raise NotImplementedError()
