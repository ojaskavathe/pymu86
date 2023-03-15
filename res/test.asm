ASSUME CS:CODE,DS:DATA

data segment
    numS db '      $'
    string db 'your number is: $'
    num dw -348
data ends

code segment
    start:
        mov ax, data
        mov ds, ax
        
        mov dx, offset string
        mov ah, 09h
        int 21h

        mov ax, num
        
        mov bx, 10
        lea si, numS
	    add si, 5 
        cmp ax,0
        jge split
        neg ax

        split:
        xor dx, dx              ;remainder stored in dx, set dx = 0
        div bx
        add dl, 30h             ;convert num into corresponding ascii
        mov [si], dl
        dec si
        cmp ax, 0       
        jne split               ;if not zero, repeat
        
        cmp num, 0
        jge print
        mov byte ptr [si], '-'   ;if negative, addend '-' 
        dec si
        
        print:
        inc si
        mov ah, 9
        mov dx, si
        int 21h
        
        mov ah, 4ch
        int 21h

     
code ends
end start