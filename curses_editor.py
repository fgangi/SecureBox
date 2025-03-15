import curses
from curses import textpad

def curses_editor(initial_text=""):
    """
    Launches a simple curses-based text editor initialized with initial_text.
    The editor finishes when the user presses Ctrl-G.
    Returns the edited text.
    """
    def editor(stdscr):
        # Clear the screen
        stdscr.clear()
        
        # Print instructions
        stdscr.addstr(0, 0, "Edit your secret (Ctrl-G to finish):")
        
        # Define dimensions and position for the editing window
        height, width = 10, 60
        start_y, start_x = 2, 2
        
        # Create a new window for editing
        edit_win = curses.newwin(height, width, start_y, start_x)
        
        # Draw a border around the editing window
        textpad.rectangle(stdscr, start_y - 1, start_x - 1, start_y + height, start_x + width)
        stdscr.refresh()
        
        # Pre-populate the editing window with initial_text
        edit_win.addstr(0, 0, initial_text)
        
        # Create a Textbox widget to allow editing
        tb = textpad.Textbox(edit_win)
        
        # Let the user edit and capture the result when Ctrl-G is pressed
        edited_text = tb.edit()
        return edited_text.strip()
    
    # Use curses.wrapper to safely initialize and tear down the curses environment
    return curses.wrapper(editor)

# Example usage:
if __name__ == "__main__":
    result = curses_editor("Type your secret here...")
    print("Edited text:", result)
