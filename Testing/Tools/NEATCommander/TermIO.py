def get_input(numeric=True, message=None):
    while True:
        message = display_prompt(message)
        if numeric and message.isdigit():
            break
        if not numeric:
            break
    return message

def print_headline(message):
    print("")
    headline = "--|" + message + "|"
    width_difference = 60 - len(headline)
    for i in range(width_difference):
        headline = headline + "-"
    print(headline)

def display_choice(choices):
    print("")
    text = ""
    count = 1
    for choice in choices:
        text = text + str(count)
        text = text + " "
        text = text + choice
        text = text + "\n"
        count += 1
    print(text)

def display_prompt(message):
    print("")
    prompt = "(>^.^)> "
    if message:
        prompt = prompt + \
                 "(" + \
                 message +\
                 ") > "
    return input(prompt)

def edit_string(string):
    print("")
    print_headline("editing ...")
    print("Editing the string: " + string + " (leave empty to cancel)")
    print("")
    new_string = get_input(numeric=False, message="New string")
    if len(new_string) > 0:
        return new_string
    else:
        return string
