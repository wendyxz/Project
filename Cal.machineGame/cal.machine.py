


import tkinter,time,decimal,math,string

root=tkinter.Tk()
root.title('Calculator')
root.resizable(0,0)
global cc, vartext, result, fh
result = fh = None
vartext = tkinter.StringVar()
cc = []

class key_figure:
    global cc, vartext, result, fh
    def __init__(self,anjian):
        self.anjian = anjian
    def jia(self):
        cc.append(self.anjian)
        vartext.set( ''.join(cc))
    def tui(self):
        cc.pop()
        vartext.set(''.join(cc))
    def clear(self):
        cc.clear()
        vartext.set('')
        result = None
        fh = None
    def zhengfu(self):
        if cc[0]:
            if cc[0] == '-':
                cc[0] = '+'
            elif cc[0] == '+':
                cc[0] = '-'
            else:
                cc.insert(0, '-')
        vartext.set(''.join(cc))
    def xiaoshudian(self):
        if cc.count('.') >= 1:
            pass
        else:
            if cc == [] :
                cc.append('0')
            cc.append('.')
            vartext.set(''.join(cc))
    def math_work(self):
        global cc, vartext, result, fh
        if vartext.get() == '':
            pass
        else:
            get1 = decimal.Decimal(vartext.get())
            if self.anjian in ('1/x','sqrt'):
                if self.anjian == '1/x':
                    result = 1/get1
                elif self.anjian == 'sqrt':
                    result = math.sqrt(get1)
            elif  self.anjian in ('+','-','*','/','='):
                if fh is not None:
                    get1 = decimal.Decimal(result)
                    get2 = decimal.Decimal(vartext.get())
                    if fh == '+':
                        result = get1 + get2
                    elif fh == '-':
                        result = get1 - get2
                    elif fh == '*':
                        result = get1 * get2
                    elif fh == '/':
                        result = get1 / get2
                else:
                    result = get1
                if self.anjian == '=':
                    fh = None
                else:
                    fh = self.anjian
            print(fh)
            print(result)
            vartext.set(str(result))
            cc.clear()

def copy1():
    # tkinter.Misc().clipboard_clear()
    tkinter.Misc().clipboard_append(string(vartext.get()))

def buju(root):
    global cc, vartext, result, fh
    entry1 = tkinter.Label(root, width=30, height=2, bg='pink', anchor='se', textvariable=vartext)
    entry1.grid(row=0, columnspan=5)
    buttonMC=tkinter.Button(root,text='MC',width=5)
    buttonMR=tkinter.Button(root,text='MR',width=5)
    buttonMS=tkinter.Button(root,text='MS',width=5)
    buttonM1=tkinter.Button(root,text='M+',width=5)
    buttonM2=tkinter.Button(root,text='M-',width=5)
    buttonMC.grid(row=1,column=0)
    buttonMR.grid(row=1,column=1)
    buttonMS.grid(row=1,column=2)
    buttonM1.grid(row=1,column=3)
    buttonM2.grid(row=1,column=4)


    buttonJ=tkinter.Button(root,text='←',width=5,command=key_figure('c').tui)
    buttonCE=tkinter.Button(root,text='CE',width=5)
    buttonC=tkinter.Button(root,text=' C ',width=5,command=key_figure('c').clear)
    button12=tkinter.Button(root,text='±',width=5,command=key_figure('c').zhengfu)
    buttonD=tkinter.Button(root,text='√',width=5,command=key_figure('sqrt').math_work)
    buttonJ.grid(row=2,column=0)
    buttonCE.grid(row=2,column=1)
    buttonC.grid(row=2,column=2)
    button12.grid(row=2,column=3)
    buttonD.grid(row=2,column=4)

    button7=tkinter.Button(root,text=' 7 ',width=5,command=key_figure('7').jia)
    button8=tkinter.Button(root,text=' 8 ',width=5,command=key_figure('8').jia)
    button9=tkinter.Button(root,text=' 9 ',width=5,command=key_figure('9').jia)
    buttonc=tkinter.Button(root, text=' / ',width=5,command=key_figure('/').math_work)
    buttonf= tkinter.Button(root, text=' % ',width=5)
    button7.grid(row=3,column=0)
    button8.grid(row=3,column=1)
    button9.grid(row=3,column=2)
    buttonc.grid(row=3,column=3)
    buttonf.grid(row=3,column=4)

    button4=tkinter.Button(root,text=' 4 ',width=5,command=key_figure('4').jia)
    button5=tkinter.Button(root,text=' 5 ',width=5,command=key_figure('5').jia)
    button6=tkinter.Button(root,text=' 6 ',width=5,command=key_figure('6').jia)
    buttonx=tkinter.Button(root,text=' * ',width=5,command=key_figure('*').math_work)
    buttonfs=tkinter.Button(root,text='1/x',width=5,command=key_figure('1/x').math_work)
    button4.grid(row=4,column=0)
    button5.grid(row=4,column=1)
    button6.grid(row=4,column=2)
    buttonx.grid(row=4,column=3)
    buttonfs.grid(row=4,column=4)

    button1 = tkinter.Button(root, text=' 1 ',width=5,command=key_figure('1').jia)
    button2 = tkinter.Button(root, text=' 2 ',width=5,command=key_figure('2').jia)
    button3 = tkinter.Button(root, text=' 3 ',width=5,command=key_figure('3').jia)
    button_= tkinter.Button(root, text=' - ',width=5,command=key_figure('-').math_work)
    buttondy= tkinter.Button(root, text=' \n = \n ',width=5,command=key_figure('=').math_work)
    button1.grid(row=5, column=0)
    button2.grid(row=5, column=1)
    button3.grid(row=5, column=2)
    button_.grid(row=5, column=3)
    buttondy.grid(row=5, column=4,rowspan=2)

    button0=tkinter.Button(root,text='   0   ',width=11,command=key_figure('0').jia)
    buttonjh = tkinter.Button(root,text=' . ',width=5,command=key_figure('c').xiaoshudian)
    buttonjia=tkinter.Button(root,text=' + ',width=5,command=key_figure('+').math_work)
    button0.grid(row=6,column=0,columnspan=2)
    buttonjh.grid(row=6,column=2)
    buttonjia.grid(row=6,column=3)
def lis_t(root):

    menu=tkinter.Menu(root)
    submenu1=tkinter.Menu(menu,tearoff=0)
    menu.add_cascade(label='View',menu=submenu1)
    submenu2 = tkinter.Menu(menu, tearoff=0)
    submenu2.add_command(label='Copy')
    submenu2.add_command(label='Paste')
    menu.add_cascade(label='Edit',menu=submenu2)
    submenu = tkinter.Menu(menu, tearoff=0)
    submenu.add_command(label='View help')
    submenu.add_separator()
    submenu.add_command(label='About')
    menu.add_cascade(label='Help',menu=submenu)
    root.config(menu=menu)


buju(root)
lis_t(root)
root.mainloop()
