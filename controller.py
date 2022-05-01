MAIN_BUTTONS = ['ZR', 'ZL', 'R', 'L', 'X', 'A', 'B', 'Y']
CENTER_BUTTONS = ['Circle', 'Home', '+', '-']

def pad_left(binary, size):
    while len(binary) < size:
        binary = '0' + binary
    return binary

def normalize_analogue(r, is_inverted=False):
    if not is_inverted:
        return round((r - 128) / 127.5, 2)
    else:
        return round((128 - r) / 127.5, 2)

def d_pad(byte):
    if byte == 0:
        d_direction = [0, 1]
    elif byte == 1:
        d_direction = [1, 1]
    elif byte == 2:
        d_direction = [1, 0]
    elif byte == 3:
        d_direction = [1, -1]
    elif byte == 4:
        d_direction = [0, -1]
    elif byte == 5:
        d_direction = [-1, -1]
    elif byte == 6:
        d_direction = [-1, 0]
    elif byte == 7:
        d_direction = [-1, 1]
    else:
        d_direction = [0, 0]
    return d_direction

def interpret(raw_bytes):
    # Main
    byte_main = raw_bytes[0]
    main_binary = pad_left(bin(byte_main).replace('0b', ''), 8)
    main_pressed = []
    for i, e in enumerate(main_binary):
        if e == '1':
            main_pressed.append(MAIN_BUTTONS[i])
    
    # Center
    byte_center = raw_bytes[1]
    center_pressed = []
    if byte_center == 4 or byte_center == 8 or byte_center == 12:
        # Ignore if joystick and/or C-stick pressed
        pass
    else:
        center_binary = pad_left(bin(int(hex(byte_center).replace('0x', ''), 4)).replace('0b', ''), 4)
        for i, e in enumerate(center_binary):
            if e == '1':
                center_pressed.append(CENTER_BUTTONS[i])
    
    # D-pad
    byte_d = raw_bytes[2]
    d_direction = d_pad(byte_d)

    # Joystick
    byte_joystick_x, byte_joystick_y = raw_bytes[3:5]
    joystick_direction = [normalize_analogue(byte_joystick_x), normalize_analogue(byte_joystick_y, is_inverted=True)]

    # C-stick
    byte_c_x, byte_c_y = raw_bytes[5:]
    c_direction = [normalize_analogue(byte_c_x), normalize_analogue(byte_c_y, is_inverted=True)]

    # Composite output
    controller_output = {
        'Main': main_pressed,
        'Center': center_pressed,
        'D-pad': d_direction,
        'Joystick': joystick_direction,
        'C-stick': c_direction,
    }
    return controller_output