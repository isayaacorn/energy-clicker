from os.path import join
from json import dump, load

from wx import App, Frame, Button, EVT_BUTTON, BoxSizer, VERTICAL, Image, Bitmap, BITMAP_TYPE_PNG, StaticText, ALIGN_CENTER_HORIZONTAL, Size, Window, MenuBar, Menu, ID_SAVE, ID_OPEN, EVT_MENU, FileDialog, FD_SAVE, FD_OPEN, ID_CANCEL, MessageDialog, OK, CENTER

from .State import State

class MainFrame(Frame):
    state: State
    
    def __init__(self, parent: Window, title: str, state: State):
        super().__init__(parent, title = title, size = (1920, 1080))
        
        menuBar = MenuBar()
        fileMenu = Menu()
        self.Bind(EVT_MENU, lambda _: self.save(), fileMenu.Append(ID_SAVE, "&Save", "Save the game"))
        self.Bind(EVT_MENU, lambda _: self.open(), fileMenu.Append(ID_OPEN, "&Open", "Open a save file"))
        menuBar.Append(fileMenu, "&File")

        self.energy_text = StaticText(self, label='0⚡', style = ALIGN_CENTER_HORIZONTAL)
        energy_button = Button(self, size = Size(200, 200))
        energy_button.Bitmap = Bitmap(Image(join('img', 'bsicons', 'lightning-fill-160.png'), BITMAP_TYPE_PNG))
        energy_button.Bind(EVT_BUTTON, lambda _: self.add_energy(1))
        box_sizer_1 = BoxSizer(orient = VERTICAL)
        box_sizer_1.Add(self.energy_text)
        box_sizer_1.Add(energy_button)

        self.SetMenuBar(menuBar)

        self.state = state
        self.state.register_energy_observer(lambda energy: self.energy_text.SetLabel(f'{energy}⚡'))
        self.SetSizerAndFit(box_sizer_1)
        self.Show()
    
    def add_energy(self, energy: int):
        self.state.energy += energy
    
    def save(self):
        with FileDialog(self, 'Choose file', wildcard = 'JSON File (*.json)|*.json', style = FD_SAVE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, 'w') as file:
                    dump(self.state.jsonObject(), file)
            except IOError:
                MessageDialog(self, 'I/O error', style = OK | CENTER)
    
    def open(self):
        with FileDialog(self, 'Choose file', wildcard = 'JSON File (*.json)|*.json', style = FD_OPEN) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, 'r') as file:
                    self.state.importJsonObject(load(file))
            except IOError:
                MessageDialog(self, 'I/O error', style = OK | CENTER)
        