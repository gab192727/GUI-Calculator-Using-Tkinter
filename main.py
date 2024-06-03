import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from math import factorial, sqrt
from re import findall, sub
from sympy import sympify


class Calculator:
    def __init__(self):
      
        # Initialize the main window.
        self.root = tk.Tk()
        self.font = font.Font(family='Times_New_Roman')
      
        # Change the path based on the location of the image you want to add as an icon.
        self.image_path_icon = "Calculator-icon.png"
        self.icon = ImageTk.PhotoImage(Image.open(self.image_path_icon))
        self.root.iconphoto(False, self.icon)

        # Set window title and size
        self.root.title("Calculator")
        self.root.geometry("575x525")
        self.root.resizable(True, True)

        # Define font sizes and colors
        self.small_fs = (self.font, 15)
        self.large_fs = (self.font, 30, "bold")
        self.digit_font = (self.font, 20)
        self.default_font = (self.font, 18)
        self.last_answer_font = (self.font, 15)

        self.operation_color = '#E4E6E5'
        self.last_ans_label_color = '#708090'
        self.text_label_color = "black"
        self.label_color = "#FAFAFA"
        self.equal_color = "#97EBF4"
        self.bg_color = '#F8FAFF'
      
        # Initialize expressions and states
        self.current_expression = ''
        self.full_expression = ''
        self.copy_expression = ''
        self.copy_last_expression = ''
        self.evaluated = False
        self.subscript = False
        count_of_r_and_c = 5

        # Mapping for superscript characters
        self.superscript_map = {'0': '\u2070', '1': '\u00B9', '2': '\u00B2', '3': '\u00B3', '4': '\u2074',
                                '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079'}
      
        # Button configurations
        self.digit_buttons = (("7", 1, 1), ("8", 1, 2), ("9", 1, 3), ("4", 2, 1), ("5", 2, 2), ("6", 2, 3),
                              ("1", 3, 1), ("2", 3, 2), ("3", 3, 3), ("0", 4, 1), (".", 4, 2))
        self.operations = (("(", "(", 0, 1), (")", ")", 0, 2), ("/ 100", "%", 0, 0),  ("/", "\u00F7", 1, 4),
                           ("*", "\u00D7", 2, 4), ("-", "-", 3, 4), ("+", "+", 4, 4))
        self.special_button = (('AC', 0, 4, self.clear_all), ("CE", 0, 3, self.clear_entry),
                               ('Ans', 4, 0, self.get_last_answer))
        self.equal_button = ('=', 4, 3)
        self.special_operator_buttons = (("ⁿ√", 1, 0, lambda x='√': self.root_to_n(x)),
                                         ('xⁿ', 2, 0, lambda x='^': self.raise_to_n(x)),
                                         ('n!', 3, 0, lambda x='!': self.factorial_n(x)))

        self.pattern = r'(\+|\-|\*|\/|√|\^|!|\(|\)|\d+\.?\d*)'
        # Create display labels
        self.last_answer_label = self.make_last_answer_display()
        self.full_label, self.current_label = self.make_display_label()
      
        # Create button frame and configure buttons
        self.button_frame = self.make_button_frame()
        self.button_configure(count_of_r_and_c)
        self.make_digit_buttons()
        self.make_operation_buttons()
        self.make_special_button()
        self.make_special_operator_buttons()
        self.make_equal_button()

        # Bind keys to functions
        self.bind_keys()

    # Create button frame
    def make_button_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill='both')
        return frame
      
    # Create display labels for current and full expression
    def make_display_label(self):
        frame = tk.Frame(self.root, height=200, bg=self.label_color)
        frame.pack(expand=True, fill='both')
        current_label = tk.Label(frame, text=self.current_expression, bg=self.label_color, fg=self.text_label_color, padx=18,
                                 font=self.last_answer_font, anchor=tk.E, pady=4)
        current_label.pack(expand=True, fill='both')
        full_label = tk.Label(frame, text=self.full_expression, bg=self.label_color, fg=self.text_label_color, padx=18,
                              font=self.large_fs,  anchor=tk.E, pady=4)
        full_label.pack(expand=True, fill='both')
        return current_label, full_label

    # Create last answer display label
    def make_last_answer_display(self):
        last_answer_label = tk.Label(self.root, text="", bg=self.label_color, fg=self.last_ans_label_color,
                                     font=(self.font, 15), anchor=tk.E, padx=10)
        last_answer_label.pack(side=tk.TOP, fill=tk.X)
        return last_answer_label

    # Create digit buttons
    def make_digit_buttons(self):
        for digit, row, column in self.digit_buttons:
            button = tk.Button(self.button_frame, text=digit, bg=self.bg_color, fg=self.text_label_color,
                               font=self.digit_font, borderwidth=0, command=lambda x=digit: self.append_digit(x))
            button.grid(row=row, column=column, sticky=tk.NSEW, padx=4, pady=4)
            self.add_hover_effect(button, self.bg_color, '#CCCCCC')

    # Create operation buttons
    def make_operation_buttons(self):
        for operator, display, row, column in self.operations:
            button = tk.Button(self.button_frame, text=display, bg=self.operation_color, fg=self.text_label_color,
                               font=self.default_font, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=row, column=column, sticky=tk.NSEW, padx=4, pady=4)
            self.add_hover_effect(button, self.operation_color, '#CCCCCC')
    # Create special buttons (AC, CE, Ans)
    def make_special_button(self):
        for display, row, column, command in self.special_button:
            button = tk.Button(self.button_frame, text=display, bg=self.operation_color,
                               fg=self.text_label_color, font=self.default_font, borderwidth=0, command=command)
            button.grid(row=row, column=column, sticky=tk.NSEW, padx=4, pady=4)
            self.add_hover_effect(button, self.operation_color, '#CCCCCC')

    # Create special operator buttons (√, ^, !)
    def make_special_operator_buttons(self):
        for display, row, column, command in self.special_operator_buttons:
            button = tk.Button(self.button_frame, text=display, bg=self.operation_color,
                               fg=self.text_label_color, font=self.default_font, borderwidth=0, command=command)
            button.grid(row=row, column=column, sticky=tk.NSEW, padx=4, pady=4)
            self.add_hover_effect(button, self.operation_color, '#CCCCCC')
    
    # Create equal button
    def make_equal_button(self):
        button = tk.Button(self.button_frame, text=self.equal_button[0], bg=self.equal_color, fg=self.text_label_color,
                           font=self.default_font, borderwidth=0,  command=self.evaluate)
        button.grid(row=self.equal_button[1], column=self.equal_button[2], sticky=tk.NSEW, padx=4, pady=4)
        self.add_hover_effect(button, self.equal_color, '#3B9EBF')

    # Configure button grid
    def button_configure(self, n):
        for x in range(n):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)

    # Update full expression label
    def update_full_label(self):
        expression = self.full_expression
        for operator, display, row, column in self.operations:
            expression = expression.replace(operator, f' {display} ')
        self.full_label.config(text=expression)

    # Update current expression label
    def update_current_label(self):
        self.current_label.config(text=self.current_expression[:24])

    # Append digit to current expression
    def append_digit(self, digit):
        if "Error" in self.current_expression:
            self.current_expression = ''
        self.current_expression += str(digit)
        if self.subscript:
            for key, value in self.superscript_map.items():
                self.current_expression = self.current_expression.replace(key, value)
        self.update_current_label()

    # Append operator to full expression
    def append_operator(self, operation):
        self.subscript = False
        self.evaluated = False
        if "Error" in self.current_expression:
            self.error_check()
            return
        if self.evaluated:
            self.full_expression = ''
        self.full_expression += self.current_expression + operation
        self.current_expression = ''
        self.update_full_label()
        self.update_current_label()

    # Clear all expressions
    def clear_all(self):
        self.evaluated = False
        self.subscript = False
        self.current_expression = ''
        self.full_expression = ''
        self.update_full_label()
        self.update_current_label()

    # Clear current entry
    def clear_entry(self):
        if "Error" in self.current_expression:
            self.error_check()
            return
        # This condition will clear the current ecpression at the current expression label first.
        # If the current label expression is empty, clear the full expression at the full expression label
        if len(self.current_expression) == 0:
            self.full_expression = self.full_expression[:-1]
            self.update_full_label()
          
        # this will clear all of the digits in the current label if you click the equal button
        elif self.evaluated:
            self.full_expression = self.copy_expression[:-1]
            self.current_expression = ''
            self.update_full_label()
            self.update_current_label()
        else:
            self.current_expression = self.current_expression[:-1]
            self.update_current_label()
        self.evaluated = False

    # Evaluate the full expression
    def evaluate(self):
        self.evaluated = True
        self.full_expression += self.current_expression
        self.update_full_label()
        try:
            full_expression = self.full_expression
            # convert the subscripted value into the original numerical value
            for key, value in self.superscript_map.items():
                full_expression = full_expression.replace(value, key)

            # convert ^ to **
            full_expression = full_expression.replace('^', '**')

            # make the full expression into a list with the use of re
            full_expression = sub(r'(\d)(\()', r'\1*\2', full_expression)
            components = findall(self.pattern, full_expression)
          
            # evaluate factorial and square root first
            components = self.evaluate_factorial(components)
            components = self.evaluate_sqrt(components)

            # turn the list into a string
            result = ''.join(components)
            self.current_expression = str(round(sympify(result), 8))
          
            # strip all of the zeros in the decimal place of the final expression 
            if '.' in self.current_expression:
                self.current_expression = self.current_expression.rstrip('0').rstrip('.')
              
            # copy the answer that will be displayed in the last answer label
            self.copy_last_expression = self.current_expression
            self.last_answer_label.config(text=f"Ans: {self.copy_last_expression}")
            # the result of the evalued full expression will be put into the current expression and the full expression will be set to ''
            self.copy_expression = self.full_expression
            self.full_expression = ''
          
        # handle different error
        except SyntaxError:
            self.current_expression = "Syntax Error"
        except ZeroDivisionError:
            self.current_expression = "Zero Division Error"
        except OverflowError:
            self.current_expression = 'Overflow Error'
        except ValueError:
            self.current_expression = "Value Error"
        finally:
            self.update_current_label()

    # this function will evaluate all of the factorial symbol that you add 
    @staticmethod
    def evaluate_factorial(expression):
        if '!' not in expression:
            return expression

        i = 0
        while i < len(expression):
            if expression[i] == '!':
                expression[i - 1] = str(factorial(int(expression[i - 1])))
                del expression[i]
            else:
                i += 1
        return expression

    # similar to the evaluate sqrt, this will first reverse the expression then evaluate all of the expression then reverase it again
    # sounds bad but this is the only solution i found that can evaluate all of the sqrt in the expression
    @staticmethod
    def evaluate_sqrt(expression):
        if '√' not in expression:
            return expression
        expression.reverse()
        i = 0
        while i < len(expression):
            if expression[i] == '√':
                expression[i - 1] = str(sqrt(float(expression[i - 1])))
                del expression[i]
            else:
                i += 1
        expression.reverse()
        return expression

    # square root* will make changes in the future. Append square root to full expression
    def root_to_n(self, n):
        self.subscript = False
        if "Error" in self.current_expression:
            self.error_check()
            return
        self.full_expression += f'{n}{self.current_expression}'
        self.current_expression = ''
        self.update_full_label()
        self.update_current_label()

    # Append exponent to full expression
    def raise_to_n(self, x):
        if "Error" in self.current_expression:
            self.error_check()
            return
        self.subscript = True
        self.full_expression += f'{self.current_expression}{x}'
        self.current_expression = ''
        self.update_current_label()
        self.update_full_label()

    # Append factorial to current expression
    def factorial_n(self, x):
        self.subscript = False
        if "Error" in self.current_expression:
            self.error_check()
            return
        self.current_expression = f'{self.current_expression}{x}'
        self.full_expression += self.current_expression
        self.current_expression = ''
        self.update_full_label()
        self.update_current_label()

    # Get last answer
    def get_last_answer(self):
        self.subscript = False
        if not self.evaluated:
            self.current_expression += self.copy_last_expression
            self.update_current_label()

    # Handle errors
    def error_check(self):
        self.copy_expression = ''
        self.current_expression = ''
        self.update_current_label()

    # Bind keyboard keys to the digit and simple operator buttons
    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.evaluate())

        for operator, display, row, column in self.operations:
            self.root.bind(operator, lambda event, x=operator: self.append_operator(x))

        for digit, row, column in self.digit_buttons:
            self.root.bind(digit, lambda event, x=digit: self.append_digit(x))

    # Add hover effect to buttons 
    @staticmethod
    def add_hover_effect(button, original_color, hover_color):
        button.bind("<Enter>", lambda event, btn=button: btn.config(bg=hover_color))
        button.bind("<Leave>", lambda event, btn=button: btn.config(bg=original_color))

    # Run the main loop
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    c = Calculator()
    c.run()
