#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%

listFile := "exes.txt"
Gui, Add, ListBox, vExeList w400 h200 gOnSelect
Gui, Add, Button, x+1 w100 h25 gAddExe, Add EXE
Gui, Add, Button, y+5 w100 h25 gRunExe, Run as Invoker
Gui, Add, Button, y+5 w100 h25 gDeleteExe, Delete
Gui, Show, , Exemanager

LoadList()
return

GuiClose:
ExitApp

AddExe:
FileSelectFile, exePath, 3,, Select EXE, *.exe
if (!exePath)
    return
FileRead, currentList, %listFile%
if InStr(currentList, exePath)
{
    MsgBox, Already in list.
    return
}
FileAppend, %exePath%`n, %listFile%
GuiControl,, ExeList, |  ; Clear list
LoadList()
return

LoadList() {
    global listFile
    if !FileExist(listFile)
        FileAppend,, %listFile%
    FileRead, contents, %listFile%
    StringReplace, contents, contents, `r`n, |, All
    GuiControl,, ExeList, %contents%
}

OnSelect:
return

RunExe:
GuiControlGet, selected,, ExeList
if (!selected) {
    MsgBox, Please select an EXE.
    return
}
Run, %selected%
return

DeleteExe:
GuiControlGet, selected,, ExeList
if (!selected) {
    MsgBox, Please select an EXE to delete.
    return
}
FileRead, fullList, %listFile%
newList := ""
Loop, Parse, fullList, `n, `r
{
    if (A_LoopField != selected)
        newList .= A_LoopField . "`n"
}
FileDelete, %listFile%
FileAppend, %newList%, %listFile%
GuiControl,, ExeList, |
LoadList()
return
