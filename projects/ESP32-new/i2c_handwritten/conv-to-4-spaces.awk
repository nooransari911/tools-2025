#!/usr/bin/awk -f

{
    # Match leading spaces (zero or more)
    match($0, /^ */)

    # RLENGTH is the length of the matched string (number of leading spaces)
    num_leading_spaces = RLENGTH

    # Calculate the new number of spaces (double the original)
    new_indent_length = num_leading_spaces * 2

    # Get the rest of the line (after the leading spaces)
    rest_of_line = substr($0, num_leading_spaces + 1)

    # Print the new indentation followed by the rest of the line
    # sprintf("%*s", n, "") creates a string of n spaces
    printf "%*s%s\n", new_indent_length, "", rest_of_line

}
