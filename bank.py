class BankMealy:
    def __init__(self):
        self.current_state = "p0" # Espera

        self.transitions = {
            ("p0", "validando"): ("p1", "check_bd_pin"),
            ("p1", "db_clave_ok"): ("p2", "clave_ok"),
            ("p1", "db_clave_no"): ("p0", "clave_no"),
            ("p2", "pedir_saldo"): ("p3", "leer_bd_saldo"),
            ("p3", "bd_leido"): ("p2", "saldo_ok"),
            ("p2", "verificar_fondos"): ("p4", "check_bd_monto"),
            ("p4", "db_fondos_no"): ("p2", "fondos_no"),
            ("p4", "db_fondos_ok"): ("p4", "fondos_ok"), 
            ("p4", "procesar_retiro"): ("p5", "update_bd"),
            ("p5", "db_update_ok"): ("p2", "banco_ok"),
            ("p2", "timeout_inactividad"): ("p0", "cerrar_sesion")
        }

    def process_input(self, input_signal):
        key = (self.current_state, input_signal)
        if key in self.transitions:
            new_state, output = self.transitions[key]
            print(f"[BANCO]  Estado: {self.current_state} --({input_signal})--> {new_state} | Salida: {output}")
            self.current_state = new_state
            return output
        return None