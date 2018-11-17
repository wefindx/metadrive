from boltons.iterutils import remap

def clean_em(items):

    def visit(path, key, value):
        if type(value) in [int, float]:
            if len(str(value)) > 7:
                return key, str(value)
        return key, value

    return remap(items, visit=visit)

