# File contains implementation of a representation for Mastermind and Rounds of Mastermind.
# See main.py or examples.ipynb for example usages.

import time
from enum import Enum
from scsa import *
from player import *


def letter_to_num(letter: str) -> int:
    """Converts letter to number based on position its in alphabet

    Args:
        letter (str): Letter to convert to number.

    Returns:
        int: Position of letter in alphabet.
    """

    return ord(letter) - 64


class Result(Enum):
    """Possible results of a round or guess."""

    WIN = 1
    LOSS = 2
    FAILURE = 3
    VALID = 4  # Used for guesses only, signals that the guess was valid, but not a winning guess.


class Results:
    """Records number of wins, losses, and failures, and score of a tournament."""

    def __init__(self):

        self.__results: dict[Result, int] = {
            Result.WIN: 0,
            Result.LOSS: 0,
            Result.FAILURE: 0,
        }  # Private field used to keep track of the result of a round.
        self.score = 0  # Public field used to keep track of score.

    def record_result(self, result: Result) -> None:
        """Records result.

        Args:
            result (Result): Records a Result.WIN, Result.LOSS, or Result.FAILURE.
        """

        self.__results[result] += 1

    def get_number_of_wins(self) -> int:

        return self.__results[Result.WIN]

    def get_number_of_losses(self) -> int:

        return self.__results[Result.LOSS]

    def get_number_of_failures(self) -> int:

        return self.__results[Result.FAILURE]

    def get_number_of_rounds(self) -> int:
        """Get number of rounds recorded.

        Returns:
            int: Number of wins, losses, and failures recorded.
        """

        return (
            self.get_number_of_wins()
            + self.get_number_of_losses()
            + self.get_number_of_failures()
        )

    def compute_old_score(self) -> int:
        """Computes score using old score function for a tournament

        Returns:
            int: Returns score for a tournament based on the results.
        """

        return 5 * self.get_number_of_wins() - 2 * self.get_number_of_losses()

    def __str__(self) -> str:
        """String representation of a Results object."""

        return (
            "{Wins: "
            + str(self.get_number_of_wins())
            + ", Losses: "
            + str(self.get_number_of_losses())
            + ", Failures: "
            + str(self.get_number_of_failures())
            + ", Score: "
            + str(self.score)
            + "}"
        )


class Round:
    """Representation for round of the game of Mastermind"""

    def __init__(
        self,
        board_length: int,
        colors,
        answer: str,
        scsa_name: str,
        guess_cutoff: int = 100,
        time_cutoff: int = 5,
    ):
        """Constuctor for Round

        Args:
            board_length (int): Number of pegs.
            colors (list[str]): All possible colors that can be used to generate a code.
            answer (string): Answer for the round that the player is trying to guess.
            scsa_name (str): Name of SCSA used to generate secret code.
            guess_cutoff (int, optional): Number of guesses allowed per round. Defaults to 100.
            time_cutoff (int, optional): Amount of time in seconds allowed for the round. Defaults to 5.
        """

        self.board_length = board_length
        self.colors = colors
        self.answer = answer
        self.scsa_name = scsa_name
        self.guesses = 0
        self.guess_cutoff = guess_cutoff
        self.time_cutoff = time_cutoff
        self.time_buffer = 0.1  # Seconds
        self.time_used = 0

    def valid_guess(self, guess: str) -> bool:
        """Checks whether a guess is valid

        Args:
            guess (str): Guess of secret code.

        Returns:
            bool: Returns True if guess is valid (correct length and uses only possible colors) and False otherwise.
        """

        if len(guess) != self.board_length:

            return False

        for peg in guess:

            if peg not in self.colors:

                return False

        return True

    def count_colors(self, guess: str):
        """Counts number of occurences for each color

        Args:
            guess (str): Guess of secret code.

        Returns:
            list[int]: Returns list of number of occurences for each color in self.color.
        """

        counts = [0] * len(self.colors)

        for peg in guess:

            idx = letter_to_num(peg) - 1

            counts[idx] += 1

        return counts

    def process_guess(self, guess: str):
        """Determines number of exactly correct pegs and partially correct pegs for a guess

        Args:
            guess (str): Guess of secret code.

        Returns:
            tuple[int,int]: (number of pegs that match exactly with the answer,
                            number of pegs that are the right color, but in the wrong location)
        """

        guess_color_count = self.count_colors(guess)
        answer_color_count = self.count_colors(self.answer)

        exact = 0
        other = 0

        for i in range(self.board_length):

            if guess[i] == self.answer[i]:

                exact += 1

                # Decrease color counts
                guess_color_count[letter_to_num(guess[i]) - 1] -= 1
                answer_color_count[letter_to_num(self.answer[i]) - 1] -= 1

        for i in range(len(self.colors)):

            if answer_color_count[i] <= guess_color_count[i]:

                other += answer_color_count[i]

            elif (
                guess_color_count[i] < answer_color_count[i]
                and guess_color_count[i] > 0
            ):

                other += guess_color_count[i]

        return (exact, other)

    def respond_to_guess(self, guess: str):
        """Responds with correctness of player's guess.

        Args:
            guess (str): Guess of secret code.

        Returns:
            tuple[Result, int, int, int]: (result of round (WIN, LOSS, VALID, or FAILURE),
                                          number of pegs that match exactly with the answer,
                                          number of pegs that are the right color, but wrong location,
                                          number of guesses so far).
        """

        self.guesses += 1

        if self.time_used > self.time_cutoff + self.time_buffer:

            return (Result.LOSS, 0, 0, self.guesses)

        elif guess == self.answer:

            response = (Result.WIN, self.board_length, 0, self.guesses)

        elif self.valid_guess(guess):

            exact, other = self.process_guess(guess)

            response = (Result.VALID, exact, other, self.guesses)

        else:

            response = (Result.FAILURE, 0, 0, self.guesses)

        return response

    def play_round(self, player: Player):
        """Plays out a round of Mastermind.

        Args:
            player (Player): Player to guess secret code.

        Returns:
            tuple[Result, int]: (result of round (WIN, LOSS, or FAILURE)
                                number of guesses until that result was achieved).
        """

        self.guesses = 0
        player_response = (0, 0, 0)

        while self.guesses < self.guess_cutoff:

            start = time.time()
            guess = player.make_guess(
                self.board_length, self.colors, self.scsa_name, player_response
            )
            end = time.time()

            duration = end - start

            self.time_used += duration

            response = self.respond_to_guess(guess)
            player_response = response[1:]  # Remove result element

            # print("Response:", response, "Time:", self.time_used)

            if response[0] != Result.VALID:

                return (response[0], self.guesses)

        return (Result.LOSS, self.guesses)


