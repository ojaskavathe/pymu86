ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    msg db "'h;e?'l;lo$", ? ; this is a comme'nt ; sdf'sd 
DATA ENDS  

CODE SEGMENT
    start: 
        mov ax, 1000h
        mov bl, 0
        div bl
        mov ah,4ch
        int 21h  

CODE ENDS
END START