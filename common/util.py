import os
import random
import time

import fontawesome as fa

from common.deps.pymetasploit3 import msfrpc


def terminal_size():
    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        # Inappropriate ioctl for device caused by running in simulated terminal
        columns, lines = 80, 24
    return columns, lines


def print_header(message, sep='=', app=None):
    """
    Print a centered header message
    :return:
    """
    columns, lines = terminal_size()
    print(sep * columns)
    print(message.center(columns))
    print(sep * columns)
    if app:
        print(str(app).center(columns))
        print(" " * columns)


def clear():
    """Clear the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def options(options: dict, text="Select", instructions="Select an option"):
    """Enumerate text value for options and print them, return the corresponding function"""
    print(instructions)
    temp = {}
    print("0: Back")
    for i, (key, value) in enumerate(options.items()):
        temp[i + 1] = value
        print(f"{i + 1}: {key}")

    while True:
        try:
            selection = int(input(f"{text} (0-{len(options)}): "))
            if selection == 0:
                return

            elif selection in range(len(options) + 1):
                # Lookup the selection
                return temp[selection]

            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid selection")


def module_loaded(text, sep='-', app=None):
    """
    Clear the screen and print a centered header message
    :param app:
    :param sep:
    :param text:
    :return:
    """

    # if an app is given with debug mode, do not clear the screen
    if app and app.debug:
        print_header("Clear Disabled on Debug Mode", "")
        print_header(text, sep=sep, app=app)

    else:
        clear()
        print_header(text, sep=sep, app=app)




def vert_center(text):
    """
    Space text at the center of the terminal vertically and horizontally
    :param text:
    :return:
    """

    columns, lines = terminal_size()
    print("\n" * (lines // 2))
    text = text.splitlines()
    for i, line in enumerate(text):
        text[i] = line.center(columns)

    text = "\n".join(text)
    text = text.center(lines)
    print(text)
    print("\n" * (lines // 2))


def warn(text, centered=True):
    """Print a warning message"""
    text = f"{fa.icons['exclamation-triangle']} {text}"
    if centered:
        print_header(text, sep=' ')
    else:
        print(text)

def exit_quote():
    """Print a random exit quote"""
    quotes = [
        "Huginn and Muninn hover each day The wide earth over; I fear for Huginn lest he fare not back,-- Yet watch I "
        "more for Muninn.",
        "The raven is a symbol of wisdom and knowledge. It is also a symbol of death and the afterlife.",
        "Muninn is the name of Odin's raven. He is the one who brings Odin the news of the world.",
        "Muninn means 'mind' or 'memory'.",
        "Two ravens flew from Odin's shoulders; Huginn to the hanged and Muninn to the slain."]

    clear()

    vert_center(f"\n{random.choice(quotes)}")
    print_header("Goodbye", sep=' ')


def run_module_with_output(console, mod, payload=None, run_as_job=False, timeout=301, runoptions=None):
    """
    Execute a module and wait for the returned data
    Mandatory Arguments:
    - mod : the MsfModule object
    Optional Keyword Arguments:
    - payload : the MsfModule object to be used as payload
    """
    options_str = ['use {}/{}'.format(mod.moduletype, mod.modulename)]
    if console.is_busy():
        raise msfrpc.MsfError('Console {} is busy'.format(console.cid))
    console.read()  # clear data buffer
    opts = runoptions.copy()
    # if payload is None:
    #     opts['DisablePayloadHandler'] = True

    # Set module params
    print(opts)
    for k in opts.keys():
        options_str.append('set {} {}'.format(k, opts[k]))

    options_str.append('run -z')
    if run_as_job:
        options_str[-1] += " -j"
    # options_str += "\n"
    print(options_str)
    for option in options_str:
        console.write(option)
        time.sleep(1)
    # console.write(options_str)
    data = ''
    timer = 0
    while data == '' or console.is_busy():
        time.sleep(1)
        data += console.read()['data']
        timer += 1
        if timer > timeout:
            break
    return data