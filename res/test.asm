ASSUME CS:CODE,DS:DATA

DATA SEGMENT ;asd
    arr db 5 dup(15)
    num db 4
    string db 'hello'
DATA ENDS

CODE SEGMENT
    start:
        mov ax, data
        mov ds, ax

        mov si, 5 
        movsb
        mov al, num

        mov cx, [1432h]
        mov bx, $

        mov ah,4ch
        int 21h
        call

CODE ENDS
END start