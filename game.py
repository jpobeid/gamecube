import time
import numpy as np

game_on = False
m = np.zeros([9, 9])
i, j = 4, 4
m[m.shape[0] - 1 - j, i] = 1

def update_matrix(i, j, direction, m):
    m_out = m.copy()
    m_out[m.shape[0] - 1 - j, i] = 0
    i += direction[0]
    j += direction[1]
    if j >= 0 and i >= 0 and j < m.shape[0] and i < m.shape[1]:
        m_out[m.shape[0] - 1 - j, i] = 1
        return [i, j, m_out]
    else:
        i -= direction[0]
        j -= direction[1]
        return [i, j, m]

def play(controller_output):
    global game_on
    global i, j, m

    if not game_on and '+' in controller_output.get('Center'):
        print('Game on!')
        game_on = True
    elif game_on:
        # Game frame rate
        time.sleep(0.1)

        direction = controller_output.get('D-pad')
        if direction == [0, 0]:
            pass
        else:
            i, j, m = update_matrix(i, j, direction, m)
            print(i, j)
            print(m)
        if 'A' in controller_output.get('Main'):
            print('BOOM!!!!')
    else:
        pass