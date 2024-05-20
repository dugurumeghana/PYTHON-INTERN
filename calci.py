import tkinter as tk
from tkinter import messagebox
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        self.geometry("400x600")
        
        # Create a StringVar to hold the expression to be evaluated
        self.expression = ""
        self.input_text = tk.StringVar()
        
        # Memory
        self.memory = 0
        
        self.create_widgets()

    def create_widgets(self):
        # Entry widget for the input expression
        input_frame = tk.Frame(self, bd=5, relief=tk.RIDGE)
        input_frame.pack(side=tk.TOP)
        
        input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self, bd=5, relief=tk.RIDGE)
        buttons_frame.pack()

        # Button layout
        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'M+',
            '1', '2', '3', '-', 'M-',
            '0', '.', '=', '+', 'MR',
            'sqrt', '^', '(', ')', 'MC'
        ]
        
        row_val = 0
        col_val = 0

        for button in buttons:
            if col_val > 4:
                col_val = 0
                row_val += 1
            
            self.create_button(button, buttons_frame, row_val, col_val)
            col_val += 1

    def create_button(self, value, frame, row, col):
        button = tk.Button(frame, text=value, font=('arial', 18), fg="black", width=9, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click(value))
        button.grid(row=row, column=col, padx=1, pady=1)

    def on_button_click(self, value):
        if value == 'C':
            self.expression = ""
            self.input_text.set("")
        elif value == '=':
            try:
                result = str(self.evaluate_expression(self.expression))
                self.input_text.set(result)
                self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot divide by zero")
                self.expression = ""
                self.input_text.set("")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.expression = ""
                self.input_text.set("")
        elif value == 'sqrt':
            try:
                result = str(math.sqrt(self.evaluate_expression(self.expression)))
                self.input_text.set(result)
                self.expression = result
            except ValueError:
                messagebox.showerror("Error", "Invalid Input for Square Root")
                self.expression = ""
                self.input_text.set("")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.expression = ""
                self.input_text.set("")
        elif value == '^':
            self.expression += '**'
            self.input_text.set(self.expression)
        elif value == 'M+':
            try:
                self.memory += self.evaluate_expression(self.expression)
                self.expression = ""
                self.input_text.set("")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif value == 'M-':
            try:
                self.memory -= self.evaluate_expression(self.expression)
                self.expression = ""
                self.input_text.set("")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif value == 'MR':
            self.input_text.set(str(self.memory))
            self.expression = str(self.memory)
        elif value == 'MC':
            self.memory = 0
            self.expression = ""
            self.input_text.set("")
        else:
            self.expression += value
            self.input_text.set(self.expression)

    def evaluate_expression(self, expression):
        """ Custom expression evaluator to replace eval """
        try:
            # Split expression into tokens
            tokens = self.tokenize(expression)
            # Convert infix expression to postfix
            postfix = self.infix_to_postfix(tokens)
            # Evaluate postfix expression
            return self.evaluate_postfix(postfix)
        except Exception as e:
            raise ValueError("Invalid Expression")

    def tokenize(self, expression):
        """ Tokenize the expression into numbers and operators """
        tokens = []
        current_num = ''
        for char in expression:
            if char in '0123456789.':
                current_num += char
            else:
                if current_num:
                    tokens.append(current_num)
                    current_num = ''
                if char in '+-*/()^':
                    tokens.append(char)
        if current_num:
            tokens.append(current_num)
        return tokens

    def infix_to_postfix(self, tokens):
        """ Convert infix expression to postfix notation """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output = []
        stack = []
        for token in tokens:
            if token.isnumeric() or '.' in token:
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # pop '('
            else:
                while stack and precedence.get(token, 0) <= precedence.get(stack[-1], 0):
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def evaluate_postfix(self, postfix):
        """ Evaluate the postfix expression """
        stack = []
        for token in postfix:
            if token.isnumeric() or '.' in token:
                stack.append(float(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        return stack[0]

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
