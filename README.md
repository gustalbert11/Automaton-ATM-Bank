# Automaton-ATM-Bank
This project implements a finite-state automaton that models the behavior of an ATM, including states such as card insertion, PIN verification, balance inquiry, cash withdrawal, and communication with the bank server.

 # Enlace a la presentacion:
 https://youtu.be/UqX7q3fX7ZE

 #Definiciones formales
 Autómata del Cajero (Matm​)

El cajero es el elemento de borde que interactúa con el usuario y reacciona a las respuestas del banco.

Conjunto de Estados:
Qatm​={q0​,q1​,q2​,q3​,q4​,q5​,q6​,q7​,q8​,q9​}

Alfabeto de Entrada (Interacciones del usuario y respuestas del banco):
Σatm​={tarjeta_in,datos_in,clave_ok,clave_no,us_retiro,us_consulta,cancelar,monto_in,fondos_ok,fondos_no,banco_ok,cierre_aut,saldo_ok,timeout_volver}

Alfabeto de Salida (Mensajes a pantalla y peticiones al banco):
Λatm​={pida_pin,validando,mostrar_menu,error_expulsar,pedir_monto,pedir_saldo,verificar_fondos,procesar_retiro,msj_sin_fondos,dar_dinero,ticket_gracias,mostrar_saldo}

Estado Inicial:
q0​=q0​

Funciones de Transición (δatm​) y Salida (λatm​):
Estado Actual (q)	Entrada (σ)	Siguiente Estado (δatm​)	Salida (λatm​)
q0​	               tarjeta_in	   q1​	                        pida_pin
q1​	               datos_in	     q2​	                        validando
q2​	               clave_ok     	q3​	                        mostrar_menu
q2​	               clave_no     	q0​	                        error_expulsar
q3​	               us_retiro    	q6​	                       pedir_monto
q3​               	us_consulta  	q4​	                     pedir_saldo
q3​	               cancelar	     q0​	                        ticket_gracias
q4​	               saldo_ok	      q5​                        	mostrar_saldo
q5​	               timeout_volver	q3​	                      mostrar_menu
q6​	               monto_in	      q7​	                        verificar_fondos
q7​	               fondos_ok	     q8​	                        procesar_retiro
q7​	               fondos_no	     q3​	                       msj_sin_fondos
q8​	               banco_ok	      q9​	                        dar_dinero
q9​	               cierre_aut	    q0​	                      ticket_gracias

Autómata del Banco (Mbank​)

El banco es el sistema central que procesa las reglas de negocio verificando la base de datos simulada.

Conjunto de Estados:
Qbank​={p0​,p1​,p2​,p3​,p4​,p5​}

Alfabeto de Entrada (Peticiones del cajero y validaciones internas de BD):
Σbank​={validando,db_clave_ok,db_clave_no,pedir_saldo,bd_leido,verificar_fondos,db_fondos_no,db_fondos_ok,procesar_retiro,db_update_ok,timeout_inactividad}

Alfabeto de Salida (Mensajes de vuelta al cajero y comandos a la BD):
Λbank​={check_bd_pin,clave_ok,clave_no,leer_bd_saldo,saldo_ok,check_bd_monto,fondos_no,fondos_ok,update_bd,banco_ok,cerrar_sesion}

Estado Inicial:
q0​=p0​

Funciones de Transición (δbank​) y Salida (λbank​):
Estado Actual (p)	Entrada (σ)	Siguiente Estado (δbank​)	Salida (λbank​)
p0​	               validando	          p1​              	check_bd_pin
p1​	               db_clave_ok	        p2​	              clave_ok
p1​	               db_clave_no	        p0​	              clave_no
p2​	               pedir_saldo	        p3​	              leer_bd_saldo
p2​	               verificar_fondos	   p4​	              check_bd_monto
p2​	               timeout_inactividad	p0​	              cerrar_sesion
p3​                bd_leido	           p2​	              saldo_ok
p4                db_fondos_ok	       p4​	              fondos_ok
p4​                db_fondos_no	       p2​	              fondos_no
p4​                procesar_retiro	    p5​	              update_bd
p5​	               db_update_ok	       p2​	              banco_ok
