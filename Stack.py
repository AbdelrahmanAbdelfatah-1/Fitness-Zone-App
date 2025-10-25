class Stack :

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, win) :
        if self.items :
            self.items[-1].withdraw()
        self.items.append(win)
        win.deiconify()

    def pop(self) :

        if len(self.items) <= 1 :
            return None

        current_win = self.items.pop()
        current_win.destroy()
        previous_win = self.items[-1]
        previous_win.deiconify()
        previous_win.state("zoomed")
        return previous_win