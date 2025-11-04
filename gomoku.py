import streamlit as st
import numpy as np
import random

BOARD_SIZE = 9

def create_board():
    return np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

class GomokuAI:
    def __init__(self):
        self.board = create_board()
    def is_winner(self, player):
        bs = BOARD_SIZE
        b = self.board
        for x in range(bs):
            for y in range(bs):
                for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
                    count = 0
                    for k in range(5):
                        nx, ny = x+dx*k, y+dy*k
                        if 0 <= nx < bs and 0 <= ny < bs and b[nx][ny] == player:
                            count += 1
                        else:
                            break
                    if count == 5:
                        return True
        return False
    def get_valid_moves(self):
        return [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if self.board[x][y] == 0]
    def make_move(self, move, player):
        x, y = move
        if self.board[x][y] == 0:
            self.board[x][y] = player
            return True
        return False
    def ai_move(self):
        valid = self.get_valid_moves()
        if valid:
            move = random.choice(valid)
            self.make_move(move, 2)
            return move
        return None

# 세션 상태 초기화
if 'mode' not in st.session_state:
    st.session_state['mode'] = None
if 'game' not in st.session_state:
    st.session_state['game'] = GomokuAI()
if 'turn' not in st.session_state:
    st.session_state['turn'] = 1
if 'winner' not in st.session_state:
    st.session_state['winner'] = None

st.title("🟦 오목(Gomoku)")

def stone_emoji(val):
    if val == 1:
        return "⚫"
    elif val == 2:
        return "⚪"
    else:
        return "△"

def reset_game():
    st.session_state['game'] = GomokuAI()
    st.session_state['turn'] = 1
    st.session_state['winner'] = None

# 모드 선택
if st.session_state['mode'] is None:
    st.write("게임 모드를 선택하세요.")
    cl1, cl2 = st.columns(2)
    with cl1:
        if st.button("1인용 (AI와 대결)"):
            st.session_state['mode'] = 'ai'
            reset_game()
            st.stop()
    with cl2:
        if st.button("2인용 (친구와 대결)"):
            st.session_state['mode'] = 'pvsp'
            reset_game()
            st.stop()

gomoku = st.session_state['game']
turn = st.session_state['turn']
winner = st.session_state['winner']

if st.button("🔄 게임 다시 시작"):
    reset_game()
    st.stop()

st.write(f"**{'AI(백)' if st.session_state['mode']=='ai' and turn==2 else '플레이어'} 차례: {'⚫' if turn==1 else '⚪'}**")
if winner:
    st.success(f"{'⚫' if winner == 1 else '⚪'} 승리!")
    st.write("게임을 새로 시작하려면 위의 버튼을 누르세요.")

board = gomoku.board

clicked = False

for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        disp = stone_emoji(board[i, j])
        disabled = (winner is not None) or (board[i, j] != 0)
        btn_id = f"{i}-{j}-{board.sum()}" # btn_id도 매번 새로 생성
        if st.session_state['mode'] == "pvsp" or (st.session_state['mode'] == "ai" and turn == 1):
            if cols[j].button(disp, key=btn_id, disabled=disabled):
                if gomoku.make_move((i, j), turn):
                    if gomoku.is_winner(turn):
                        st.session_state['winner'] = turn
                    else:
                        st.session_state['turn'] = 2 if turn == 1 else 1
                    clicked = True
        else:
            cols[j].write(disp)

# 턴이 넘어갔으면 한 번만 rerun
if clicked:
    st.stop()

# AI 자동수 (오류 최소를 위해 마지막에만!)
if st.session_state['mode'] == "ai" and turn == 2 and not winner:
    gomoku.ai_move()
    if gomoku.is_winner(2):
        st.session_state['winner'] = 2
    st.session_state['turn'] = 1
    st.stop()

if st.button("메뉴로 돌아가기"):
    st.session_state['mode'] = None
    st.stop()

st.caption("⚫ : 흑(플레이어1), ⚪ : 백(플레이어2/AI), △ : 빈 격자점")
