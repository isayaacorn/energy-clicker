from decimal import Decimal
from json import dump, load
from os.path import join
from typing import Optional

from wx import Frame, Button, EVT_BUTTON, BoxSizer, StaticBoxSizer, VERTICAL, Image, Bitmap, BITMAP_TYPE_PNG, \
    StaticText, \
    ALIGN_CENTER_HORIZONTAL, Window, MenuBar, Menu, ID_SAVE, ID_OPEN, EVT_MENU, FileDialog, FD_SAVE, FD_OPEN, \
    ID_CANCEL, MessageDialog, OK, CENTER, Timer, EVT_TIMER, ScrolledWindow

from .Building import BUILDINGS, Building
from .State import State
from .assets import get_asset


class MainFrame(Frame):
    __state: State
    __timer: Timer
    __building_texts: dict[str, StaticText]

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
        energy_button.SetBitmap(get_asset('lightning'))
        energy_button.Bind(EVT_BUTTON, lambda _: self.add_energy(Decimal(1)))
        click_sizer = StaticBoxSizer(orient=VERTICAL, parent=self, label='Energy')
        click_sizer.Add(energy_text)
        click_sizer.Add(eps_text)
        click_sizer.Add(energy_button)

        self.__building_texts = {}

        building_sizer = StaticBoxSizer(orient=VERTICAL, parent=self, label='Buildings')

        for building in BUILDINGS:
            button = Button(self)
            button.building = building
            button.SetBitmap(get_asset(building.id))
            button.Bind(
                EVT_BUTTON, lambda event: self.purchase_building(event.GetEventObject().building))
            self.__building_texts[building.id] = StaticText(self, label=f'{building.name}: {building.price:.2f}⚡')
            sizer = StaticBoxSizer(orient=VERTICAL, parent=self, label=building.name)
            sizer.Add(button)
            sizer.Add(self.__building_texts[building.id])
            building_sizer.Add(sizer)

        sizer = BoxSizer(orient=VERTICAL)
        sizer.Add(click_sizer)
        sizer.Add(building_sizer)

        self.__state = state
        self.__state.register_energy_observer(
            lambda energy: energy_text.SetLabel(f'{round(energy, 2).normalize().to_eng_string()}⚡'))
        self.__state.register_energy_per_second_observer(
            lambda eps: eps_text.SetLabel(f'{round(eps, 1).normalize().to_eng_string()}⚡/sec'))
        self.__state.register_buildings_observer(lambda _: self.update_buildings())
        self.SetSizerAndFit(sizer)
        self.Show()

        self.__timer = Timer(self)
        self.Bind(EVT_TIMER, lambda _: self.__state.tick(), self.__timer)
        self.__timer.Start(1000)

    def add_energy(self, energy: Decimal):
        self.__state.energy += energy

    def purchase_building(self, building: Building):
        new_price = round(building.price * Decimal(1.05) ** self.__state.buildings[building.id], 2)
        if self.__state.energy >= new_price:
            self.__state.energy -= new_price
            self.__state.energy_per_second += building.energy_per_second
            self.__state.add_building(building)
            self.__building_texts[building.id].SetLabel(f'{building.name}: {new_price * Decimal(1.05):.2f}⚡')

    def update_buildings(self):
        for building in BUILDINGS:
            self.__building_texts[building.id].SetLabel(
                f'{building.name}: {round(building.price * Decimal(1.05) ** self.__state.buildings[building.id], 2)}')

    def save(self):
        with FileDialog(self, 'Choose file', wildcard='JSON File (*.json)|*.json', style=FD_SAVE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, 'w') as file:
                    dump(self.__state.json_object(), file)
            except IOError:
                MessageDialog(self, 'I/O error', style=OK | CENTER)

    def open(self):
        with FileDialog(self, 'Choose file', wildcard='JSON File (*.json)|*.json', style=FD_OPEN) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, 'r') as file:
                    self.__state.import_json_object(load(file))
            except IOError:
                MessageDialog(self, 'I/O error', style=OK | CENTER)
