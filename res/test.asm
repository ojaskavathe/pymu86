ASSUME CS:CODE,DS:DATA

DATA SEGMENT ;asd
    arr db 5 dup(15)
    num dw 10
    string db 'hello'
DATA ENDS

CODE SEGMENT
    start:
        mov ax, data
        mov ds, ax
        
        mov dx, 'a'
        add ax, dx

        mov cx, [1432h]
        mov bx, $

        mov ah,4ch
        int 21h
        call

CODE ENDS
END start