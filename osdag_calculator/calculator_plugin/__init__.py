from PyQt5 import QtWidgets, QtCore, QtGui
from math import sqrt, sin, cos, tan, radians

class CalculatorWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator")
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        self.setFixedSize(420, 580)
        self.setup_ui()
        self.setup_buttons()
        self.current_input = ''
        self.stored_value = 0
        self.current_operation = None
        self.should_clear = False
        self.decimal_added = False
        
    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(10, 5, 10, 10)
        
        self.display = QtWidgets.QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(QtCore.Qt.AlignRight)
        self.display.setMaxLength(20)  
        font = self.display.font()
        font.setPointSize(26)  
        font.setBold(True)
        self.display.setFont(font)
        self.display.setMinimumHeight(60)  
        self.display.setStyleSheet('''
            QLineEdit {
                background-color: white; 
                border: 2px solid #aaa; 
                border-radius: 8px; 
                padding: 10px 15px;
                color: #333;
                margin-bottom: 5px;
            }
        ''')
        
        self.memory_display = QtWidgets.QLabel('')
        self.memory_display.setAlignment(QtCore.Qt.AlignRight)
        memory_font = self.memory_display.font()
        memory_font.setPointSize(11)
        self.memory_display.setFont(memory_font)
        self.memory_display.setStyleSheet('''
            color: #555; 
            font-weight: bold;
            margin-bottom: 2px;
            padding: 0 5px;
        ''')
        self.memory_display.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.buttons_layout = QtWidgets.QGridLayout()
        self.buttons_layout.setSpacing(6)  # Slightly reduced spacing
        
        self.layout.addWidget(self.memory_display)
        self.layout.addWidget(self.display)
        self.layout.addLayout(self.buttons_layout)
        
    def setup_buttons(self):
        buttons = [
            ('C', 1, 0, 1, 1, ''),
            ('±', 1, 1, 1, 1, ''),
            ('%', 1, 2, 1, 1, ''),
            ('÷', 1, 3, 1, 1, ''),
            
            ('7', 2, 0, 1, 1, ''),
            ('8', 2, 1, 1, 1, ''),
            ('9', 2, 2, 1, 1, ''),
            ('×', 2, 3, 1, 1, ''),
            
            ('4', 3, 0, 1, 1, ''),
            ('5', 3, 1, 1, 1, ''),
            ('6', 3, 2, 1, 1, ''),
            ('-', 3, 3, 1, 1, ''),
            
            ('1', 4, 0, 1, 1, ''),
            ('2', 4, 1, 1, 1, ''),
            ('3', 4, 2, 1, 1, ''),
            ('+', 4, 3, 1, 1, ''),
            
            ('0', 5, 0, 1, 2, ''),
            ('.', 5, 2, 1, 1, ''),
            ('=', 5, 3, 1, 1, ''),
            
            ('sin', 0, 0, 1, 1, ''),
            ('cos', 0, 1, 1, 1, ''),
            ('tan', 0, 2, 1, 1, ''),
            ('√', 0, 3, 1, 1, ''),
            
            ('π', 6, 0, 1, 1, ''),
            ('x²', 6, 1, 1, 1, ''),
            ('1/x', 6, 2, 1, 1, ''),
            ('⌫', 6, 3, 1, 1, ''),
        ]
        
        for btn_text, row, col, row_span, col_span, style in buttons:
            button = QtWidgets.QPushButton(btn_text)
            button.setMinimumSize(60, 60)
            button.setStyleSheet('''
                QPushButton {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    padding: 10px;
                    font-size: 18px;
                    font-weight: normal;
                    margin: 2px;
                    color: #212529;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
                }
            ''')
            button.clicked.connect(self.on_button_click)
            self.buttons_layout.addWidget(button, row, col, row_span, col_span)
    
    def on_button_click(self):
        button = self.sender()
        text = button.text()
        
        if text.isdigit() or text == '.':
            self.handle_digit_or_decimal(text)
        elif text in ['+', '-', '×', '÷']:
            self.handle_operation(text)
        elif text == '=':
            self.calculate_result()
        elif text == 'C':
            self.clear_all()
        elif text == '⌫':
            self.backspace()
        elif text == '±':
            self.toggle_sign()
        elif text == '%':
            self.percentage()
        elif text == '√':
            self.square_root()
        elif text == 'x²':
            self.square()
        elif text == '1/x':
            self.reciprocal()
        elif text == 'π':
            self.add_pi()
        elif text in ['sin', 'cos', 'tan']:
            self.trig_function(text)
    
    def handle_digit_or_decimal(self, text):
        if self.should_clear:
            self.current_input = ''
            self.should_clear = False
            
        if text == '.':
            if not self.decimal_added:
                if not self.current_input:
                    self.current_input = '0.'
                else:
                    self.current_input += '.'
                self.decimal_added = True
        else:
            if self.current_input == '0' and text == '0':
                return
            if self.current_input == '0':
                self.current_input = text
            else:
                self.current_input += text
                
        self.display.setText(self.current_input)
    
    def handle_operation(self, op):
        if self.current_input:
            if self.current_operation:
                self.calculate_result()
            self.stored_value = float(self.current_input)
            self.current_operation = op
            self.memory_display.setText(f"{self.stored_value} {op}")
            self.should_clear = True
            self.decimal_added = False
    
    def calculate_result(self):
        if not self.current_operation or not self.current_input:
            return
            
        current_value = float(self.current_input)
        result = 0
        
        if self.current_operation == '+':
            result = self.stored_value + current_value
        elif self.current_operation == '-':
            result = self.stored_value - current_value
        elif self.current_operation == '×':
            result = self.stored_value * current_value
        elif self.current_operation == '÷':
            if current_value == 0:
                self.display.setText("Error")
                self.current_input = ''
                self.current_operation = None
                return
            result = self.stored_value / current_value
        
        if result.is_integer():
            result = int(result)
            
        self.display.setText(str(result))
        self.current_input = str(result)
        self.current_operation = None
        self.memory_display.clear()
        self.should_clear = True
    
    def clear_all(self):
        self.current_input = '0'
        self.stored_value = 0
        self.current_operation = None
        self.should_clear = False
        self.decimal_added = False
        self.display.setText('0')
        self.memory_display.clear()
    
    def backspace(self):
        if len(self.current_input) > 0:
            if self.current_input[-1] == '.':
                self.decimal_added = False
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = '0'
            self.display.setText(self.current_input)
    
    def toggle_sign(self):
        if self.current_input and self.current_input != '0':
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display.setText(self.current_input)
    
    def percentage(self):
        if self.current_input:
            value = float(self.current_input) / 100
            if value.is_integer():
                value = int(value)
            self.current_input = str(value)
            self.display.setText(self.current_input)
    
    def square_root(self):
        if self.current_input:
            try:
                value = float(self.current_input)
                if value < 0:
                    self.display.setText("Error")
                    return
                result = sqrt(value)
                if result.is_integer():
                    result = int(result)
                self.current_input = str(result)
                self.display.setText(self.current_input)
            except:
                self.display.setText("Error")
    
    def square(self):
        if self.current_input:
            value = float(self.current_input)
            result = value ** 2
            if result.is_integer():
                result = int(result)
            self.current_input = str(result)
            self.display.setText(self.current_input)
    
    def reciprocal(self):
        if self.current_input and self.current_input != '0':
            try:
                value = float(self.current_input)
                if value == 0:
                    self.display.setText("Error")
                    return
                result = 1 / value
                if result.is_integer():
                    result = int(result)
                self.current_input = str(result)
                self.display.setText(self.current_input)
            except:
                self.display.setText("Error")
    
    def add_pi(self):
        self.current_input = str(3.14159265359)
        self.display.setText(self.current_input)
    
    def trig_function(self, func):
        if self.current_input:
            try:
                value = radians(float(self.current_input))
                if func == 'sin':
                    result = sin(value)
                elif func == 'cos':
                    result = cos(value)
                elif func == 'tan':
                    if cos(value) == 0:
                        self.display.setText("Error")
                        return
                    result = tan(value)
                
                if abs(result) < 1e-10:
                    result = 0
                
                if result.is_integer():
                    result = int(result)
                
                self.current_input = str(result)
                self.display.setText(self.current_input)
            except:
                self.display.setText("Error")

class ScientificCalculatorPlugin:
    def __init__(self):
        self.name = 'Scientific Calculator'
        self.version = '2.0.0'
        self.description = 'A full-featured scientific calculator with basic and advanced functions'
        self.author = 'Aathithya Sharan'
        self.widget = None
    
    def register(self):
        self.widget = CalculatorWidget()
        self.widget.show()
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author
        }
    
    def deactivate(self):
        if self.widget:
            self.widget.close()
            self.widget = None

plugin_class = ScientificCalculatorPlugin
