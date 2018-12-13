import code

def repl():
    help = "MetaDrive a new way to driver world around you..."
    code.interact(
        banner="Welcome to MetaDrive! Type 'help' for more info.",
        local=locals(),
        exitmsg="See you~"
    )

if __name__ == "__main__":
    repl()
