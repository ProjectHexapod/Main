


class CommandWrapper:
    """This is a thin wrapper to make it easier to access fields in the robotControl proto.
    """
    def __init__(self, proto):
        self.proto = proto
        self.raw_key_values = {}
        for raw in proto.raw_command:
            if raw.HasField('index'):
                self.raw_key_values[raw.index] = raw.value
            if raw.HasField('name'):
                self.raw_key_values[raw.name] = raw.value
        self.fields = {k: v for k,v in proto.ListFields()}

    def __getitem__(self, name):
        if name in self.raw_key_values:
            return self.raw_key_values[name]
        elif name in self.fields:
            return self.fields[name]

