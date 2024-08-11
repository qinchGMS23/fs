# -*- encoding:utf-8 -*-
''''
@Time : 2024/08/11/ 02:02:45
@Author : 氢気氚 | qinch
@Version : 1.0.4
@Contact : BlueRect@outlook.com
'''
import sys
import cmd
import os
print(os.getcwd())
class Conseols(cmd.Cmd):
    intro = "Welcome! Type help or ? to list all commands.\n"
    Virtual_Text = []
    State = 'N'
    F = None
    path = ""
    line = 0
    Error_Code = ["", "FileError", "Out Of Index", "Invalid Parameters", "File Exists"]
    try:
        if not sys.argv[1] == "":
            path = sys.argv[1]
            F = open(sys.argv[1], "r+", encoding="utf-8")
            print(State)
            State = 'H'
            prompt = f"[{F.name}]@{State}-[{line+1}]~>"
            Virtual_Text = F.readlines()

    except IndexError:
        State = 'V'
        path = "Buffer_Files-fs.txt"
        F = open("Buffer_Files-fs.txt", "w+", encoding="utf-8")
        Virtual_Text = F.readlines()
        prompt = f"[{F.name}]@{State}-[{line+1}]~>"
    def do_load(self, arg):
        '加载文件到缓冲区'
        self.F.close()
        if self.State == 'V':
            os.remove("Buffer_Files-fs.txt")
        try:
            self.F = open(arg, "r+", encoding="utf-8")
            self.State = 'H'
            self.prompt = f"[{self.F.name}]@{self.State}-[{self.line+1}]~>"
            self.Virtual_Text = self.F.readlines()
            self.path = self.F.name
        except FileNotFoundError:
            print(self.Error_Code[1])
            
    def do_show(self, arg=""):
        '展示文件内容'
        Error = 0
        if arg == "":
            print(f"===Show=== -> {1}:{len(self.Virtual_Text)} | {self.Error_Code[Error]}")
            k = 1
            for i in self.Virtual_Text:
                print(f"{k}|\t{i}", end="")
                k += 1
            print("\n", end="")
            print(f"===Show=== -> {1}:{len(self.Virtual_Text)} | {self.Error_Code[Error]}")
        else:
            try:
                parameter = arg.split( )
                if not len(parameter) > 2:
                    if len(parameter) == 1:
                        start = int(parameter[0]) - 1
                        k = 0
                        if start > len(self.Virtual_Text):
                            Error = 2
                        print(f"===Show=== -> {1}:{start+1} | {self.Error_Code[Error]}")
                        for i in self.Virtual_Text:
                            if k <= start:
                                print(f"{k+1}|\t{i}", end="")
                            k += 1
                        print("\n", end="")
                        print(f"\n===Show=== -> {1}:{start+1} | {self.Error_Code[Error]}")
                        Error = 0
                    elif len(parameter) == 2:
                        start = int(parameter[0]) - 1
                        stop = int(parameter[1]) - 1
                        k = 0
                        if start > len(self.Virtual_Text) or stop > len(self.Virtual_Text):
                            Error = 2
                        print(f"===Show=== -> {start+1}:{stop+1} | {self.Error_Code[Error]}")
                        for i in self.Virtual_Text:
                            if k >= start and k <= stop:
                                print(f"{k+1}|\t{i}", end="")
                            k += 1
                        if stop == len(self.Virtual_Text):
                            print("\n", end="")
                        print(f"\n===Show=== -> {start+1}:{stop+1} | {self.Error_Code[Error]}")
                        Error = 0
                else:
                    print("Too many parameters!")
            except ValueError:
                ...
    def do_i(self, arg):
        '插入指定行(未指定则以光标所在行为准)输入 -end 可结束插入'
        o = self.State
        self.State = 'I'
        if self.line > len(self.Virtual_Text):
            for i in range(self.line - len(self.Virtual_Text)):
                self.Virtual_Text.append("\n")
        if arg == "":
            while True:
                temp = input(f"[{self.F.name}]@{self.State}-[{self.line+1}]~>")
                if temp == "-end":
                    self.State = o
                    break
                self.Virtual_Text.insert(self.line, temp + "\n")
                self.line += 1
        else:
            try:
                self.line = int(arg)
                while True:
                    temp = input(f"[{self.F.name}]@{self.State}-[{self.line+1}]~>")
                    if temp == "-end":
                        self.State = o
                        break
                    self.Virtual_Text.insert(self.line, temp + "\n")
                    self.line += 1
            except ValueError:
                print(self.Error_Code[3])
    def do_o(self, arg):
        '覆写指定行(未指定则以光标所在行为准)输入 -end 可结束覆写'
        o = self.State
        self.State = 'W'
        if self.line > len(self.Virtual_Text):
            for i in range(self.line):
                self.Virtual_Text.append("\n")
        if arg == "":
            while True:
                try:
                    temp = input(f"[{self.F.name}]@{self.State}-[{self.line+1}]~>")
                    if temp == "-end":
                        self.State = o
                        break
                    else:
                        self.Virtual_Text[self.line] = temp+"\n"
                        self.line += 1
                except IndexError:
                    self.Virtual_Text.append(temp+"\n")
                    self.line += 1
            self.prompt = f"[{self.F.name}]@{self.State}-[{self.line+1}]~>"
        else:
            try:
                self.line = int(arg) - 1
                while True:
                        temp = input(f"[{self.F.name}]@{self.State}-[{self.line+1}]~>")
                        if temp == "-end":
                            self.State = o
                            break
                        else:
                            self.Virtual_Text[self.line] = temp+"\n"
                            self.line += 1
            except IndexError:
                self.Virtual_Text.append(temp+"\n")
            except ValueError:
                print(self.Error_Code[3])
    def do_del(self, arg):
        '删除多行或指定删除单行'
        parameter = arg.split( )
        try:
            if len(parameter) == 1:
                    temp = int(arg) - 1
                    del self.Virtual_Text[temp]
            elif len(parameter) == 2:
                    del self.Virtual_Text[int(parameter[0]) - 1: int(parameter[1]) - 1]
        except ValueError:
            print(self.Error_Code[3])
        except IndexError:
            print(self.Error_Code[2])
    def do_line(self, arg):
        '查看行或是更改行'
        if arg == "":
            print(self.line+1)
        else:
            try:
                self.line = int(arg) - 1
                self.prompt = f"[{self.F.name}]@{self.State}-[{self.line+1}]~>"
            except ValueError:
                print(self.Error_Code[3])
    def do_unload(self, arg):
        '将当前文件弹出'
        self.F.close()
        self.path = ""
        self.line = 0
        self.State = 'N'
        self.Virtual_Text = []
        self.prompt = f"[{self.path}]@{self.State}-[{self.line+1}]~>"
    def do_w(self, arg):
        '将缓冲区的文本写入文件'
        self.F.close()
        self.F = open(self.path, "w+", encoding="utf-8")
        self.F.writelines(self.Virtual_Text)
        self.F.close()
        if self.State == 'V':
            while True:
                    if input("Save this file? (Yes/No)") == "Yes":
                        try:
                            name = input("This is a new file,Pless type filename:")
                            os.rename("Buffer_Files-fs.txt", name)
                            self.State = 'H'
                            self.path = name
                            self.F = open(self.path, "r+", encoding="utf-8")
                            self.State = 'H'
                            self.prompt = f"[{self.F.name}]@{self.State}-[{self.line+1}]~>"
                            break
                        except FileExistsError:
                            print(self.Error_Code[4])
                    else:
                        break
        else:
            self.F = open(self.path, "r+", encoding="utf-8")
            self.State = 'H'
            self.prompt = f"[{self.F.name}]@{self.State}-[{self.line+1}]~>"
        
    def do_wq(self, arg):
        '将缓冲区的文本写入文件并退出fs'
        self.F.close()
        self.F = open(self.path, "w+", encoding="utf-8")
        self.F.writelines(self.Virtual_Text)
        self.F.close()
        
        if self.State == 'V':
            while True:
                    if input("Save this file? (Yes/No)") == "Yes":
                        try:
                            name = input("This is a new file,Pless type filename:")
                            os.rename("Buffer_Files-fs.txt", name)
                            self.State = 'H'
                            self.path = name
                            break
                        except FileExistsError:
                            print(self.Error_Code[4])
                    else:
                        os.remove("Buffer_Files-fs.txt")
        print("The fs is exit! (。・∀・)/")
        return True
    def do_echo(self, arg):
        print("show")
    def do_q(self, arg):
        '退出 fs'
        self.F.close()
        if self.State == 'V':
            os.remove("Buffer_Files-fs.txt")
        print("The fs is exit! (。・∀・)/")
        return True
    
conseols = Conseols(completekey="tab")
conseols.cmdloop()
