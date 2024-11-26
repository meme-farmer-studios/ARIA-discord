import os
import time
import subprocess
import signal

ARIA_SCRIPT = 'aria.py'
SIGNAL_FILE = 'aria_signal.txt'

def start_aria():
    return subprocess.Popen(['python', ARIA_SCRIPT])

def read_signal():
    if os.path.exists(SIGNAL_FILE):
        with open(SIGNAL_FILE, 'r') as f:
            signal = f.read().strip()
        os.remove(SIGNAL_FILE)
        return signal
    return None

def write_signal(signal):
    with open(SIGNAL_FILE, 'w') as f:
        f.write(signal)

def main():
    aria_process = start_aria()
    print(f'Started {ARIA_SCRIPT} with PID {aria_process.pid}')

    while True:
        time.sleep(1)
        signal = read_signal()

        if signal == 'restart':
            print('Restart signal received')
            aria_process.terminate()
            aria_process.wait()
            aria_process = start_aria()
            print(f'Restarted {ARIA_SCRIPT} with PID {aria_process.pid}')
        elif signal == 'shutdown':
            print('Shutdown signal received')
            aria_process.terminate()
            aria_process.wait()
            print(f'Shut down {ARIA_SCRIPT}')
            break
        elif signal == 'update':
            print('Update signal received')
            aria_process.terminate()
            aria_process.wait()
            aria_process = start_aria()
            print(f'Restarted {ARIA_SCRIPT} with updated code, PID {aria_process.pid}')
        elif aria_process.poll() is not None:
            print(f'{ARIA_SCRIPT} has stopped unexpectedly, restarting...')
            aria_process = start_aria()
            print(f'Restarted {ARIA_SCRIPT} with PID {aria_process.pid}')

if __name__ == '__main__':
    main()