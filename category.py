class Note:

    def __init__(self, text):
        self.text = text


class Category:

    def __init__(self, name):
        self.name = name
        self.notes = dict()
        self.nextid = 0

    def add_note(self, text):
        self.notes.update({self.nextid: text})
        self.nextid += 1

    def del_note(self, key):
        key = int(key)
        notes = dict()
        for notekey in self.notes:
            if notekey > key:
                notes.update({notekey-1: self.notes[notekey]})
            elif notekey == key:
                self.nextid -= 1
                continue
            else:
                notes.update({notekey: self.notes[notekey]})
        self.notes = notes

    def get_text(self):
        msg = '*' + self.name + '*\n'
        for note in self.notes:
            msg += str(note) + '. ' + self.notes[note] + '\n'
        return msg
