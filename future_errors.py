def print_add_format_error():
    print('Incorrect format. Use one of the following:')
    print('"add to yyyy-mm-dd"')
    print('"add to mm-dd" - assuming it is current year')
    print('"add to dd" - assuming it is current month')

def print_incorrect_date_error():
    print('Incorrect date format. Use yyyy-mm-dd')

def print_past_error():
    print('Date is in the past!')

def print_incorrect_rm_format_error():
    print('Incorrect "rm" format. Use "rm <index>"')

def print_incorrect_index_error():
    print("Incorrect index. It must be an integer that fits index bounds.")

def print_cycle_format_error():
    print("Incorrect cycle format. Use [cycle <cycle type> <yyyy-mm-dd>]")

def print_cycle_type_error():
    print("Unknown cycle type")

def print_set_error():
    print('No such command. To set window use "set window".')

def print_window_error():
    print("Incorrect window value. It must be an integer greater than zero.")
