import os
import main
from time import sleep


class Args:
    """Convenience class to simulate the Namespace object provided to `main.main()`"""

    def __init__(self, input_path, output_path):
        self.input = input_path
        self.output = output_path
        self.verbose = None
        self.exclude = None


def continuous():
    """Main function to continuously look at the input folder and convert + move any .anx files found into the output folder."""
    input_folder_path = "user_experience/input"
    output_folder_path = "user_experience/output"
    iteration = 1
    while True:
        # Look at each file in the input folder
        files = os.listdir(input_folder_path)
        for file in files:
            # If the file is not .anx, just skip it
            base_name, extension = os.path.splitext(file)
            if extension != ".anx":
                continue

            # call main.py for the file, directing the converted file to the output folder
            with open(
                f"user_experience/input/{base_name}{extension}",
                mode="r",
                encoding="UTF-8",
            ) as in_file:
                with open(
                    f"user_experience/output/{base_name}.json", mode="w"
                ) as out_file:
                    args = Args(in_file, out_file)

                    try:
                        main.main(args)
                    except Exception as e:
                        print(f"Something went wrong with {base_name}: {e}")
                        continue

                    # move the .anx file into the output folder as well
                    os.rename(
                        f"{input_folder_path}/{file}", f"{output_folder_path}/{file}"
                    )

        # Delay the program for 30 seconds
        print(f"Finished iteration {iteration}")
        sleep(15)
        iteration += 1


if __name__ == "__main__":
    continuous()
