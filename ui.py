from typing import Callable, Dict, List, Tuple

import os, sys
import webbrowser

import tkinter
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

import adofaiParser

PosType = Dict[str, int]
ElementType = Tuple[tkinter.Widget, PosType]
LabelType = Tuple[tkinter.Label, PosType]

def Pos(x: int = 0, y: int = 0, width: int = 0, height: int = 0, anchor: str = '') -> PosType:
    pos: PosType = {}

    if x != 0: pos['x'] = x
    if y != 0: pos['y'] = y
    if width != 0: pos['width'] = width
    if height != 0: pos['height'] = height
    if anchor != '': pos['anchor'] = anchor

    return pos

def Font(family: str, size: int) -> tkinter.font.Font:
    return tkinter.font.Font(family=family, size=size)

class UI:
    def __init__(self):
        self.Elements: List[ElementType] = []
        self.Labels: List[LabelType] = []
        self.adofaiFileName: str = ''

        self.BuildWindow()
        self.InitValues()
        self.BuildElements()
        self.PlaceElements()

    def BuildWindow(self):
        self.window = tkinter.Tk()

        self.window.title("YOUR TITLE") # TODO: Rename your title
        self.window.geometry("640x480") # NOTE: Change resolution fit to your program
        self.window.resizable(False, False)

        def closeWindow(event):
            self.window.withdraw()
            sys.exit()
            
        self.window.bind('<Escape>', closeWindow)
    
    def InitValues(self):
        self.Log = tkinter.StringVar(self.window, value='', name='Log')
        # NOTE: Add your needed variables here
    
    def BuildLabel(self, text: str, font: tkinter.font.Font, pos: PosType, parent: tkinter.Widget=None, *, var: tkinter.StringVar=None):
        label = tkinter.Label(parent if parent else self.window, text=text, height=3, font=font, textvariable=var)
        self.Labels.append((label, pos))
        return label
    
    def BuildEntry(self, pos: PosType, parent: tkinter.Widget=None):
        entry = tkinter.Entry(parent if parent else self.window)
        self.Elements.append((entry, pos))
        return entry
    
    def BuildButton(self, text: str, command: Callable[[], None], pos: PosType, parent: tkinter.Widget=None):
        button = tkinter.Button(parent if parent else self.window, text=text, command=command, bg='#dfdfdf')
        self.Elements.append((button, pos))
        return button
    
    def BuildFrame(self, text: str, pos: PosType, parent: tkinter.Widget=None):
        frame = tkinter.LabelFrame(parent if parent else self.window, text=text, relief=tkinter.GROOVE, bd=2)
        self.Elements.append((frame, pos))
        return frame
    
    def BuildRadioButton(self, text: str, variable: tkinter.StringVar, value: int, pos: PosType, parent: tkinter.Widget=None, *, command=None):
        radio = tkinter.Radiobutton(parent if parent else self.window, text=text, variable=variable, value=value, anchor='w', command=command)
        self.Elements.append((radio, pos))
        return radio

    def BuildProgressBar(self, pos: PosType, parent: tkinter.Widget=None):
        progress = tkinter.ttk.Progressbar(parent if parent else self.window, length=550)
        self.Elements.append((progress, pos))
        return progress

    def BuildComboBox(self, values: List[str], pos: PosType, parent: tkinter.Widget=None):
        comboBox = tkinter.ttk.Combobox(parent if parent else self.window, values=values, state="readonly")
        comboBox.current(0)
        self.Elements.append((comboBox, pos))
        return comboBox

    def BuildElements(self):
        copyright = self.BuildLabel('made by Runas & ', Font("Arial", 10), Pos(270, 430))
        copyright.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/Runas8128/'))
        copyright = self.BuildLabel('{YOUR_NAME}, ', Font("Arial", 10), Pos(380, 430))
        copyright.bind('<Button-1>', lambda e: webbrowser.open_new('https://github.com/Your_Name/Your_Repo_Name'))
        # NOTE: You can change license since this program does'nt have SA License
        copyright = self.BuildLabel('CC BY License', Font("Arial", 10), Pos(480, 430))
        copyright.bind('<Button-1>', lambda e: webbrowser.open_new('https://creativecommons.org/licenses/by/4.0/deed.ko'))

        self.BuildLabel("{Your_Program_Title}", Font("Arial", 20), Pos(200, -10))
        fileNameEntry = self.BuildEntry(Pos(60, 90, 400, 30))

        def onClickBrowseButton():
            adofaiFileName = tkinter.filedialog.askopenfilename(
                initialdir="/",
                title="Select file",
                filetypes=(
                    ("adofai files", "*.adofai"),
                )
            )

            fileNameEntry.delete(0, "end")
            fileNameEntry.insert(0, adofaiFileName)
            self.adofaiFileName = adofaiFileName

        self.BuildButton("Browse...", onClickBrowseButton, Pos(490, 90, 100, 30))

        # TODO: Add your components here

        self.BuildLabel("", Font('Arial', 10), Pos(50, 410), var=self.Log)
        progress = self.BuildProgressBar(Pos(50, 390, 400))

        def Run():
            fileName = fileNameEntry.get()

            if not fileName or not os.path.isfile(fileName):
                tkinter.messagebox.showerror("error", "파일을 선택해주세요!")
                return
            
            def logger(log: str):
                self.Log.set(log)
                progress.step(100 / 3) # TODO: Change 3 to number of steps in your Runner process
            
            try:
                adofaiParser.run(
                    fileName,
                    # Your arguments...
                    logger
                )
                tkinter.messagebox.showinfo("done", "성공했습니다!")
            except adofaiParser.ParseException as Error:
                tkinter.messagebox.showerror("error", str(Error))
            except ValueError as Error:
                tkinter.messagebox.showerror("error", "정수 또는 실수를 적절히 입력해주세요!")
            # NOTE: add your additional Exceptions here
            except Exception as Error:
                tkinter.messagebox.showerror("fatal", f"예상치못한 오류가 발생했습니다.\n{Error}")
            finally:
                progress.stop()
                self.Log.set('')

        self.BuildButton("실행!", Run, Pos(485, 350, 100, 70))
        self.window.bind('<Return>', lambda event: Run())
    
    def PlaceElements(self):
        for Label in self.Labels:
            Label[0].place(**Label[1])

        for Element in self.Elements:
            Element[0].place(**Element[1])

    def start(self):
        self.window.mainloop()
