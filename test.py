from inputter import Inputter, nonempty_condition


def main():
    (bread, _), (meat, _), (condiment, _) = (
        Inputter((nonempty_condition(),),
                 prompt="What type of bread would you like? ",
                 no_input_msg="You get white bread.",
                 no_input_val="white bread").get(),
        Inputter((nonempty_condition(),),
                 prompt="What type of meat would you like? ",
                 no_input_msg="You get chicken.",
                 no_input_val="chicken").get(),
        Inputter((nonempty_condition(),),
                 prompt="What condiment would you like? ",
                 no_input_msg="You get mayo.",
                 no_input_val="mayo").get()
    )

    print(f"First, toast the {bread}")
    print(f"Then, add the {meat}")
    print(f"Finally, add the {condiment}")

if __name__ == '__main__':
    main()
