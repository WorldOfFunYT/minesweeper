class Command:
    def __init__(self, name: str, parameters: list, description: str) -> None:
        self.name = name
        self.parameters = parameters
        self.description = description
        self.usage = self.name
        for parameter in self.parameters:
            self.usage += f' {parameter}'
    def __str__(self):
        finalString = self.name
        for parameter in self.parameters:
            finalString += f' {parameter}'
        finalString += f'\n{self.description}'
        return finalString


class Parameter:
    def __init__(self, name: str, required: bool) -> None:
        self.name = name
        self.required = required
    def __str__(self):
        if self.required:
            return f'<{self.name}>'
        else:
            return f'[{self.name}]'