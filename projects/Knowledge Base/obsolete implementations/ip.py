import sys
import signal
import tty
import termios

def get_char(fd):
    """Reads a single character from stdin."""
    ch = sys.stdin.read(1)
    return ch

def run_chatbot():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def restore_terminal():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def signal_handler_ctrl_d(sig, frame):
        restore_terminal()
        print("\nChatbot exiting")
        sys.exit(0)

    signal.signal(signal.SIGQUIT, signal_handler_ctrl_d)  # Ctrl+D
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)  # Ignore Ctrl+Z

    print("Chatbot started. Type 'exit' to quit or press Ctrl+D.")

    try:
        while True:
            print("You: ", end="", flush=True)
            user_input = ""
            tty.setraw(fd)  # Set raw mode for each input

            try:
                while True:
                    char = get_char(fd)

                    if char == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt  # Raise the exception

                    elif char == '\x04':  # Ctrl+D
                        raise EOFError

                    elif char == '\r' or char == '\n':
                        print()
                        break

                    elif char == '\x7f':  # Backspace
                        if user_input:
                            user_input = user_input[:-1]
                            print('\b \b', end="", flush=True)
                    else:
                        user_input += char
                        print(char, end="", flush=True)

            except KeyboardInterrupt:
                print("^C")
                restore_terminal() #restore terminal
                # print("You: ", end="", flush=True)  # Reprint prompt
                continue  # Go back to the beginning of the outer loop

            finally:
                restore_terminal() #always restore


            if user_input.lower() == 'exit':
                break
            print("Chatbot:", user_input)

    except EOFError:
        print("\nChatbot exiting")
    finally:
        restore_terminal()  # Always restore terminal settings

if __name__ == "__main__":
    run_chatbot()
