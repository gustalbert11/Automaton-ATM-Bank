from collections import deque
from atm import AtmMealy
from bank import BankMealy

class AtmSystem:
    def __init__(self):
        self.atm = AtmMealy()
        self.bank = BankMealy()
        
        self.queue_atm_to_bank = deque()
        self.queue_bank_to_atm = deque()

        # ==========================================
        # BASE DE DATOS SIMULADA Y MEMORIA
        # ==========================================
        self.db_pin = "1234"     # Clave predeterminada
        self.db_saldo = 1000.0   # Saldo predeterminado
        
        # Memoria temporal para la transacción actual
        self.temp_pin = ""
        self.temp_monto = 0.0

    def send_external_input_to_atm(self, signal):
        output = self.atm.process_input(signal)
        
        signals_for_bank = ["validando", "pedir_saldo", "verificar_fondos", "procesar_retiro"]
        if output in signals_for_bank:
            self.queue_atm_to_bank.append(output)
            self.process_queues()

    def process_queues(self):
        while self.queue_atm_to_bank or self.queue_bank_to_atm:
            
            if self.queue_atm_to_bank:
                signal_for_bank = self.queue_atm_to_bank.popleft()
                bank_output = self.bank.process_input(signal_for_bank)
                
                # LA LÓGICA DEL BANCO AHORA USA DATOS REALES
                if bank_output == "check_bd_pin":
                    if self.temp_pin == self.db_pin:
                        bank_response = self.bank.process_input("db_clave_ok") 
                    else:
                        bank_response = self.bank.process_input("db_clave_no") 
                    self.queue_bank_to_atm.append(bank_response)       
                
                elif bank_output == "leer_bd_saldo":
                    print(f"\n[SISTEMA DEL BANCO] --> Tu saldo actual es: ${self.db_saldo}")
                    bank_response = self.bank.process_input("bd_leido")    
                    self.queue_bank_to_atm.append(bank_response)       
                
                elif bank_output == "check_bd_monto":
                    if self.temp_monto <= self.db_saldo:
                        # ¡Aquí enviamos la señal correcta a la nueva transición!
                        bank_response = self.bank.process_input("db_fondos_ok") 
                    else:
                        print(f"\n[SISTEMA DEL BANCO] --> Fondos insuficientes. Tienes: ${self.db_saldo}")
                        bank_response = self.bank.process_input("db_fondos_no") 
                    self.queue_bank_to_atm.append(bank_response)       
                
                elif bank_output == "update_bd":
                    self.db_saldo -= self.temp_monto # Descontamos el dinero de la cuenta
                    print(f"\n[SISTEMA DEL BANCO] --> Retiro exitoso. Nuevo saldo: ${self.db_saldo}")
                    bank_response = self.bank.process_input("db_update_ok") 
                    self.queue_bank_to_atm.append(bank_response)        

            if self.queue_bank_to_atm:
                signal_for_atm = self.queue_bank_to_atm.popleft()
                atm_output = self.atm.process_input(signal_for_atm)
                
                if atm_output == "procesar_retiro":
                    self.queue_atm_to_bank.append(atm_output)


# ==========================================
# SIMULADOR INTERACTIVO CON TRADUCTOR DE DATOS
# ==========================================
if __name__ == "__main__":
    system = AtmSystem()
    
    print("======================================================")
    print("   SIMULADOR INTERACTIVO DE ATM (Con base de datos)")
    print("======================================================")
    print(f"DATOS DE PRUEBA -> PIN: {system.db_pin} | Saldo: ${system.db_saldo}\n")

    while True:
        current_state = system.atm.current_state
        print(f"\n--- PANTALLA DEL ATM (Estado interno: {current_state}) ---")
        
        # Dependiendo del estado, mostramos un menú distinto y procesamos datos reales
        
        if current_state == "q0":
            opcion = input("Presiona 'ENTER' para insertar tu tarjeta (o escribe 'salir' para apagar): ")
            if opcion.lower() == 'salir': break
            system.send_external_input_to_atm("tarjeta_in")
            
        elif current_state == "q1":
            pin_ingresado = input("Por favor, ingresa tu PIN de 4 dígitos: ")
            system.temp_pin = pin_ingresado # Guardamos el PIN en memoria
            system.send_external_input_to_atm("datos_in") # Enviamos la señal al autómata
            
        elif current_state == "q3":
            print("MENÚ PRINCIPAL:")
            print("1. Retirar efectivo")
            print("2. Consultar saldo")
            print("3. Salir y retirar tarjeta")
            opcion = input(">> Elige una opción (1/2/3): ").strip()
            
            if opcion == "1":
                system.send_external_input_to_atm("us_retiro")
            elif opcion == "2":
                system.send_external_input_to_atm("us_consulta")
            elif opcion == "3":
                system.send_external_input_to_atm("cancelar")
            else:
                print("[!] Opción inválida.")
                
        elif current_state == "q5":
            # El saldo ya se imprimió desde la función del banco
            input("\nPresiona 'ENTER' para volver al menú...")
            system.send_external_input_to_atm("timeout_volver")
            
        elif current_state == "q6":
            try:
                monto_ingresado = float(input("¿Cuánto dinero deseas retirar? $"))
                if monto_ingresado <= 0:
                    raise ValueError
                system.temp_monto = monto_ingresado # Guardamos el monto en memoria
                system.send_external_input_to_atm("monto_in")
            except ValueError:
                print("[!] Por favor, ingresa una cantidad numérica válida.")
                
        elif current_state == "q9":
            input(f"\n>> (La máquina dispensa ${system.temp_monto}). Presiona 'ENTER' para tomar tu dinero y tarjeta...")
            system.temp_monto = 0 # Limpiamos la memoria
            system.temp_pin = ""
            system.send_external_input_to_atm("cierre_aut")