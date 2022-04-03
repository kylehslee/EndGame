# File contains implementation of the secret code generating algorithms.
# See main.py or examples.ipynb for example usage.

import random
from abc import ABC, abstractmethod


def list_to_str(arr) -> str:
    """Converts a list of strings to a string

    Args:
        arr (list[str]]): List of strings.

    Returns:
        str: Returns string where all elements of list are joined together.
    """

    return "".join(arr)


def read_from_file(file_name):
    """Reads codes from file

    Args:
        file_name (str): Name of file to read from.

    Returns:
        list[str]: Returns list of codes read from specified file.
    """

    codes = []

    file = open(file_name, "r")

    lines = file.readlines()

    for l in lines:

        codes.append(l.strip())

    file.close()

    return codes


class SCSA(ABC):
    """Secret-code selection algorithm"""

    def __init__(self):
        """Constructor for SCSA"""

        self.name = ""

    @abstractmethod
    def generate_codes(
        self, length: int, colors, num_codes: int = 1):
        """Generate codes based on secret-code selection algorithm

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Raises:
            NotImplementedError: Function must be implemented by children classes.
        """

        raise NotImplementedError

    def write_to_file(self, codes, length: int, num_colors: int) -> None:
        """Writes codes to a file

        Args:
            codes (list[str]): List of codes to write to file.
            length (int): The length of the generated codes (same as number of pegs for an instance of Mastermind).
            num_colors (int): Number of colors that could be used to generate a code (i.e. length of list of colors).
        """

        file_name = self.name + "_" + str(length) + "_" + str(num_colors) + ".txt"

        file = open(file_name, "w")

        for code in codes:

            file.write(code + "\n")

        file.close()

        return

    def generate_and_write_to_file(
        self, length: int, colors, num_codes: int = 100
    ) -> None:
        """Generates codes and writes them to a file

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 100.
        """

        codes = self.generate_codes(length, colors, num_codes)

        if num_codes == 1:

            codes = [codes]

        self.write_to_file(codes, length, len(colors))

        return


class InsertColors(SCSA):
    """SCSA that generates codes containing colors selected at random"""

    def __init__(self):
        """Constructor for InsertColors"""

        self.name = "InsertColors"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on InsertColors SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        if len(colors) < 1:

            return []

        codes = []

        for _ in range(num_codes):

            codes.append(list_to_str(random.choices(colors, k=length)))

        return codes


class TwoColor(SCSA):
    """SCSA that generates codes containing only two randomly chosen colors"""

    def __init__(self):
        """Constructor for TwoColor"""

        self.name = "TwoColor"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on TwoColor SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        if len(colors) < 2:

            return []

        codes = []

        for _ in range(num_codes):

            usable_colors = random.sample(colors, k=2)

            # Create 'uninitialized' code as list
            code = [0] * length

            # Randomly pick two spots in string
            indicies = random.sample(range(0, length), k=2)

            # Set those two spots in the string to the two colors
            # This guarantees both colors are used at least once
            code[indicies[0]] = usable_colors[0]
            code[indicies[1]] = usable_colors[1]

            # Set rest of spots in code to one of the two colors randomly
            for i in range(length):

                if code[i] == 0:

                    code[i] = random.choice(usable_colors)

            codes.append(list_to_str(code))

        return codes


class ABColor(SCSA):
    """SCSA that generates codes containing only "A"s and "B"s"""

    def __init__(self):
        """Constructor for ABColor"""

        self.name = "ABColor"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on ABColor SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        usable_colors = ["A", "B"]

        codes = []

        for _ in range(num_codes):

            # Create 'uninitialized' code as list
            code = [0] * length

            # Randomly pick two spots in string
            indicies = random.sample(range(0, length), k=2)

            # Set those two spots in the string to the two colors
            # This guarantees both colors are used at least once
            code[indicies[0]] = usable_colors[0]
            code[indicies[1]] = usable_colors[1]

            # Set rest of spots in code to one of the two colors randomly
            for i in range(length):

                if code[i] == 0:

                    code[i] = random.choice(usable_colors)

            codes.append(list_to_str(code))

        return codes


class TwoColorAlternating(SCSA):
    """SCSA that generates codes that alternate between two colors"""

    def __init__(self):
        """Constructor for TwoColorAlternating"""

        self.name = "TwoColorAlternating"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on TwoColorAlternating SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        if len(colors) < 2:

            return []

        codes = []

        for _ in range(num_codes):

            first_color, second_color = random.sample(colors, k=2)

            code = ""

            for i in range(length):

                if i % 2 == 0:

                    code += first_color

                else:

                    code += second_color

            codes.append(code)

        return codes


class OnlyOnce(SCSA):
    """SCSA that generates codes in which a color appears at most once"""

    def __init__(self):
        """Constructor for OnlyOnce"""

        self.name = "OnlyOnce"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on OnlyOnce SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        actual_len = -1

        if len(colors) < length:

            actual_len = length
            length = len(colors)

        codes = []

        for _ in range(num_codes):

            code = list_to_str(random.sample(colors, k=length))

            if actual_len != -1:

                while len(code) < actual_len:

                    code += random.choice(colors)

            codes.append(code)

        return codes


class FirstLast(SCSA):
    """SCSA that generates codes in which the first and last colors are the same"""

    def __init__(self):
        """Constructor for FirstLast"""

        self.name = "FirstLast"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on FirstLast SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        if len(colors) < 1:

            return []

        codes = []

        for _ in range(num_codes):

            code = random.choices(colors, k=length - 2)
            color = random.choices(colors, k=1)

            code.insert(0, color[0])
            code.append(color[0])

            code = list_to_str(code)

            codes.append(code)

        return codes


class UsuallyFewer(SCSA):
    """SCSA that generates codes that usually has fewer (2 or 3) colors"""

    def __init__(self):
        """Constructor for UsuallyFewer"""

        self.name = "UsuallyFewer"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on UsuallyFewer SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        if len(colors) < 3:

            return []

        codes = []

        for _ in range(num_codes):

            probability = random.randint(0, 100)

            if probability < 90:

                num = random.randint(2, 3)

                picked_colors = random.sample(colors, k=num)

            else:

                picked_colors = colors

            code = list_to_str(random.choices(picked_colors, k=length))

            codes.append(code)

        return codes


class PreferFewer(SCSA):
    """SCSA that generates codes with a preference for fewer colors"""

    def __init__(self):
        """Constructor for PreferFewer"""

        self.name = "PreferFewer"

    def generate_codes(
        self, length: int, colors, num_codes: int = 1
    ):
        """Generate codes based on PreferFewer SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list[str]): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            list[str]: Returns code(s) generated from SCSA.
        """

        if len(colors) < 2:

            return []

        codes = []

        for _ in range(num_codes):

            probability = random.randint(0, 100)

            if probability <= 49:

                num = 1

                picked_colors = random.sample(colors, k=num)

            elif probability <= 74:

                num = 2

                picked_colors = random.sample(colors, k=num)

            elif probability <= 87:

                num = min(3, len(colors))

                picked_colors = random.sample(colors, k=num)

            elif probability <= 95:

                num = min(4, len(colors))

                picked_colors = random.sample(colors, k=num)

            elif probability <= 98:

                num = min(5, len(colors))

                picked_colors = random.sample(colors, k=num)

            else:

                picked_colors = colors

            code = list_to_str(random.choices(picked_colors, k=length))

            codes.append(code)

        return codes
