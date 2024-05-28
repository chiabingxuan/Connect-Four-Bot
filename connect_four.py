import copy


class ConnectFour(object):
    def __init__(self, first_player, num_rows=6, num_cols=7, bot_depth_of_search=9):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = [["" for col in range(num_cols)] for row in range(num_rows)]
        self.heights = [0 for col in range(num_cols)]
        self.available_columns = {col for col in range(self.num_cols)}
        self.current_player = first_player
        self.player_1_char = "H"    # player 1 is the maximiser in minimax algorithm
        self.player_2_char = "R"    # player 2 is the minimiser in minimax algorithm
        self.empty_char = "_"
        self.winner = None
        self.num_counters_in_board = 0
        self.col_of_last_counter = -1
        self.bot = ConnectFourBot(self.current_player, self.player_1_char, self.player_2_char, bot_depth_of_search, is_minimiser=True)

    def print_board(self):
        print(f"Current board ({self.player_1_char} = Your counter, {self.player_2_char} = Robot's counter, {self.empty_char} = Empty):")
        for row in self.board:
            row_str = ""
            is_first_slot = True
            for slot in row:
                if not slot:
                    added_char = self.empty_char
                else:
                    added_char = slot
                if is_first_slot:
                    row_str += added_char
                    is_first_slot = False
                else:
                    row_str += f" {added_char}"
            print(row_str)
        print()

    def place_counter(self, col):
        if col not in self.available_columns:  # checks whether column is completely filled
            return False
        current_height_of_col = self.heights[col]
        if self.board[self.num_rows - current_height_of_col - 1][col]:
            raise Exception("Slot is already occupied by a counter. Heights were not adjusted properly")
        if self.current_player == "1":
            self.board[self.num_rows - current_height_of_col - 1][col] = self.player_1_char
            print(f"You have inserted a counter into column {col + 1}\n")
        else:
            self.board[self.num_rows - current_height_of_col - 1][col] = self.player_2_char
            print(f"Robot has inserted a counter into column {col + 1}\n")
        self.heights[col] += 1
        if self.heights[col] == self.num_rows:
            self.available_columns.remove(col)
        self.num_counters_in_board += 1
        return True

    def game_is_over(self, col_of_last_counter):
        if col_of_last_counter == -1:  # game has only just started
            return False
        height_of_last_counter = self.heights[col_of_last_counter]
        row_of_last_counter = self.num_rows - height_of_last_counter
        if self.current_player == "1":  # last player was player 2
            last_player_symbol = self.player_2_char
        else:  # last player was player 1
            last_player_symbol = self.player_1_char
        # first check column
        if height_of_last_counter >= 4:
            for row in range(row_of_last_counter + 1, row_of_last_counter + 4):
                slot = self.board[row][col_of_last_counter]
                if not slot:
                    raise Exception("There are empty slots below the last counter added; last counter was inserted wrongly")
                if slot != last_player_symbol:
                    break
            else:  # did not break out of for loop
                if self.current_player == "1":
                    self.winner = "2"
                else:
                    self.winner = "1"
                return True
        # now check row
        current_moving_col = max(0, col_of_last_counter - 3)
        while current_moving_col <= min(self.num_cols - 4, col_of_last_counter):
            for count in range(4):
                slot = self.board[row_of_last_counter][current_moving_col]
                if slot != last_player_symbol:
                    current_moving_col += 1
                    break
                current_moving_col += 1
            else:  # did not break out of for loop
                if self.current_player == "1":
                    self.winner = "2"
                else:
                    self.winner = "1"
                return True
        # now check first diagonal (/)
        row_bound = min(self.num_rows - 1, row_of_last_counter + 3)
        steps_from_last_counter_to_row_bound = row_bound - row_of_last_counter
        col_bound = max(0, col_of_last_counter - 3)
        steps_from_last_counter_to_col_bound = col_of_last_counter - col_bound
        if steps_from_last_counter_to_row_bound >= steps_from_last_counter_to_col_bound:
            current_moving_row = row_of_last_counter + steps_from_last_counter_to_col_bound
            current_moving_col = col_bound
        else:
            current_moving_row = row_bound
            current_moving_col = col_of_last_counter - steps_from_last_counter_to_row_bound
        while current_moving_row >= max(3, row_of_last_counter) and current_moving_col <= min(self.num_cols - 4, col_of_last_counter):
            for count in range(4):
                slot = self.board[current_moving_row][current_moving_col]
                if slot != last_player_symbol:
                    current_moving_row -= 1
                    current_moving_col += 1
                    break
                current_moving_row -= 1
                current_moving_col += 1
            else:  # did not break out of for loop
                if self.current_player == "1":
                    self.winner = "2"
                else:
                    self.winner = "1"
                return True
        # now check second diagonal (\)
        row_bound = max(0, row_of_last_counter - 3)
        steps_from_last_counter_to_row_bound = row_of_last_counter - row_bound
        col_bound = max(0, col_of_last_counter - 3)
        steps_from_last_counter_to_col_bound = col_of_last_counter - col_bound
        if steps_from_last_counter_to_row_bound >= steps_from_last_counter_to_col_bound:
            current_moving_row = row_of_last_counter - steps_from_last_counter_to_col_bound
            current_moving_col = col_bound
        else:
            current_moving_row = row_bound
            current_moving_col = col_of_last_counter - steps_from_last_counter_to_row_bound
        while current_moving_row <= min(self.num_rows - 4, row_of_last_counter) and current_moving_col <= min(self.num_cols - 4, col_of_last_counter):
            for count in range(4):
                slot = self.board[current_moving_row][current_moving_col]
                if slot != last_player_symbol:
                    current_moving_row += 1
                    current_moving_col += 1
                    break
                current_moving_row += 1
                current_moving_col += 1
            else:  # did not break out of for loop
                if self.current_player == "1":
                    self.winner = "2"
                else:
                    self.winner = "1"
                return True
        if self.num_counters_in_board == self.num_rows * self.num_cols:  # game is a draw
            return True
        return False

    def switch_player(self):
        if self.current_player == "1":
            self.current_player = "2"
        else:
            self.current_player = "1"

    def play(self):
        print("You have started a Connect Four game!")
        print("-------------------------------------")
        self.print_board()
        while not self.game_is_over(self.col_of_last_counter):
            if self.current_player == "1":
                print("It's your turn to make a move!")
                col_chosen_str = input(f"Which column would you like to place a counter in? Enter a number from 1 to {self.num_cols} (1 = leftmost column, {self.num_cols} = rightmost column): ")
                while True:
                    if col_chosen_str not in [str(i) for i in range(1, self.num_cols + 1)]:
                        print("Invalid input!")
                        col_chosen_str = input(f"Which column would you like to place a counter in? Enter a number from 1 to {self.num_cols}: ")
                    else:
                        col_chosen = int(col_chosen_str) - 1
                        if not self.place_counter(col_chosen):
                            print("That column has already been completely filled!")
                            col_chosen_str = input(f"Which column would you like to place a counter in? Enter a number from 1 to {self.num_cols}: ")
                        else:
                            self.col_of_last_counter = col_chosen
                            break
            else:
                print("It's the robot's turn to make a move!")
                print("Robot is thinking...")
                min_utility, bot_col_chosen = self.bot.find_best_move(self.board)
                self.place_counter(bot_col_chosen)
                print(f"Robot's evaluation of current position (Positive = Better for you, Negative = Better for robot): {min_utility}")
                self.col_of_last_counter = bot_col_chosen
            self.print_board()
            self.switch_player()
        if not self.winner:
            print("Game has ended in a draw")
        elif self.winner == "1":
            print("Congratulations, you won!")
            print("-------------------------")
        else:
            print("Sorry, you lost, better luck next time!")
            print("---------------------------------------")


