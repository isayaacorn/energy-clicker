from os.path import join

from wx import App, Frame, Button, EVT_BUTTON, BoxSizer, VERTICAL, Image, Bitmap, BITMAP_TYPE_PNG, StaticText, ALIGN_CENTER_HORIZONTAL, Size, Window

from .State import State

class MainFrame(Frame):
    state: State
    
    def __init__(self, parent: Window, title: str, state: State):
        super().__init__(parent, title = title, size = (1920, 1080))

        self.state = state

        self.energy_text = StaticText(self, label='0⚡', style = ALIGN_CENTER_HORIZONTAL)
        energy_button = Button(self, size = Size(200, 200))
        energy_button.Bitmap = Bitmap(Image(join('img', 'bsicons', 'lightning-fill-160.png'), BITMAP_TYPE_PNG))
        energy_button.Bind(EVT_BUTTON, lambda _: self.add_energy(1))
        box_sizer_1 = BoxSizer(orient = VERTICAL)
        box_sizer_1.Add(self.energy_text)
        box_sizer_1.Add(energy_button)
        self.SetSizerAndFit(box_sizer_1)
        self.Show()
    
    def add_energy(self, energy: int):
        self.state.energy += energy
        self.energy_text.SetLabel(f'{self.state.energy}⚡')
        