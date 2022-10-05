from json import dump, load
from os.path import join
from typing import Optional

from wx import Frame, Button, EVT_BUTTON, StaticBoxSizer, VERTICAL, Image, Bitmap, BITMAP_TYPE_PNG, StaticText, \
    ALIGN_CENTER_HORIZONTAL, Size, Window, MenuBar, Menu, ID_SAVE, ID_OPEN, EVT_MENU, FileDialog, FD_SAVE, FD_OPEN, \
    ID_CANCEL, MessageDialog, OK, CENTER

from .State import State


class MainFrame(Frame):
    state: State

    def __init__(self, parent: Optional[Window], title: str, state: State):
        super().__init__(parent, title=title, size=(1920, 1080))

        menu_bar = MenuBar()
        file_menu = Menu()
        self.Bind(EVT_MENU, lambda _: self.save(), file_menu.Append(ID_SAVE, "&Save", "Save the game"))
        self.Bind(EVT_MENU, lambda _: self.open(), file_menu.Append(ID_OPEN, "&Open", "Open a save file"))
        menu_bar.Append(file_menu, "&File")

        self.energy_text = StaticText(self, label='0⚡', style=ALIGN_CENTER_HORIZONTAL)
        energy_button = Button(self, size=Size(200, 200))
        energy_button.SetBitmap(Bitmap(Image(join('img', 'icons', 'lightning.png'), BITMAP_TYPE_PNG)))
        energy_button.Bind(EVT_BUTTON, lambda _: self.add_energy(1))
        box_sizer_1 = StaticBoxSizer(orient=VERTICAL, parent=self, label="Energy")
        box_sizer_1.Add(self.energy_text)
        box_sizer_1.Add(energy_button)

        self.SetMenuBar(menu_bar)

        self.state = state
        self.state.register_energy_observer(lambda energy: self.energy_text.SetLabel(f'{energy}⚡'))
        self.SetSizerAndFit(box_sizer_1)
        self.Show()

    def add_energy(self, energy: int):
        self.state.energy += energy

    def save(self):
        with FileDialog(self, 'Choose file', wildcard='JSON File (*.json)|*.json', style=FD_SAVE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, 'w') as file:
                    dump(self.state.json_object(), file)
            except IOError:
                MessageDialog(self, 'I/O error', style=OK | CENTER)

    def open(self):
        with FileDialog(self, 'Choose file', wildcard='JSON File (*.json)|*.json', style=FD_OPEN) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, 'r') as file:
                    self.state.import_json_object(load(file))
            except IOError:
                MessageDialog(self, 'I/O error', style=OK | CENTER)
