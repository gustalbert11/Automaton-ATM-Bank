class AtmMealy:
    def __init__(self):
        self.current_state = "q0" # Inicio

        self.transitions = {
            ("q0", "tarjeta_in"): ("q1", "pida_pin"),
            ("q1", "datos_in"): ("q2", "validando"),
            ("q2", "clave_ok"): ("q3", "mostrar_menu"),
            ("q2", "clave_no"): ("q0", "error_expulsar"),
            ("q3", "us_retiro"): ("q6", "pedir_monto"),
            ("q3", "us_consulta"): ("q4", "pedir_saldo"),
            ("q6", "monto_in"): ("q7", "verificar_fondos"),
            ("q7", "fondos_ok"): ("q8", "procesar_retiro"),
            ("q7", "fondos_no"): ("q3", "msj_sin_fondos"),
            ("q8", "banco_ok"): ("q9", "dar_dinero"),
            ("q9", "cierre_aut"): ("q0", "ticket_gracias"),
            ("q4", "saldo_ok"): ("q5", "mostrar_saldo"),
            ("q5", "timeout_volver"): ("q3", "mostrar_menu")
        }

    def process_input(self, input_signal):
        key = (self.current_state, input_signal)
        if key in self.transitions:
            new_state, output = self.transitions[key]
            print(f"[CAJERO] Estado: {self.current_state} --({input_signal})--> {new_state} | Salida: {output}")
            self.current_state = new_state
            return output
        return None