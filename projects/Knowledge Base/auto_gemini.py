import pexpect
import time

# Path to your gemini_generate.py script
script_path = './gemini_generate.py'

# Start the process
child = pexpect.spawn(f'python3 {script_path} links_primitive.md', encoding='utf-8')

# Function to capture all output
def capture_output(child):
    return child.before

# Wait for the "Enter a prompt (or 'done' to finish):"
child.expect(r'Enter a prompt \(or "done" to finish\):')

# Automate the first input (Embed link into markdown)
child.sendline('Embed this link into markdown with correct title and bullet -')

# Wait for the next prompt
child.expect(r'Enter a prompt \(or "done" to finish\):')

# Automate the second input (Summarize the post)
child.sendline('Summarize this post in detail')

# Wait for the next prompt
child.expect(r'Enter a prompt \(or "done" to finish\):')

# Automate the "done" input
child.sendline('done')

# Wait for the "Choose the content source" prompt
child.expect(r'Choose the content source \(1 for files, 2 for lines\):')

# Automate the selection of content source (2 for lines)
child.sendline('2')

# Wait for the next prompt ("Do you want to perform aggregate operation?")
child.expect(r'Do you want to perform aggregate operation\?')

# Automate the aggregate operation selection (1 for agg)
child.sendline('1')

# Allow the process to finish and capture all output
child.expect(pexpect.EOF)

# Capture the output after all inputs are completed
final_output = capture_output(child)

# Print the final output (everything after all the inputs)
print(final_output)

# Close the process
child.close()

print("Automation complete.")
