import sys
import os

import yaml


HELP_MESSAGE = """
_______________________________________________
The lexic analyzer for boolean logic operations
by Elina Akhmanova 
_______________________________________________


* to get this message: 
    `python lexic.py [--help|-h|man|help]`
    
* to process a file with data
    `python lexic.py <filename>`
    - <filename> is the name of file with logic operations
"""
DEBUG_LENGTH = 10


def exit_with_error(data, pos):
    start = max(0, pos - DEBUG_LENGTH)
    end = min(len(data), pos + DEBUG_LENGTH)
    new_str = data[start:end].replace('\n', ' ')
    error_msg = f"Lexic error: unexpected data. \n {new_str}\n" + ' ' * (pos-start+1) + '^'
    return error_msg

def lexic(data, state_machines):
    # Preprocessing data
    data = data.upper() + ' '
    # Result of the lexic analyzer
    result = []
    # Current message
    curr_line = ''
    # Start position
    start_pos = 0
    # curr_line position
    pos = 0
    # curr_line state machine's index
    sm_idx = 0
    # curr_line state
    curr_state = 'q0'
    while pos < len(data):
        element = data[pos]

        if curr_state == 'qerror':
            sm_idx += 1
            pos = start_pos
            curr_line = ''

        # We don't have any more state machines
        if sm_idx >= len(state_machines):
            return exit_with_error(data, pos)

        states = state_machines[sm_idx]['states']

        # The element was found in the state machine
        if element in states[curr_state]:
            curr_line = curr_line + element
            pos += 1
            curr_state = states[curr_state][element]
        else:
            pos = start_pos
            curr_state = 'q0'
            curr_line = ''
            sm_idx += 1

        if curr_state.startswith('END'):
            el_type = curr_state.split('|')[1]
            # Not delimiters or brackets
            if len(curr_line) > 1:
                curr_line = curr_line[:-1]
                pos -= 1
            result.append((el_type, curr_line))
            curr_line = ''
            sm_idx = 0
            curr_state = 'q0'
            start_pos = pos

    return result[:-1]


if __name__ == '__main__':
    # Load dictionaries for state machines
    state_machines = []
    for dic_file in ['delimiters', 'equal', 'brackets', 'logic', 'integers', 'variables']:
        with open(f"state-machine-data/{dic_file}.yaml", 'r') as f:
            state_machines.append(yaml.full_load(f))

    # Get all arguments
    args = sys.argv[1:]

    # Help message
    if len(args) != 1 or len(args) == 1 and args[0] in ('--help', '-h', 'man', 'help'):
        print(HELP_MESSAGE)
    # Get a filename
    else:
        filename = args[0]
        if not os.path.isfile(filename):
            print("Wrong file!")
            exit(2)
        with open(filename, 'r+') as f:
            # Add a delimiter ' ' in the end of file.
            data = f.read()
        print((lexic(data, state_machines)))
