import math

def get_number(prompt):
    """Get a valid number (integer or float) from user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input == "":
                print("Please enter a valid number.")
                continue
            
            # Try to convert to float first (handles both int and float)
            number = float(user_input)
            return number
        except ValueError:
            print("Invalid input! Please enter a valid number (integer or decimal).")

def get_operation():
    """Get operation choice from user"""
    operations = {
        'add': '+', 'addition': '+', 'plus': '+',
        'subtract': '-', 'subtraction': '-', 'minus': '-',
        'multiply': '*', 'multiplication': '*', 'times': '*',
        'divide': '/', 'division': '/',
        'power': '**', 'exponent': '**', 'raise': '**',
        'modulo': '%', 'mod': '%', 'remainder': '%',
        'floor_divide': '//', 'integer_divide': '//',
        'sqrt': 'sqrt', 'square_root': 'sqrt',
        'sin': 'sin', 'sine': 'sin',
        'cos': 'cos', 'cosine': 'cos',
        'tan': 'tan', 'tangent': 'tan',
        'log': 'log', 'logarithm': 'log',
        'ln': 'ln', 'natural_log': 'ln',
        'abs': 'abs', 'absolute': 'abs',
        'ceil': 'ceil', 'ceiling': 'ceil',
        'floor': 'floor'
    }
    
    print("\nAvailable operations:")
    print("Basic Operations: add, subtract, multiply, divide")
    print("Advanced Operations: power, modulo, floor_divide")
    print("Single Number Operations: sqrt, sin, cos, tan, log, ln, abs, ceil, floor")
    print("(You can also use synonyms like: plus, minus, times, etc.)")
    
    while True:
        operation = input("\nEnter operation name: ").strip().lower()
        
        if operation in operations:
            return operations[operation]
        else:
            print("Invalid operation! Please enter a valid operation name.")
            print("Examples: add, subtract, multiply, divide, power, sqrt, etc.")

def perform_calculation(num1, num2, operation):
    """Perform the calculation based on operation"""
    try:
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                return "Error: Division by zero is not allowed!"
            return num1 / num2
        elif operation == '**':
            return num1 ** num2
        elif operation == '%':
            if num2 == 0:
                return "Error: Division by zero is not allowed!"
            return num1 % num2
        elif operation == '//':
            if num2 == 0:
                return "Error: Division by zero is not allowed!"
            return num1 // num2
        else:
            return "Error: Invalid operation!"
    except OverflowError:
        return "Error: Result too large!"
    except Exception as e:
        return f"Error: {str(e)}"

def perform_single_operation(num, operation):
    """Perform single number operations"""
    try:
        if operation == 'sqrt':
            if num < 0:
                return "Error: Cannot calculate square root of negative number!"
            return math.sqrt(num)
        elif operation == 'sin':
            return math.sin(math.radians(num))  # Convert to radians
        elif operation == 'cos':
            return math.cos(math.radians(num))
        elif operation == 'tan':
            return math.tan(math.radians(num))
        elif operation == 'log':
            if num <= 0:
                return "Error: Cannot calculate logarithm of non-positive number!"
            return math.log10(num)
        elif operation == 'ln':
            if num <= 0:
                return "Error: Cannot calculate natural logarithm of non-positive number!"
            return math.log(num)
        elif operation == 'abs':
            return abs(num)
        elif operation == 'ceil':
            return math.ceil(num)
        elif operation == 'floor':
            return math.floor(num)
        else:
            return "Error: Invalid single operation!"
    except Exception as e:
        return f"Error: {str(e)}"

def format_number(num):
    """Format number for display (remove unnecessary decimals)"""
    if isinstance(num, float) and num.is_integer():
        return int(num)
    elif isinstance(num, float):
        return round(num, 10)  # Round to 10 decimal places to avoid floating point errors
    return num

def calculator():
    """Main calculator function"""
    print("=" * 50)
    print("         COMPREHENSIVE CALCULATOR")
    print("=" * 50)
    print("This calculator supports:")
    print("• Any digit numbers (integers and decimals)")
    print("• Basic operations: addition, subtraction, multiplication, division")
    print("• Advanced operations: power, modulo, floor division")
    print("• Mathematical functions: sqrt, sin, cos, tan, log, ln, abs, ceil, floor")
    print("• Type 'quit' or 'exit' to stop")
    print("=" * 50)
    
    while True:
        try:
            print("\n" + "-" * 30)
            
            # Check if user wants to quit
            first_input = input("Enter first number (or 'quit' to exit): ").strip().lower()
            if first_input in ['quit', 'exit']:
                print("Thank you for using the calculator!")
                break
            
            # Get first number
            try:
                num1 = float(first_input)
            except ValueError:
                print("Invalid input! Please enter a valid number.")
                continue
            
            # Get operation
            operation = get_operation()
            
            # Check if it's a single number operation
            single_ops = ['sqrt', 'sin', 'cos', 'tan', 'log', 'ln', 'abs', 'ceil', 'floor']
            
            if operation in single_ops:
                # Single number operation
                result = perform_single_operation(num1, operation)
                
                if isinstance(result, str):  # Error message
                    print(f"\n{result}")
                else:
                    formatted_result = format_number(result)
                    print(f"\nResult: {operation}({format_number(num1)}) = {formatted_result}")
            else:
                # Two number operation
                num2 = get_number("Enter second number: ")
                result = perform_calculation(num1, num2, operation)
                
                if isinstance(result, str):  # Error message
                    print(f"\n{result}")
                else:
                    formatted_result = format_number(result)
                    operation_names = {
                        '+': 'addition',
                        '-': 'subtraction', 
                        '*': 'multiplication',
                        '/': 'division',
                        '**': 'power',
                        '%': 'modulo',
                        '//': 'floor division'
                    }
                    op_name = operation_names.get(operation, operation)
                    print(f"\nResult: {format_number(num1)} {operation} {format_number(num2)} = {formatted_result}")
                    print(f"Operation: {op_name}")
            
            # Ask if user wants to continue
            continue_calc = input("\nDo you want to perform another calculation? (yes/no): ").strip().lower()
            if continue_calc not in ['yes', 'y', 'yeah', 'yep']:
                print("Thank you for using the calculator!")
                break
                
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")

# Run the calculator
if __name__ == "__main__":
    calculator()