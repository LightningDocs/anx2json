class Knackly_Writer:
    def __init__(self):
        pass

    def remove_none_values(self, dictionary: dict) -> dict:
        new_dict = {}
        for key, value in list(dictionary.items()):
            if isinstance(value, dict):
                new_dict[key] = self.remove_none_values(value)
            elif value is not None:
                new_dict[key] = value

        return new_dict
