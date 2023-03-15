
ASSUME CS:CODE

CODE SEGMENT
isr0:
        jmp short start
        db 'Single Step Interrupt$'
start:  
        push ax
        push cx
        push ds

        lea dx,1
        mov ds,1010h
        mov ah,09h
        int 21h

        mov ax,4c01h
        int 21h

        pop ds
        pop cx
        pop ax
CODE ENDS