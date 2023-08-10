import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import sys
import json


sys.path.append("/home/marcesch/privat/Selina/Notenuebersicht/backend/")
from gui_overview_all_classes import App_OverviewClasses




def startup_process():
    print("Somewhere here I could start initializing all classes, .. loaded from disk => use that in memory (presumably reasonably small amount of data) and load from disk only once ")



def load_config():
    """
    Loads config info from files, most notably the theme
    :return:
    """

    theme = "azure"
    mode = "light"
    return theme, mode


if __name__ == '__main__':
    theme, mode = load_config()
    startup_process()
    app = App_OverviewClasses(theme, mode)
    # app = App(input("Theme (azure / park / sun-valley): ").lower(), input("dark / light: ").lower())