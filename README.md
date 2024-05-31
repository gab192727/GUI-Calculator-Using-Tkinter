# GUI-Calculator-Using-Tkinter
This is a simple GUI calculator built using Python and Tkinter. With the guide of Programiz, a YouTuber that does coding and stuff. here is the link https://www.youtube.com/watch?v=QZPv1y2znZo of what he made.

## Description:

This project is a graphical user interface (GUI) calculator built using Python, Tkinter, Pillow (PIL), and SymPy. It supports basic arithmetic operations, and advanced functions like factorials and square roots, and uses a visually appealing interface for user interaction.

![Caculator](./calculator(0).png "GUI Calculator")

### Features

- **Basic Operations**: Addition, subtraction, multiplication, and division.
- **Advanced Functions**: Factorials, nth roots, and power operations.
- **User Interface**: Clear and responsive interface with buttons for digits, operations, and special functions.
- **Keyboard Support**: Allows input through keyboard keys for convenience.
- **Error Handling**: Displays appropriate error messages for syntax errors, zero division errors, and other invalid operations.
- **Previous Result**: Shows the last evaluated result for quick reference.

### Project Structure

- **calculator.py**: The main script containing the `Calculator` class, which handles the GUI layout, button configurations, event bindings, and calculation logic.
- **requirements.txt**: Lists the necessary Python packages to run the calculator.
- **README.md**: Detailed documentation of the project, including features, setup instructions, and usage.

![Caculator](./calculator(1).png "GUI Calculator")

### File Descriptions

1. **calculator.py**: 
   - **Class `Calculator`**:
     - `__init__`: Initializes the calculator window, sets up fonts, colors, button configurations, and binds keys.
     - `make_button_frame`: Creates the frame for buttons.
     - `make_display_label`: Creates the labels for displaying the current and full expressions.
     - `make_last_answer_display`: Creates the label for displaying the last answer.
     - `make_digit_buttons`, `make_operation_buttons`, `make_special_button`, `make_special_operator_buttons`, `make_equal_button`: Methods to create and configure buttons.
     - `button_configure`: Configures the grid layout for buttons.
     - `update_full_label`, `update_current_label`: Updates the display labels with current expressions.
     - `append_digit`, `append_operator`: Methods to handle digit and operator button presses.
     - `clear_all`, `clear_entry`: Methods to clear the display.
     - `evaluate`: Evaluates the full expression.
     - `evaluate_factorial`, `evaluate_sqrt`: Static methods to handle factorial and square root operations.
     - `root_to_n`, `raise_to_n`, `factorial_n`: Methods to handle special operations.
     - `get_last_answer`: Retrieves the last calculated answer.
     - `error_check`: Clears the display in case of an error.
     - `bind_keys`: Binds keyboard keys to respective functions.
     - `add_hover_effect`: Adds hover effects to buttons.
     - `run`: Starts the main event loop for the application.

2. **requirements.txt**: Specifies the Python packages required to run the calculator:
   - `Pillow`: Used for handling images.
   - `SymPy`: Used for symbolic mathematics, ensuring accurate calculations.
   - `tkinter`: Used for the graphical user interface.
   - 'math': used for accurate calculation of square root and factorial.
   - 're': used for finding all the digits and operators for easy evaluation
   - 'sympy': used for evaluation and correct handling of parenthesis.


