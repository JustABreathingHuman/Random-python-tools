; Press and hold Left Alt to simulate random symbol key presses

; List of symbols to randomly choose from
symbols := ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "_", "+", "[", "]", "{", "}", "|", "\", ";", ":", "'", "\", ".", "/", "<", ">", "?"]

; Flag to track the key-holding state
isSending := false

~LShift::
    if (!isSending) {
        isSending := true
        SetTimer, SendRandomSymbol, 100  ; send a symbol every 100ms
    }
return

~RShift Up::
    isSending := false
    SetTimer, SendRandomSymbol, Off
return

SendRandomSymbol:
    Random, index, 1, % symbols.MaxIndex()
    Send, % symbols[index]
return

