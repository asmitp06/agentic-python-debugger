import sys
import threading
import queue

# Define a timeout for input in seconds
INPUT_TIMEOUT = 1

# Function to read input in a separate thread
def read_input_thread(q):
    try:
        # sys.stdin.readline() is a blocking call.
        # We put it in a thread so the main thread can wait with a timeout.
        line = sys.stdin.readline().strip()
        q.put(line)
    except Exception:
        # In case of any error during readline (e.g., EOF on some systems), put None
        q.put(None)

# Create a queue to pass data from the thread to the main process
input_queue = queue.Queue()

# Start the input reading thread
input_thread = threading.Thread(target=read_input_thread, args=(input_queue,))
input_thread.daemon = True # Allow the main program to exit even if the thread is still running
input_thread.start()

line = None
try:
    # Attempt to get input from the queue with a timeout
    line = input_queue.get(timeout=INPUT_TIMEOUT)
except queue.Empty:
    # Timeout occurred, no input received within the specified time
    line = None

# Now process the 'line' variable as per the original logic
if line is not None: # Input was received (not a timeout, and no thread error)
    if line:
        try:
            a, b = map(int, line.split())
        except ValueError:
            # Handle cases where input is not two integers or malformed
            a, b = 0, 0 # Default values to prevent further errors
    else:
        # Input stream was readable but returned an empty line (e.g., EOF or just Enter)
        a, b = 0, 0 # Default values
else:
    # Timeout occurred, or an error in the input thread (line is None)
    a, b = 0, 0 # Default values

print(a + b)