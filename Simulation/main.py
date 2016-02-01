import PyCreatures


def __main__():

    py_creatures = PyCreatures.PyCreatures()

    while not py_creatures.should_quit:
        py_creatures.perform_command(input("> "))


if __name__ == "__main__":
    # milestone_1()
    # milestone_2()
    __main__()
