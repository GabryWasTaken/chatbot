import getpass
try:
    import termios  # Linux/MacOS
except:
    import msvcrt  # Windows


def getpass_masked(prompt="Password: "):
    password = ""
    if msvcrt.get_osfhandle(0) != -1:  # Verify if the system is Windows
        print(prompt, end="", flush=True)
        while True:
            key = msvcrt.getch()
            if key == b'\r' or key == b'\n':
                print()
                break
            elif key == b'\x08':  
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            else:
                password += key.decode("utf-8")
                print("*", end="", flush=True)
    else:  # If you are on Linux or MacOS
        print(prompt, end="", flush=True)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key = ord(sys.stdin.read(1))
                if key == 13 or key == 10: 
                    print()
                    break
                elif key == 127:  
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    password += chr(key)
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password
