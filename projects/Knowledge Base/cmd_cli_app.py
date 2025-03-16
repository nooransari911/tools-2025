import cmd

class MyCLI(cmd.Cmd):
    intro = "Welcome to my CLI!"
    prompt = "(mycli) "

    def do_hello(self, arg):
        """Prints 'Hello' along with any provided argument."""
        print(f"Hello {arg}!")

    def do_exit(self, arg):
        """Exits the CLI."""
        print("Goodbye!")
        return True  # Returning True stops the cmdloop

if __name__ == '__main__':
    MyCLI().cmdloop()
