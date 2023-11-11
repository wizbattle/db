from katsuba import op


def make_bind_serializer(type_list: op.TypeList) -> op.Serializer:
    """Creates a new BINd deserializer given a list of types."""

    # Apply the fixed base configuration used by all game files.
    opts = op.SerializerOptions()
    opts.flags |= op.STATEFUL_FLAGS
    opts.shallow = False
    opts.skip_unknown_types = True

    return op.Serializer(opts, type_list)
