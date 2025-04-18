class AnyType:
    def __eq__(self, _):
        return True

    def __instancecheck__(self, _):
        return True

    def __call__(self, value: any) -> any:
        return value
