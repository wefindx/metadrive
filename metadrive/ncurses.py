import curses

# -----------------------------------
# | Adddress: ______________________ |
# -----------------------------------
# |                                  |
# |                                  |
# |                                  |
# ------------------------------------


class AddressWindow(object):
    def __init__(self, std_screen):
        self.window = std_screen
        self.pos_x, self.pos_y = 0, 0
        self.total_rows, self.total_cols = self.window.getmaxyx()

    def print_border(self):
        self.window.clear()
        for idx in range(1, self.total_rows - 1):
            self.window.addstr(idx, 0, '|')
            self.window.addstr(idx, int(self.total_cols/2) + 1, '|')
            self.window.addstr(idx, self.total_cols - 1, '|')

        self.window.addstr(0, 1, '-' * (self.total_cols - 2))
        self.window.addstr(self.total_rows - 1, 1, '-' * (self.total_cols - 2))
        self.window.refresh()

    def init_window(self, *args, **kwargs):
        pass

    def display(self, *args, **kwargs):
        pass


class MainWindow(object):
    def __init__(self, std_screen):
        try:
            self.screen = std_screen
            self.selected = 0
            curses.cbreak()
            curses.noecho()
            curses.curs_set(0)
            self.main = self.screen.subwin(0, 0)
            self.main.keypad(1)
            self.main.nodelay(1)
            self.cwin = AddressWindow(self.screen)
            self.cwin.print_border()

            self.raise_exception = True
        except Exception as e:
            print(str(e))
            raise Exception("Failed to initialize cursor")

    def update(self):
        self.lwin.display()
        self.rwin.display()

    def listener(self):
        while True:
            key = self.main.getch()
            if key in [ord('q'), ord('Q')]:
                self.destroy()
                if self.raise_exception:
                    raise WXError('User exit')
                else:
                    break
            else:
                self.rwin.listener(key)

    def exit(self, raise_exception=True):
        # Push 'q' so the next getch() will return it
        self.raise_exception = raise_exception
        curses.ungetch(ord('q'))

    def destroy(self):
        # Don't not end the window again if it's already de-initialized
        if not self.isendwin:
            curses.initscr()
            curses.nocbreak()
            curses.echo()
            curses.endwin()

    @property
    def isendwin(self):
        return curses.isendwin()
