import yaml
import inspect

def get_actions(cls):
    '''
    Convenience function to create summaries of actions.
    '''
    actions = {}

    for k, v in cls.__dict__.items():
        if not k.startswith('__'):
            sig = inspect.signature(v)
            actions[k] = \
                '<'+', '.join([
                p + str(sig.parameters[p].annotation.__name__ != '_empty' and ': '+sig.parameters[p].annotation.__name__ or '')
                for p in sig.parameters
                if sig.parameters[p].name != 'self'
            ])+'>'

            if v.__doc__:
                actions[k] += ' - ' + v.__doc__.strip()

    return actions

def print_actions(cls):
    actions = get_actions(cls)

    string = yaml.dump({'_:actions': actions}, default_flow_style=False)

    string = string.replace('_:actions:', "\'_:actions\':")

    print(string, end='')
