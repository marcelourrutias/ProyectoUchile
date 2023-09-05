#li 	x17, 5		# syscall 5: GetInt
addi x17, zero, 5
ecall			# Get int: INIT_ARG en a0
add	a1, zero, a0	# Guarda el valor X en a1

#li      x17, 5		# syscall 5: GetInt
addi x17, zero, 5
ecall			# Get int: INIT_ARG en a0
add 	a2, zero, a0	# Guarda el valor de Y en a2

#prueba

#li 	a3, 1		#guarda un 1 en a3
addi a3, zero, 1
fcvt.s.w fa0, a3	#lo convierte a Flotante y lo guarda en fa0
inicio:
mul 	a3, a3, a1		#multiplica recursivamente (X**n)*X, con caso inicial (X**n)=1
addi 	a2, a2, -1		#se le resta 1 al valor del exponente Y
beq 	a2,zero, result		#Si el exponente Y==0, salto a resuelto, está lista la recursión
bne 	a2, zero,inicio		#En caso contrario vuelve a inicio
result:
fcvt.s.w fa1, a3	#Una vez obtenido el valor se convierte a flotante y se guarda en fa1
fdiv.s 	fa0, fa0,fa1	#Luego se obtiene la división 1/(X**Y)=(1/X)**Y
#li 	x17, 2		# syscall 2: PrintFloat
addi x17, zero, 2
ecall			# Pint float: FLOAT_ARG en fa0