class Mastermind:
    """Representation to play the game of Mastermind."""

    def __init__(
        self,
        board_length: int = 4,
        colors: str = [chr(i) for i in range(65, 91)],
        guess_cutoff: int = 100,
        round_time_cutoff: int = 5,
        tournament_time_cutoff: int = 300,
    ):
        """Constructor for Mastermind.

        Args:
            board_length (int, optional): Number of pegs. Defaults to 4.
            colors (list[str], optional): List of colors that can be used to generate a secret code. Defaults to [chr(i) for i in range(65,91)].
            guess_cutoff (int, optional): Number of guesses allowed per round. Defaults to 100.
            round_time_cutoff (int, optional):  Amount of time in seconds allowed for the round. Defaults to 5.
            tournament_time_cutoff (int, optional): Amount of time in seconds allowed for the round. Defaults to 300.
        """

        self.board_length = board_length
        self.colors = colors
        self.num_colors = len(colors)
        self.guess_cutoff = guess_cutoff
        self.round_time_cutoff = round_time_cutoff
        self.tournament_time_cutoff = tournament_time_cutoff
        self.time_used = 0

    def print_results(
        self, player: Player, scsa_name: str, results: Results, num_rounds: int
    ) -> None:
        """Prints results for a tournament.

        Args:
            player (Player): Player who played in the tournament.
            scsa_name (str): Name of SCSA used to generate codes in tournament.
            results (Results): Object containing number of wins, losses, failures, and score for a tournament.
            num_rounds (int): Number of rounds in the tournament.
        """

        print("Player:", player.player_name)
        print("SCSA Name:", scsa_name)
        print("Game:", self.board_length, "Pegs", self.num_colors, "Colors")
        print("Rounds:", results.get_number_of_rounds(), "out of", num_rounds)
        print("Results:", results)

        return

    def play_tournament(self, player: Player, scsa: SCSA, num_rounds: int) -> None:
        """Plays a tournament of Mastermind

        Args:
            player (Player): Player who plays in tournament, making guesses.
            scsa (SCSA): SCSA used to generate secret codes for player to guess.
            num_rounds (int): Number of rounds of Mastermind to play.
        """

        results = Results()

        for round in range(1, num_rounds + 1):

            code = scsa.generate_codes(self.board_length, self.colors, 1)[0]

            round = Round(
                self.board_length,
                self.colors,
                code,
                scsa.name,
                self.guess_cutoff,
                self.round_time_cutoff,
            )

            start = time.time()
            result, guesses = round.play_round(player)
            end = time.time()

            duration = end - start

            self.time_used += duration

            if self.time_used > self.tournament_time_cutoff:

                break

            # print("Round:", round, "|",  "Result:", result, "|", "Guesses:", guesses)

            results.record_result(result)

            if result == Result.WIN:

                results.score += (
                    self.board_length * len(self.colors) * (5 * guesses ** (-0.5))
                )

            elif result == Result.FAILURE:

                results.score -= 2 * self.board_length * len(self.colors)

                break

        self.print_results(player, scsa.name, results, num_rounds)

        return

    def practice_tournament(
        self, player: Player, scsa_name: str, code_file: str
    ) -> None:
        """Plays a tournament of Mastermind using pregenerated codes from file

        Args:
            player (Player): Player who plays in tournament, making guesses.
            scsa_name (str): Name of SCSA used to generate codes in tournament.
            code_file (str): Name of file to read secret codes from.
        """

        codes = read_from_file(code_file)
        num_rounds = len(codes)
        results = Results()
        cur_round = 0

        for code in codes:

            cur_round += 1

            round = Round(
                self.board_length,
                self.colors,
                code,
                scsa_name,
                self.guess_cutoff,
                self.round_time_cutoff,
            )

            start = time.time()
            result, guesses = round.play_round(player)
            end = time.time()

            duration = end - start

            self.time_used += duration

            if self.time_used > self.tournament_time_cutoff:

                break

            # print("Round:", cur_round, "|", "Result:", result, "|", "Guesses:", guesses)

            results.record_result(result)

            if result == Result.WIN:

                results.score += (
                    self.board_length * len(self.colors) * (5 * guesses ** (-0.5))
                )

            elif result == Result.FAILURE:

                results.score -= 2 * self.board_length * len(self.colors)

                break

        self.print_results(player, scsa_name, results, num_rounds)

        return