class ConnectFourBot(object):
    def __init__(self, first_player, player_1_char, player_2_char, bot_depth_of_search, is_minimiser):
        self.first_player = first_player
        self.player_1_char = player_1_char
        self.player_2_char = player_2_char
        self.is_minimiser = is_minimiser
        self.transposition_table = dict()
        self.bot_depth_of_search = bot_depth_of_search
        self.current_depth = 1

    def find_available_actions(self, board):
        available_actions = set()
        top_row = board[0]
        for col, slot in enumerate(top_row):
            if not slot:
                available_actions.add(col)
        return available_actions

    def find_result_of_action(self, board, action, is_minimiser):
        row = len(board) - 1
        moving_slot = board[row][action]
        while moving_slot:
            row -= 1
            if row < 0:
                raise Exception("Column selected was already filled to begin with, set of available actions are wrong")
            moving_slot = board[row][action]
        new_board = copy.deepcopy(board)
        if not is_minimiser:
            new_board[row][action] = self.player_1_char
        else:
            new_board[row][action] = self.player_2_char
        return new_board

    def find_winner(self, board):
        num_rows_in_board = len(board)
        num_cols_in_board = len(board[0])
        # check rows
        for row in board:
            col = 0
            slot_checked = row[col]
            while col <= num_cols_in_board - 4:
                if not slot_checked:
                    col += 1
                    slot_checked = row[col]
                    continue
                for count in range(4):
                    moving_slot = row[col]
                    if moving_slot != slot_checked:
                        slot_checked = moving_slot
                        break
                    col += 1
                else:   # did not break out of for loop
                    if slot_checked == self.player_1_char:
                        return "1"
                    return "2"
        # check columns
        for col in range(num_cols_in_board):
            row = 0
            slot_checked = board[row][col]
            while row <= num_rows_in_board - 4:
                if not slot_checked:
                    row += 1
                    slot_checked = board[row][col]
                    continue
                for count in range(4):
                    moving_slot = board[row][col]
                    if moving_slot != slot_checked:
                        slot_checked = moving_slot
                        break
                    row += 1
                else:  # did not break out of for loop
                    if slot_checked == self.player_1_char:
                        return "1"
                    return "2"
        # check first diagonal (/)
        first_diagonal_starting_points = list()
        for row in range(3, num_rows_in_board - 1):
            first_diagonal_starting_points.append((row, 0))
        for col in range(num_cols_in_board - 3):
            first_diagonal_starting_points.append((num_rows_in_board - 1, col))
        for starting_point in first_diagonal_starting_points:
            row, col = starting_point
            slot_checked = board[row][col]
            while row >= 3 and col <= num_cols_in_board - 4:
                if not slot_checked:
                    row -= 1
                    col += 1
                    slot_checked = board[row][col]
                    continue
                for count in range(4):
                    moving_slot = board[row][col]
                    if moving_slot != slot_checked:
                        slot_checked = moving_slot
                        break
                    row -= 1
                    col += 1
                else:  # did not break out of for loop
                    if slot_checked == self.player_1_char:
                        return "1"
                    return "2"
        # check second diagonal (\)
        second_diagonal_starting_points = list()
        for row in range(1, num_rows_in_board - 3):
            second_diagonal_starting_points.append((row, 0))
        for col in range(num_cols_in_board - 3):
            second_diagonal_starting_points.append((0, col))
        for starting_point in second_diagonal_starting_points:
            row, col = starting_point
            slot_checked = board[row][col]
            while row <= num_rows_in_board - 4 and col <= num_cols_in_board - 4:
                if not slot_checked:
                    row += 1
                    col += 1
                    slot_checked = board[row][col]
                    continue
                for count in range(4):
                    moving_slot = board[row][col]
                    if moving_slot != slot_checked:
                        slot_checked = moving_slot
                        break
                    row += 1
                    col += 1
                else:  # did not break out of for loop
                    if slot_checked == self.player_1_char:
                        return "1"
                    return "2"
        if not self.find_available_actions(board):     # game is a draw
            return "draw"
        return None

    def is_terminal_state(self, board):
        return bool(self.find_winner(board))

    def find_utility(self, terminal_board, current_depth):     # 100 for player 1 winning, 0 for draw, -100 for player 2 winning
        outcome = self.find_winner(terminal_board)
        if outcome == "1":
            return 10000 - current_depth
        if outcome == "2":
            return -10000 + current_depth
        return 0

    def find_row_weight(self, row, num_rows_in_board):
        return ((row + 1) / num_rows_in_board) + ((num_rows_in_board - 1) / (2 * num_rows_in_board))       # weighted by height of row; added additional term to standardise around 1

    def find_col_weight(self, col, num_cols_in_board):
        middle_column = ((num_cols_in_board + 1) // 2) - 1
        if col <= middle_column:
            column_weight = (col + 1) / (middle_column + 1)
        else:
            column_weight = (middle_column - (col - middle_column) + 1) / (middle_column + 1)
        return column_weight + (middle_column / (2 * middle_column + 2))        # weighted by distance from middle column; added additional term to standardise around 1

    def evaluation_function(self, board):
        num_rows_in_board = len(board)
        num_cols_in_board = len(board[0])
        player_1_score = 0
        player_2_score = 0
        # check rows
        for row_index in range(num_rows_in_board - 1, -1, -1):
            row = board[row_index]
            if self.player_1_char not in row and self.player_2_char not in row:
                break
            col = 0
            while col <= num_cols_in_board - 4:
                stretch_of_slots = dict()
                is_split = False
                for count in range(4):
                    slot = row[col + count]
                    if slot not in stretch_of_slots:
                        if (slot == self.player_1_char and self.player_2_char in stretch_of_slots) or (slot == self.player_2_char and self.player_1_char in stretch_of_slots):
                            break
                        stretch_of_slots[slot] = list()
                    if slot and stretch_of_slots[slot] and stretch_of_slots[slot][-1] + 1 < count:
                        is_split = True
                    stretch_of_slots[slot].append(count)
                else:       # did not break out of for loop
                    if self.player_1_char in stretch_of_slots:
                        num_non_empty_slots_in_stretch = len(stretch_of_slots[self.player_1_char])
                        raw_score = num_non_empty_slots_in_stretch * 2 - 1
                        if is_split:
                            raw_score -= 1
                        player_1_score_gained = raw_score * self.find_row_weight(row_index, num_rows_in_board)
                        player_1_score += player_1_score_gained
                        player_2_score -= player_1_score_gained
                    elif self.player_2_char in stretch_of_slots:
                        num_non_empty_slots_in_stretch = len(stretch_of_slots[self.player_2_char])
                        raw_score = num_non_empty_slots_in_stretch * 2 - 1
                        if is_split:
                            raw_score -= 1
                        player_2_score_gained = raw_score * self.find_row_weight(row_index, num_rows_in_board)
                        player_2_score += player_2_score_gained
                        player_1_score -= player_2_score_gained
                col += 1
        # check columns
        for col in range(num_cols_in_board):
            bottom_slot = board[num_rows_in_board - 1][col]
            if not bottom_slot:
                continue
            row = num_rows_in_board - 1
            lowest_empty_row = -1
            while row >= 3:
                if row == lowest_empty_row:
                    break
                stretch_of_slots = dict()
                is_successful_stretch = True
                for count in range(4):
                    slot = board[row - count][col]
                    if slot not in stretch_of_slots:
                        if not slot:
                            if lowest_empty_row == -1:
                                lowest_empty_row = row - count
                                break
                        if (slot == self.player_1_char and self.player_2_char in stretch_of_slots) or (slot == self.player_2_char and self.player_1_char in stretch_of_slots):
                            is_successful_stretch = False
                            break
                        stretch_of_slots[slot] = 0
                    stretch_of_slots[slot] += 1
                if is_successful_stretch:
                    if self.player_1_char in stretch_of_slots:
                        num_non_empty_slots_in_stretch = stretch_of_slots[self.player_1_char]
                        raw_score = num_non_empty_slots_in_stretch * 2 - 1
                        player_1_score_gained = raw_score * self.find_col_weight(col, num_cols_in_board)
                        player_1_score += player_1_score_gained
                        player_2_score -= player_1_score_gained
                    else:   # self.player_2_char in stretch_of_slots
                        num_non_empty_slots_in_stretch = stretch_of_slots[self.player_2_char]
                        raw_score = num_non_empty_slots_in_stretch * 2 - 1
                        player_2_score_gained = raw_score * self.find_col_weight(col, num_cols_in_board)
                        player_2_score += player_2_score_gained
                        player_1_score -= player_2_score_gained
                row -= 1
        # check first diagonal (/)
        first_diagonal_starting_points = list()
        for row in range(3, num_rows_in_board - 1):
            first_diagonal_starting_points.append((row, 0))
        for col in range(num_cols_in_board - 3):
            first_diagonal_starting_points.append((num_rows_in_board - 1, col))
        for starting_point in first_diagonal_starting_points:
            row, col = starting_point
            while row >= 3 and col <= num_cols_in_board - 4:
                stretch_of_slots = dict()
                is_split = False
                for count in range(4):
                    slot = board[row - count][col + count]
                    if slot not in stretch_of_slots:
                        stretch_of_slots[slot] = list()
                    if slot and stretch_of_slots[slot] and stretch_of_slots[slot][-1] + 1 < count:
                        is_split = True
                    stretch_of_slots[slot].append(count)
                if self.player_1_char in stretch_of_slots and self.player_2_char in stretch_of_slots:
                    row -= 1
                    col += 1
                    continue
                if self.player_1_char not in stretch_of_slots and self.player_2_char not in stretch_of_slots:
                    row -= 1
                    col += 1
                    continue
                if self.player_1_char in stretch_of_slots:
                    num_non_empty_slots_in_stretch = len(stretch_of_slots[self.player_1_char])
                    raw_score = num_non_empty_slots_in_stretch * 2 - 1
                    if is_split:
                        raw_score -= 1
                    player_1_score_gained = raw_score
                    player_1_score += player_1_score_gained
                    player_2_score -= player_1_score_gained
                else:  # self.player_2_char in stretch_of_slots
                    num_non_empty_slots_in_stretch = len(stretch_of_slots[self.player_2_char])
                    raw_score = num_non_empty_slots_in_stretch * 2 - 1
                    if is_split:
                        raw_score -= 1
                    player_2_score_gained = raw_score
                    player_2_score += player_2_score_gained
                    player_1_score -= player_2_score_gained
                row -= 1
                col += 1
        # check second diagonal (\)
        second_diagonal_starting_points = list()
        for row in range(1, num_rows_in_board - 3):
            second_diagonal_starting_points.append((row, 0))
        for col in range(num_cols_in_board - 3):
            second_diagonal_starting_points.append((0, col))
        for starting_point in second_diagonal_starting_points:
            row, col = starting_point
            while row <= num_rows_in_board - 4 and col <= num_cols_in_board - 4:
                stretch_of_slots = dict()
                is_split = False
                for count in range(4):
                    slot = board[row + count][col + count]
                    if slot not in stretch_of_slots:
                        stretch_of_slots[slot] = list()
                    if slot and stretch_of_slots[slot] and stretch_of_slots[slot][-1] + 1 < count:
                        is_split = True
                    stretch_of_slots[slot].append(count)
                if self.player_1_char in stretch_of_slots and self.player_2_char in stretch_of_slots:
                    row += 1
                    col += 1
                    continue
                if self.player_1_char not in stretch_of_slots and self.player_2_char not in stretch_of_slots:
                    row += 1
                    col += 1
                    continue
                if self.player_1_char in stretch_of_slots:
                    num_non_empty_slots_in_stretch = len(stretch_of_slots[self.player_1_char])
                    raw_score = num_non_empty_slots_in_stretch * 2 - 1
                    if is_split:
                        raw_score -= 1
                    player_1_score_gained = raw_score
                    player_1_score += player_1_score_gained
                    player_2_score -= player_1_score_gained
                else:  # self.player_2_char in stretch_of_slots
                    num_non_empty_slots_in_stretch = len(stretch_of_slots[self.player_2_char])
                    raw_score = num_non_empty_slots_in_stretch * 2 - 1
                    if is_split:
                        raw_score -= 1
                    player_2_score_gained = raw_score
                    player_2_score += player_2_score_gained
                    player_1_score -= player_2_score_gained
                row += 1
                col += 1
        return player_1_score    # player 2 is looking to minimise utility

    def convert_board_to_tuple(self, board):
        tuple_sequence = list()
        for row in board:
            for slot in row:
                tuple_sequence.append(slot)
        tuple_sequence = tuple(tuple_sequence)
        return tuple_sequence

    def alpha_beta_pruning(self, board, is_minimiser, alpha, beta, current_depth, max_depth):
        board_state = self.convert_board_to_tuple(board)
        board_state_is_in_table = False
        if board_state in self.transposition_table:
            board_state_is_in_table = True
            stored_utility, best_action, max_depth_searched_to_produce_info, nature_of_stored_utility = self.transposition_table[board_state]
            if max_depth_searched_to_produce_info >= max_depth:
                if nature_of_stored_utility == "exact":
                    return stored_utility, best_action
                if nature_of_stored_utility == "upper bound" and stored_utility <= alpha:
                    return stored_utility, best_action
                if nature_of_stored_utility == "lower bound" and stored_utility >= beta:
                    return stored_utility, best_action
        if self.is_terminal_state(board):
            info_stored_in_table = (self.find_utility(board, current_depth), -1, max_depth, "exact")  # no action can be taken in terminal state
            self.transposition_table[board_state] = info_stored_in_table
            return info_stored_in_table[0], info_stored_in_table[1]
        if current_depth == max_depth:
            info_stored_in_table = (self.evaluation_function(board), -1, max_depth, "exact")  # no action is required at max depth
            self.transposition_table[board_state] = info_stored_in_table
            return info_stored_in_table[0], info_stored_in_table[1]
        available_actions = self.find_available_actions(board)
        if board_state_is_in_table:
            recorded_best_action = self.transposition_table[board_state][1]
            if recorded_best_action != -1:
                available_actions.remove(recorded_best_action)
                available_actions = [recorded_best_action] + list(available_actions)
        if is_minimiser:
            min_utility = float("inf")
            best_action = -1
            is_exact_utility = True
            for action in available_actions:
                possible_min_utility, next_player_best_action = self.alpha_beta_pruning(self.find_result_of_action(board, action, is_minimiser=True), False, alpha, beta, current_depth=current_depth + 1, max_depth=max_depth)
                if possible_min_utility < min_utility:
                    min_utility = possible_min_utility
                    best_action = action
                beta = min(beta, possible_min_utility)
                if alpha >= beta:
                    is_exact_utility = False
                    break
            if is_exact_utility:
                nature_of_stored_utility = "exact"
            else:
                nature_of_stored_utility = "upper bound"
            info_stored_in_table = (min_utility, best_action, max_depth, nature_of_stored_utility)
            self.transposition_table[board_state] = info_stored_in_table
            return info_stored_in_table[0], info_stored_in_table[1]
        else:
            max_utility = float("-inf")
            best_action = -1
            is_exact_utility = True
            for action in available_actions:
                possible_max_utility, next_player_best_action = self.alpha_beta_pruning(self.find_result_of_action(board, action, is_minimiser=False), True, alpha, beta, current_depth=current_depth + 1, max_depth=max_depth)
                if possible_max_utility > max_utility:
                    max_utility = possible_max_utility
                    best_action = action
                alpha = max(alpha, possible_max_utility)
                if alpha >= beta:
                    is_exact_utility = False
                    break
            if is_exact_utility:
                nature_of_stored_utility = "exact"
            else:
                nature_of_stored_utility = "lower bound"
            info_stored_in_table = (max_utility, best_action, max_depth, nature_of_stored_utility)
            self.transposition_table[board_state] = info_stored_in_table
            return info_stored_in_table[0], info_stored_in_table[1]

    def find_best_move(self, board):
        alpha = float("-inf")
        beta = float("inf")
        if self.is_minimiser:
            min_utility, best_action = self.alpha_beta_pruning(board, True, alpha, beta, current_depth=self.current_depth, max_depth=self.current_depth + self.bot_depth_of_search)
            self.current_depth += 2
            return min_utility, best_action
        max_utility, best_action = self.alpha_beta_pruning(board, False, alpha, beta, current_depth=self.current_depth, max_depth=self.current_depth + self.bot_depth_of_search)
        self.current_depth += 2
        return max_utility, best_action


if __name__ == '__main__':
    print("Welcome to Connect Four :D")
    human_start_first_str = input("Would you like to start first? Y/N: ").lower()
    while human_start_first_str not in ["y", "n"]:
        print("Invalid input!")
        human_start_first_str = input("Would you like to start first? Y/N: ").lower()
    if human_start_first_str == "y":
        start_first = "1"
    else:
        start_first = "2"
    depth_of_search_str = input("Set the depth of search of the robot (Enter a positive integer less than 10): ")
    while True:
        try:
            depth_of_search = int(depth_of_search_str)
        except ValueError:
            print("Invalid input!")
        else:
            if depth_of_search >= 10 or depth_of_search <= 0:
                print("Depth of search outside of accepted range!")
            else:
                break
        depth_of_search_str = input("Set the depth of search of the robot (Enter a positive integer less than 10): ")
    print()
    game = ConnectFour(first_player=start_first, bot_depth_of_search=depth_of_search)
    game.play()
    end = input("Enter any key to quit: ")
