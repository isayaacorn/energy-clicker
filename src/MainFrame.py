from decimal import Decimal
from json import dump, load
from os.path import join
from typing import Optional

from wx import Frame, Button, EVT_BUTTON, BoxSizer, StaticBoxSizer, VERTICAL, Image, Bitmap, BITMAP_TYPE_PNG, \
    StaticText, \
    ALIGN_CENTER_HORIZONTAL, Window, MenuBar, Menu, ID_SAVE, ID_OPEN, EVT_MENU, FileDialog, FD_SAVE, FD_OPEN, \
    ID_CANCEL, MessageDialog, OK, CENTER, Timer, EVT_TIMER

from .State import State


class MainFrame(Frame):
    state: State

    def __init__(self, parent: Optional[Window], title: str, state: State):
        super().__init__(parent, title=title, size=(1920, 1080))

        menu_bar = MenuBar()
        file_menu = Menu()
        self.Bind(EVT_MENU, lambda _: self.save(), file_menu.Append(ID_SAVE, '&Save', 'Save the game'))
        self.Bind(EVT_MENU, lambda _: self.open(), file_menu.Append(ID_OPEN, '&Open', 'Open a save file'))
        menu_bar.Append(file_menu, '&File')

        self.SetMenuBar(menu_bar)

        energy_text = StaticText(self, label='0⚡', style=ALIGN_CENTER_HORIZONTAL)
        eps_text = StaticText(self, label='0⚡/sec')
        energy_button = Button(self)
        energy_button.SetBitmap(Bitmap(Image(join('img', 'icons', 'lightning.png'), BITMAP_TYPE_PNG)))
        energy_button.Bind(EVT_BUTTON, lambda _: self.add_energy(Decimal(1)))
        click_sizer = StaticBoxSizer(orient=VERTICAL, parent=self, label='Energy')
        click_sizer.Add(energy_text)
        click_sizer.Add(eps_text)
        click_sizer.Add(energy_button)

        campfire_button = Button(self)
        campfire_button.SetBitmap(Bitmap(Image(join('img', 'icons', 'campfire.png'), BITMAP_TYPE_PNG)))
        campfire_button.Bind(EVT_BUTTON, lambda _: self.purchase_building('campfire', Decimal(0.2), Decimal(15)))
        self.campfire_text = StaticText(self, label='15.00⚡')
        campfire_sizer = StaticBoxSizer(orient=VERTICAL, parent=self, label='Campfire')
        campfire_sizer.Add(campfire_button)
        campfire_sizer.Add(self.campfire_text)

        building_sizer = StaticBoxSizer(orient=VERTICAL, parent=self, label='Buildings')
        building_sizer.Add(campfire_sizer)

        sizer = BoxSizer(orient=VERTICAL)
        sizer.Add(click_sizer)
        sizer.Add(building_sizer)

        self.state = state
        self.state.register_energy_observer(
            lambda energy: energy_text.SetLabel(f'{round(energy, 2).normalize().to_eng_string()}⚡'))
        self.state.register_energy_per_second_observer(
            lambda eps: eps_text.SetLabel(f'{round(eps, 1).normalize().to_eng_string()}⚡/sec'))
        self.SetSizerAndFit(sizer)
        self.Show()

        self.timer = Timer(self)
        self.Bind(EVT_TIMER, lambda _: self.state.tick(), self.timer)
        self.timer.Start(1000)

    def add_energy(self, energy: Decimal):
        self.state.energy += energy

    def purchase_building(self, building: str, eps: Decimal, price: Decimal):
        new_price = round(price * Decimal(1.05) ** self.state.buildings[building], 2)
        if self.state.energy >= new_price:
            self.state.energy -= new_price
            self.state.energy_per_second += eps
            self.state.buildings[building] += 1
            self.campfire_text.SetLabel(f'{round(new_price * Decimal(1.05), 2)}⚡')

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
