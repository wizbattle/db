from contextlib import contextmanager

from .emitter import Register


def count_trailing_zeros(value: int) -> int:
    """Counts trailing zero bits in a number."""
    return 0 if value == 0 else (value & -value).bit_length() - 1


def count_trailing_ones(value: int) -> int:
    """Counts trailing one bits in a number."""
    return count_trailing_zeros(~value)


class RegisterAllocator:
    """
    Guards access to a fixed number of available general-purpose
    registers in the VM.

    Acquiring permits to access registers can be done in one of two
    ways: either paired allocate/release calls, or for the duration
    of a context manager.

    When no more registers are available, an exception will be thrown.
    More often than not, this should be a red flag indicating either
    resource leaks or wasteful use of available resources.
    """

    def __init__(self, limit):
        self._mask = 0
        self.limit = limit

    def allocate(self) -> Register:
        """
        Allocates an available register and returns its index.
        
        Must be released manually.
        """

        reg = count_trailing_ones(self._mask)
        if reg >= self.limit:
            raise RuntimeError("register allocation limit exceeded")

        self._mask |= (1 << reg)
        return Register(Register.REG0.value + reg)

    def release(self, reg: Register):
        """Releases a previously allocated register."""
        self._mask &= ~(1 << (reg.value - Register.REG0.value))

    @contextmanager
    def borrow(self) -> Register:
        """
        Borrows an unoccupied register for the context manager's lifetime.

        On exit, the register will be released again and can be reallocated
        on future allocate calls.
        """

        reg = self.allocate()
        try:
            yield reg
        finally:
            self.release(reg)
