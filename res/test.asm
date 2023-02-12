ASSUME CS:CODE,DS:DATA

DATA SEGMENT ;asd
    msg db "'h;e?'l;lo$", ? ; this is a comme'nt ; sdf'sd 
DATA ENDS  

CODE SEGMENT
    start:
        mov ax, data
        mov ds, ax
        
        mov bx, $

        mov ah,4ch
        int 21h  

CODE ENDS
END START