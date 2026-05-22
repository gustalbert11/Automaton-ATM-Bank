class AtmMealy:

    def __init__(self):

        self.current_state = "q0"

        # Transition table
        self.transitions = {

            ("q0", "card_in"): "q1",

            ("q1", "data_in"): "q2",
            ("q1", "cancel"): "q0",

            ("q2", "pin_ok"): "q3",
            ("q2", "pin_wrong"): "q0",

            ("q3", "usr_balance"): "q4",
            ("q3", "usr_withdraw"): "q5",
            ("q3", "usr_change_pin"): "q7",

            ("q5", "bank_ok"): "q6",

            ("q6", "auto_close"): "q0"
        }

        # Output table (Mealy)
        self.outputs = {

            ("q0", "card_in"): "request_pin",

            ("q1", "data_in"): "validate_data",

            ("q2", "pin_ok"): "show_menu",
            ("q2", "pin_wrong"): "pin_error",

            ("q3", "usr_balance"): "show_balance",
            ("q3", "usr_withdraw"): "request_amount",

            ("q5", "bank_ok"): "dispense_cash",

            ("q6", "auto_close"): "logout"
        }

    def process_input(self, input_signal):

        key = (self.current_state, input_signal)

        if key in self.transitions:

            output = self.outputs.get(key, None)

            new_state = self.transitions[key]

            print(f"[{self.current_state}] --{input_signal}--> [{new_state}]")

            if output:
                print(f"Output: {output}")

            self.current_state = new_state

        else:
            print("Invalid input")