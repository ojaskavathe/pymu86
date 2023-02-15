ASSUME CS:CODE,DS:DATA

DATA SEGMENT ;asd
    arr db 5 dup(15)
    var db 3, 5, 'gfd', 3, 14
    string db 'hello? this is ?',?, 'a string?' ;?????  
DATA ENDS

CODE SEGMENT
    start:
        mov ax, data
        mov ds, ax
        
        mov bx, $

        mov ah,4ch
        int 21h  

CODE ENDS
END start