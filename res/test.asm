ASSUME CS:CODE,DS:DATA

DATA SEGMENT ;asd
    arr db 5 dup(15)
    string db 1, 2, 3, 4
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