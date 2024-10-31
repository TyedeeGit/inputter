from src.inputter_tyedee import Inputter, nonempty_condition


def main():
    (bread, _), (meat, _), (condiment, _) = (
        Inputter((nonempty_condition(),),
                 prompt="What type of bread would you like? ",
                 attempts=0).get(),
        Inputter((nonempty_condition(),),
                 prompt="What type of meat would you like? ",
                 no_input_msg="You get chicken.",
                 no_input_val="chicken",
                 attempts=1).get(),
        Inputter((nonempty_condition(),),
                 prompt="What condiment would you like? ",
                 no_input_msg="You get mayo.",
                 no_input_val="mayo",
                 attempts=3).get()
    )

    print(f"First, toast the {bread}")
    print(f"Then, add the {meat}")
    print(f"Finally, add the {condiment}")

if __name__ == '__main__':
    main()
