import wpf

from System.Windows import Window,MessageBox

class LoadingWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'LoadingWindow.xaml')
