xpos1=
xpos2=
colour1=
min=
max=
SetMouseDelay,-1
SetBatchLines, -1
Process, Priority,, High
 
MsgBox autoclick script. press F1 to define the following variables: scan area topleft, bottomright, colour1, colour2, waittime min and max. Press F2 to stop execution.
f1::
If xpos1 =  
	{
	MouseGetPos, xpos1, ypos1 
	MsgBox pos1
	Return
	}
If xpos2 =  
	{
	MouseGetPos, xpos2, ypos2
	MsgBox pos2
	Return
	}
If colour1=
	{
	InputBox, colour1, %colour1%:
	MsgBox %colour1%
	Return
	}
If min=
	{
	InputBox, min, minimum wait time:
	Return
	}
If max=
	{
	InputBox, max, maximum wait time:
	MsgBox ready to start
	}

loop{
	PixelSearch, Px, Py, %xpos1%, %ypos1%, %xpos2%, %ypos2%, colour1, 5, Fast
	If Px !=
		{
		Py:=Py+4
		MouseClick, left, %Px%, %Py%
		}
	Random, waitt, min, max
	sleep waitt
	}	
 
f2::
Msgbox, Script ended.
exitapp