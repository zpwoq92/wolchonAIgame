import streamlit as st
import numpy as np
import random

class GomokuAI:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
    def is_winner(self, player):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.check_direction(x, y, 1, 0, player) or \
                   self.check_direction(x, y, 0, 1, player) or \
                   self.check_direction(x, y, 1, 1, player) or \
                   self.check_direction(x, y, 1, -1, player):
                    return True
        return False
    def check_direction(self, x, y, dx, dy, player):
        count = 0
        for i in range(5):
            if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == player:
                count += 1
                if count == 5:
                    return True
            else:
                break
            x += dx
            y += dy
        return False
    def get_valid_moves(self):
        moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    moves.append((x, y))
        return moves
    def make_move(self, move, player):
        x, y = move
        if self.board[x][y] == 0:
            self.board[x][y] = player
            return True
        return False
    def ai_move(self):
        moves = self.get_valid_moves()
        # 간단한 랜덤 AI (여기에 Minimax 등으로 교체하면 됩니다)
        if moves:
            move = random.choice(moves)
            self.make_move(move, 2)
            return move
        return None

# Streamlit 어플리케이션
st.title("오목 게임 (Gomoku)")

SIZE = 9  # 15x15은 너무 큼, 9x9로 줄임(화면에 맞게)
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'gomoku' not in st.session_state:
    st.session_state.gomoku = GomokuAI(SIZE)
if 'turn' not in st.session_state:
    st.session_state.turn = 1  # 1: 흑, 2: 백

if st.session_state.mode is None:
    st.session_state.gomoku = GomokuAI(SIZE)
    st.session_state.turn = 1
    st.session_state.winner = None
    st.write("게임 모드를 선택하세요.")
    if st.button("1인용: AI와 대결"):
        st.session_state.mode = "ai"
    if st.button("2인용: 친구와 대결"):
        st.session_state.mode = "pvsp"
else:
    gomoku = st.session_state.gomoku
    winner = getattr(st.session_state, 'winner', None)
    if st.button("🔄 게임 다시 시작"):
        st.session_state.gomoku = GomokuAI(SIZE)
        st.session_state.turn = 1
        st.session_state.winner = None
        st.experimental_rerun()
    board = gomoku.board
    columns = st.columns(SIZE)
    for i in range(SIZE):
        with columns[i]:
            for j in range(SIZE):
                cell = board[i][j]
                label = ""
                if cell == 1:
                    label = "⚫"
                elif cell == 2:
                    label = "⚪"
                if winner or cell != 0:
                    st.button(label if label else " ", key=f"{i}_{j}", disabled=True)
                else:
                    if st.button(label if label else " ", key=f"{i}_{j}"):
                        if not winner and gomoku.make_move((i, j), st.session_state.turn):
                            if gomoku.is_winner(st.session_state.turn):
                                st.session_state.winner = st.session_state.turn
                            elif st.session_state.mode == "ai" and st.session_state.turn == 1:
                                # AI 차례
                                ai_move = gomoku.ai_move()
                                if ai_move and gomoku.is_winner(2):
                                    st.session_state.winner = 2
                            else:
                                st.session_state.turn = 3 - st.session_state.turn
                            st.experimental_rerun()
    # 상태 표시
    if st.session_state.mode == "ai":
        st.write("1인용: 흑(⚫)은 여러분, 백(⚪)은 AI입니다.")
    else:
        st.write("2인용: 친구와 번갈아 두세요 (흑:⚫ / 백:⚪)")
    if winner:
        st.success(f"{'⚫' if winner==1 else '⚪'} 승리!")

    if st.button("메뉴로 돌아가기"):
        st.session_state.mode = None
        st.session_state.winner = None
        st.experimental_rerun()
