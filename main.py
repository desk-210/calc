from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from plyer import vibrator
from kivy.uix.label import Label

class Calculator(BoxLayout):
    expression = StringProperty("0")
    history = ListProperty([])
    dark_theme = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._swipe_threshold = 50
        # For haptic feedback: we'll call vibrate() on button press

    def on_kv_post(self, base_widget):
        self.update_history_ui()

    def update_history_ui(self):
        if hasattr(self, 'ids') and 'history_list' in self.ids:
            history_box = self.ids.history_list
            history_box.clear_widgets()
            for entry in self.history:
                history_box.add_widget(Label(text=entry, size_hint_y=None, height=30, color=(0.7, 0.7, 0.7, 1), font_size='14sp'))

    def add_character(self, char):
        if char == 'C':
            self.expression = "0"
        elif char == '⌫':
            if len(self.expression) == 1 or (len(self.expression) == 2 and self.expression[0] == '-' and self.expression[1] != '0'):
                self.expression = "0"
            else:
                self.expression = self.expression[:-1]
                if self.expression == "":
                    self.expression = "0"
        elif char == '=':
            self.calculate()
        else:
            if self.expression == "0":
                self.expression = char
            else:
                self.expression += char

    def calculate(self):
        try:
            allowed = set("0123456789+-*/.()")
            if all(c in allowed for c in self.expression):
                result = eval(self.expression)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                result_str = str(result)
                self.history.insert(0, f"{self.expression} = {result_str}")
                if len(self.history) > 10:
                    self.history.pop()
                self.expression = result_str
                self.update_history_ui()
            else:
                raise Exception
        except Exception:
            self.expression = "Error"
            Clock.schedule_once(lambda dt: setattr(self, 'expression', "0"), 1)

    def clear_history(self):
        self.history = []
        self.update_history_ui()

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme

    def vibrate(self):
        try:
            vibrator.vibrate(0.05)
        except:
            pass

class CalculatorApp(App):
    def build(self):
        return Calculator()

if __name__ == '__main__':
    CalculatorApp().run()