ASSUME CS:CODE,DS:DATA

data segment
    first db '\nfirst$'
    second db 'second$'
data ends

code segment
    start:
        mov ax, data
        mov ds, ax
        
        call print
        mov ah, 09h
        lea dx, first
        int 21h
        
        mov ah, 4ch
        int 21h

        print:
        mov ah, 09h
        lea dx, second
        int 21h
        ret
        
     
code ends
end start