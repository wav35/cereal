import socket
from figlets import letters

def transform_figlets(fig: str) -> list[list[int]]:
    """
    Converts a figlet string to an array, setting
    a '1' where there is a '#' symbol and 0
    otherwise
    """
    array: list[list[int]] = [[]]
    array_counter = 0
    for char in fig:
        if char == "\n":
            array.append([])
            array_counter += 1
        elif char == "#":
            array[array_counter].append(1)
        else:
            array[array_counter].append(0)

    return array

def string_to_figlet_array(padding: int, string: str) -> list[list[int]]:
    """
    Converts a string into a contiguous figlet array and adds
    starting padding (all zeros)
    """
    fig_array = [[] for _ in range(7)] # All figlets are exactly 7 chars high
    for _ in range(padding):
        for i in range(len(fig_array)):
            fig_array[i].append(0)
    for char in string:
        figlet = letters[char]
        for i, row in enumerate(figlet):
            fig_array[i].extend(row)
        for i, row in enumerate(letters["charspace"]):
            fig_array[i].extend(row)

    return fig_array



def print_figlet_array(array: list[list[int]], start: int, end: int):
    """
    Prints the given figlet array in the window size [start, end)
    """
    for y in array:
        for x in y[start:end]:
            if x == 1:
                print("#", end="")
            elif x == 0:
                print(" ", end="")
        print()

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    lip = s.getsockname()[0]
    s.close()

    return lip
