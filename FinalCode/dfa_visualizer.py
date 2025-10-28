import tkinter as tk
from tkinter import ttk, messagebox
import math

class DFA:
    def __init__(self):
        self.states = {}  # Dictionary to store state info: {name: (x, y, is_start, is_accept)}
        self.transitions = {}  # Dictionary to store transitions: {(from_state, symbol): to_state}
        self.alphabet = set()  # Set of input symbols
        self.current_state = None
        self.state_counter = 0

    def add_state(self, x, y, is_start=False, is_accept=False):
        name = f"q{self.state_counter}"
        self.states[name] = (x, y, is_start, is_accept)
        if is_start:
            self.current_state = name
        self.state_counter += 1
        return name

    def add_transition(self, from_state, to_state, symbol_input):
        symbols = [s.strip() for s in symbol_input.split(',') if s.strip()]
        for symbol in symbols:
            self.transitions[(from_state, symbol)] = to_state
            self.alphabet.add(symbol)

    def set_accept_state(self, state_name):
        x, y, is_start, _ = self.states[state_name]
        self.states[state_name] = (x, y, is_start, True)

    def set_start_state(self, state_name):
        if self.current_state:
            x, y, _, is_accept = self.states[self.current_state]
            self.states[self.current_state] = (x, y, False, is_accept)
        self.current_state = state_name
        x, y, _, is_accept = self.states[state_name]
        self.states[state_name] = (x, y, True, is_accept)

    def process_input(self, symbol):
        if self.current_state and (self.current_state, symbol) in self.transitions:
            self.current_state = self.transitions[(self.current_state, symbol)]
            return True
        return False

    def reset(self):
        for state, (x, y, is_start, is_accept) in self.states.items():
            if is_start:
                self.current_state = state
                break

    def is_accepting_state(self, state_name):
        if state_name in self.states:
            return self.states[state_name][3]
        return False

class DFAVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA Visualizer")
        self.dfa = DFA()
        self.selected_state = None
        self.transition_from = None
        self.selected_transition = None
        self.mode = "define"  # Modes: "define" or "simulate"
        self.action_mode = ""  # "set_start", "set_accept", "add_transition", "delete"
        self.input_string = ""
        self.current_symbol_index = 0
        self.state_radius = 30

        self.setup_gui()

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=800, height=500, bg='white', borderwidth=2, relief=tk.SUNKEN)
        self.canvas.grid(row=0, column=0, columnspan=3, pady=5)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)

        instructions_text = (
            "1. Click on canvas to add states. Select a state, then use 'Set Start' or 'Set Accept'.\n"
            "2. For transitions (incl. loops), click 'Add Transition', select states, enter symbol.\n"
            "3. Drag states to move. Use 'Delete' for states/transitions. 'Step' to simulate, 'Reset' to start over."
        )
        self.instructions_label = ttk.Label(self.main_frame, text=instructions_text, justify=tk.LEFT)
        self.instructions_label.grid(row=1, column=0, columnspan=3, pady=5, sticky=tk.W)

        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky=tk.W+tk.E)

        ttk.Button(self.control_frame, text="Add State", command=lambda: self.set_action_mode("add_state")).grid(row=0, column=0, padx=5)
        ttk.Button(self.control_frame, text="Set Start", command=lambda: self.set_action_mode("set_start")).grid(row=0, column=1, padx=5)
        ttk.Button(self.control_frame, text="Set Accept", command=lambda: self.set_action_mode("set_accept")).grid(row=0, column=2, padx=5)
        ttk.Button(self.control_frame, text="Add Transition", command=lambda: self.set_action_mode("add_transition")).grid(row=0, column=3, padx=5)
        ttk.Button(self.control_frame, text="Delete", command=lambda: self.set_action_mode("delete")).grid(row=0, column=4, padx=5)
        ttk.Button(self.control_frame, text="Step", command=self.step_simulation).grid(row=0, column=5, padx=5)
        ttk.Button(self.control_frame, text="Reset", command=self.reset_dfa).grid(row=0, column=6, padx=5)

        ttk.Label(self.control_frame, text="Input/Symbol:").grid(row=0, column=7, padx=5)
        self.input_entry = ttk.Entry(self.control_frame, width=20)
        self.input_entry.grid(row=0, column=8, padx=5)
        self.input_entry.bind("<Return>", self.handle_input_entry)

        self.status_label = ttk.Label(self.control_frame, text="Mode: Define DFA")
        self.status_label.grid(row=0, column=9, padx=5)

        self.redraw_dfa()

    def set_action_mode(self, mode):
        self.action_mode = mode
        self.status_label.config(text=f"Mode: {mode.replace('_', ' ').title()}")
        if mode != "delete":
            self.selected_transition = None

    def canvas_click(self, event):
        x, y = event.x, event.y
        state_clicked = self.get_state_at_position((x, y))
        transition_clicked = self.get_transition_at_position((x, y))

        if self.action_mode == "add_state":
            if not state_clicked:
                name = self.dfa.add_state(x, y)
                self.redraw_dfa()
                self.status_label.config(text=f"Added state {name}")

        elif self.action_mode == "delete":
            if state_clicked:
                self.delete_state(state_clicked)
                self.redraw_dfa()
                self.status_label.config(text=f"Deleted state {state_clicked}")
            elif transition_clicked:
                self.delete_transition(transition_clicked)
                self.redraw_dfa()
                self.status_label.config(text="Deleted transition")
            self.selected_state = None
            self.selected_transition = None
            self.action_mode = ""
            self.status_label.config(text="Mode: Define DFA")

        elif state_clicked:
            if self.action_mode == "set_start":
                self.dfa.set_start_state(state_clicked)
                self.redraw_dfa()
                self.action_mode = ""
                self.status_label.config(text="Mode: Define DFA")

            elif self.action_mode == "set_accept":
                self.dfa.set_accept_state(state_clicked)
                self.redraw_dfa()
                self.action_mode = ""
                self.status_label.config(text="Mode: Define DFA")

            elif self.action_mode == "add_transition":
                if self.transition_from is None:
                    self.transition_from = state_clicked
                    self.selected_state = state_clicked
                    self.status_label.config(text=f"Selected {state_clicked} for transition start")
                else:
                    symbol = self.input_entry.get().strip() or "a"
                    self.dfa.add_transition(self.transition_from, state_clicked, symbol)
                    self.transition_from = None
                    self.selected_state = None
                    self.action_mode = ""
                    self.input_entry.delete(0, tk.END)
                    self.redraw_dfa()
                    self.status_label.config(text="Mode: Define DFA")
            else:
                self.selected_state = state_clicked
                self.dragging_state = state_clicked
                self.drag_start_x, self.drag_start_y = x, y
                self.status_label.config(text=f"Selected state {state_clicked} - Drag to move")

            self.redraw_dfa()

    def get_state_at_position(self, pos):
        x, y = pos
        for state, (sx, sy, _, _) in self.dfa.states.items():
            if (x - sx) ** 2 + (y - sy) ** 2 <= self.state_radius ** 2:
                return state
        return None

    def get_transition_at_position(self, pos):
        x, y = pos
        for (from_state, symbol), to_state in self.dfa.transitions.items():
            from_x, from_y, _, _ = self.dfa.states[from_state]
            to_x, to_y, _, _ = self.dfa.states[to_state]
            if from_state == to_state:  # Self-loop hitbox
                mid_x, mid_y = from_x, from_y - self.state_radius - 15
                if abs(x - mid_x) < 20 and abs(y - mid_y) < 10:
                    return (from_state, symbol, to_state)
            else:
                dx, dy = to_x - from_x, to_y - from_y
                length = math.hypot(dx, dy) or 1
                ux, uy = dx/length, dy/length
                start_x = from_x + ux * self.state_radius
                start_y = from_y + uy * self.state_radius
                end_x   = to_x   - ux * self.state_radius
                end_y   = to_y   - uy * self.state_radius
                mid_x, mid_y = (start_x + end_x)/2, (start_y + end_y)/2
                if abs(x - mid_x) < 20 and abs(y - mid_y) < 10:
                    return (from_state, symbol, to_state)
        return None

    def delete_state(self, state_name):
        if state_name in self.dfa.states:
            del self.dfa.states[state_name]
            # Remove associated transitions
            to_remove = [k for k in self.dfa.transitions if k[0]==state_name or self.dfa.transitions[k]==state_name]
            for k in to_remove:
                del self.dfa.transitions[k]
            if self.dfa.current_state == state_name:
                self.dfa.current_state = None

    def delete_transition(self, transition_key):
        from_state, symbol, to_state = transition_key
        key = (from_state, symbol)
        if key in self.dfa.transitions and self.dfa.transitions[key] == to_state:
            del self.dfa.transitions[key]

    def redraw_dfa(self):
        self.canvas.delete("all")

        # ─── Draw transitions ───────────────────────────────────────────────────
        transitions_by_pair = {}
        for (from_state, symbol), to_state in self.dfa.transitions.items():
            transitions_by_pair.setdefault((from_state, to_state), []).append(symbol)

        for (from_state, to_state), symbols in transitions_by_pair.items():
            label = ",".join(symbols)
            from_x, from_y, _, _ = self.dfa.states[from_state]
            to_x,   to_y,   _, _ = self.dfa.states[to_state]

            if from_state == to_state:
                # Self-loop
                end_x = from_x + self.state_radius
                end_y = from_y - self.state_radius - 5
                self.canvas.create_line(
                    from_x - self.state_radius, from_y - self.state_radius - 5,
                    from_x - 40,             from_y - 80,
                    from_x + 40,             from_y - 80,
                    end_x,                   end_y,
                    fill="black", width=2, smooth=True
                )
                # Arrowhead
                arrow_size = 10
                angle = math.radians(30)
                dx_back = -arrow_size * math.cos(angle)
                dx_side =  arrow_size * math.sin(angle)
                self.canvas.create_polygon(
                    end_x, end_y,
                    end_x + dx_back +  dx_side, end_y - dx_side,
                    end_x + dx_back -  dx_side, end_y + dx_side,
                    fill="black"
                )
                # Label
                self.canvas.create_text(from_x, from_y - 65, text=label, font=("Arial", 10))

            else:
                # Straight single transition
                dx, dy = to_x - from_x, to_y - from_y
                dist = math.hypot(dx, dy) or 1
                ux, uy = dx/dist, dy/dist

                start_x = from_x + ux * self.state_radius
                start_y = from_y + uy * self.state_radius
                end_x   = to_x   - ux * self.state_radius
                end_y   = to_y   - uy * self.state_radius

                # Draw line
                ctrl_x, ctrl_y = (start_x + end_x)/2, (start_y + end_y)/2
                self.canvas.create_line(
                    start_x, start_y,
                    ctrl_x,   ctrl_y,
                    end_x,    end_y,
                    fill="black", width=2, smooth=True
                )

                # Arrowhead
                arrow_size = 10
                angle = math.radians(30)
                dx_back = -ux * arrow_size * math.cos(angle)
                dy_back = -uy * arrow_size * math.cos(angle)
                dx_side =  uy * arrow_size * math.sin(angle)
                dy_side = -ux * arrow_size * math.sin(angle)
                self.canvas.create_polygon(
                    end_x, end_y,
                    end_x + dx_back + dx_side, end_y + dy_back + dy_side,
                    end_x + dx_back - dx_side, end_y + dy_back - dy_side,
                    fill="black"
                )

                # Label above midpoint
                offset = 5
                lx = ctrl_x + uy * offset
                ly = ctrl_y - ux * offset
                self.canvas.create_text(lx, ly, text=label, font=("Arial", 10))

        # ─── Draw states ─────────────────────────────────────────────────────────
        for state, (x, y, is_start, is_accept) in self.dfa.states.items():
            # Highlight current in simulate
            if self.mode == "simulate" and state == self.dfa.current_state:
                self.canvas.create_oval(
                    x - self.state_radius - 5, y - self.state_radius - 5,
                    x + self.state_radius + 5, y + self.state_radius + 5,
                    fill="yellow", outline="yellow"
                )
            color = ("green" if state == self.selected_state
                     else "red" if state == self.dfa.current_state
                     else "blue")
            self.canvas.create_oval(
                x - self.state_radius, y - self.state_radius,
                x + self.state_radius, y + self.state_radius,
                outline=color, width=2
            )
            if is_accept:
                self.canvas.create_oval(
                    x - self.state_radius + 5, y - self.state_radius + 5,
                    x + self.state_radius - 5, y + self.state_radius - 5,
                    outline=color, width=2
                )
            if is_start:
                arrow_len = 20
                self.canvas.create_line(
                    x - self.state_radius - arrow_len, y,
                    x - self.state_radius, y,
                    fill="black", width=2
                )
                self.canvas.create_polygon(
                    x - self.state_radius, y,
                    x - self.state_radius - 5, y - 5,
                    x - self.state_radius - 5, y + 5,
                    fill="black"
                )
            self.canvas.create_text(x, y, text=state, font=("Arial", 12))

    def handle_input_entry(self, event):
        if self.mode == "simulate":
            self.input_string = self.input_entry.get()
            self.current_symbol_index = 0
            self.dfa.reset()
            self.redraw_dfa()
            self.status_label.config(text="Mode: Simulate")

    def canvas_drag(self, event):
        if getattr(self, 'dragging_state', None) and self.action_mode == "":
            x, y = event.x, event.y
            dx = x - self.drag_start_x
            dy = y - self.drag_start_y
            old_x, old_y, is_start, is_accept = self.dfa.states[self.dragging_state]
            self.dfa.states[self.dragging_state] = (old_x + dx, old_y + dy, is_start, is_accept)
            self.drag_start_x, self.drag_start_y = x, y
            self.redraw_dfa()

    def canvas_release(self, event):
        if getattr(self, 'dragging_state', None) and self.action_mode == "":
            self.dragging_state = None
            self.redraw_dfa()
            self.status_label.config(text="Mode: Define DFA")

    def step_simulation(self):
        if self.mode != "simulate":
            self.mode = "simulate"
            self.input_string = self.input_entry.get()
            self.current_symbol_index = 0
            self.dfa.reset()
            self.status_label.config(text="Mode: Simulate")

        if self.current_symbol_index < len(self.input_string):
            symbol = self.input_string[self.current_symbol_index]
            if self.dfa.process_input(symbol):
                self.current_symbol_index += 1
                self.status_label.config(text=f"Processed '{symbol}', current state: {self.dfa.current_state}")
            else:
                self.status_label.config(text=f"No transition for '{symbol}' from {self.dfa.current_state} - Invalid Input")
            self.redraw_dfa()
        else:
            final = self.dfa.current_state
            valid = "Valid" if self.dfa.is_accepting_state(final) else "Invalid"
            self.status_label.config(text=f"Input processed, final state: {final} - {valid} Input")

    def reset_dfa(self):
        self.dfa.reset()
        self.input_string = ""
        self.current_symbol_index = 0
        self.mode = "define"
        self.selected_state = None
        self.transition_from = None
        self.action_mode = ""
        self.input_entry.delete(0, tk.END)
        self.redraw_dfa()
        self.status_label.config(text="Mode: Define DFA")

if __name__ == "__main__":
    root = tk.Tk()
    app = DFAVisualizer(root)
    root.mainloop()
