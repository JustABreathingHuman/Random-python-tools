SetMouseDelay,-1
SetBatchLines, -1
Process, Priority,, High

x1=
x2=
i1=
i2=

f1::
If x1=
	{
	MouseGetPos, x1, y1
	MsgBox pos1 set
	Return
	}
If x2=
	{
	MouseGetPos, x2, y2
	MsgBox pos2 set
	Return
	}
If i1=
	{
	InputBox, i1, minimum interval
	MsgBox min set to %i1%
	Return
	}
If i2=
	{
	InputBox, i2, minimum interval
	MsgBox max set to %i2%
	MsgBox ready to start
	}

loop{
	Random, xp, x1, x2
	Random, yp, y1, y2
	MouseMove, xp, yp, 50
	MouseClick
	Random, time, i1, i2
	Sleep, time
	}

f2::
MsgBox script ended
exitapp
