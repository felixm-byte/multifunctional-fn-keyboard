import pickle

# Run me on your PC, NOT on the pico.

#reference https://github.com/micropython/micropython-lib/blob/master/micropython/usb/usb-device-keyboard/usb/device/keyboard.py#L118 for key binding
class KeyCode:
    No = 0 
    A = 4
    B = 5
    C = 6
    D = 7
    E = 8
    F = 9
    G = 10
    H = 11
    I = 12
    J = 13
    K = 14
    L = 15
    M = 16
    N = 17
    O = 18
    P = 19
    Q = 20
    R = 21
    S = 22
    T = 23
    U = 24
    V = 25
    W = 26
    X = 27
    Y = 28
    Z = 29
    N1 = 30  # Standard number row keys
    N2 = 31
    N3 = 32
    N4 = 33
    N5 = 34
    N6 = 35
    N7 = 36
    N8 = 37
    N9 = 38
    N0 = 39
    ENTER = 40
    ESCAPE = 41
    BACKSPACE = 42
    TAB = 43
    SPACE = 44
    MINUS = 45  # - _
    EQUAL = 46  # = +
    OPEN_BRACKET = 47  # [ {
    CLOSE_BRACKET = 48  # ] }
    BACKSLASH = 49  # \ |
    HASH = 50  # # ~
    SEMICOLON = 51  # ; :
    QUOTE = 52  # ' "
    GRAVE = 53  # ` ~
    COMMA = 54  # , <
    DOT = 55  # . >
    SLASH = 56  # / ?
    CAPS_LOCK = 57
    F1 = 58
    F2 = 59
    F3 = 60
    F4 = 61
    F5 = 62
    F6 = 63
    F7 = 64
    F8 = 65
    F9 = 66
    F10 = 67 
    F11 = 68 
    F12 = 69 
    PRINTSCREEN = 70 
    SCROLL_LOCK = 71 
    PAUSE = 72 
    INSERT = 73
    HOME = 74
    PAGEUP = 75
    DELETE = 76
    END = 77
    PAGEDOWN = 78
    RIGHT = 79  # Arrow keys
    LEFT = 80
    DOWN = 81
    UP = 82
    KP_NUM_LOCK = 83
    KP_DIVIDE = 84
    KP_AT = 85
    KP_MULTIPLY = 85
    KP_MINUS = 86
    KP_PLUS = 87
    KP_ENTER = 88
    KP_1 = 89
    KP_2 = 90
    KP_3 = 91
    KP_4 = 92
    KP_5 = 93
    KP_6 = 94
    KP_7 = 95
    KP_8 = 96
    KP_9 = 97
    KP_0 = 98


keys = ["Y","X","B","A","UP","LEFT","RIGHT","DOWN","1","2","3","4","5"]

def view_previous():
    with open('mappings.kb', 'rb') as f:
        file = pickle.load(f)
        print(file)

def setup_bindings():
    if input("y/n to debug previous file:").lower() == "y":
        view_previous()
    inputs = {}
    print("Refer to the code for the exact format to enter your desired keys in. Enter No to bind nothing to a key.")
    for key in keys:
        keycode = 0
        while keycode == 0:
            n = input(f"Enter the key's name for {key}:").upper()
            keycode = getattr(KeyCode, n, 0)
        inputs[key] = keycode
    try:
        with open('mappings.kb', 'wb') as f:
            pickle.dump(inputs, f)
    except Exception as e:
        print("Error occured while saving")
        print(f"{e}")
    print("All done, file saved!")


setup_bindings()

