import streamlit as st
import numpy as np
import random

BOARD_SIZE = 9  # 9x9, 더 크게도 가능

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

# --- Streamlit 상태 관리 ---
if 'mode' not in st.session_state:
    st.session_state['mode'] = None
if 'game' not in st.session_state:
    st.session_state['game'] = GomokuAI()
if 'turn' not in st.session_state:
    st.session_state['turn'] = 1  # 1=흑, 2=백
if 'winner' not in st.session_state:
    st.session_state['winner'] = None

st.title("🟦 오목(Gomoku)")

# 모드 선택
if st.session_state['mode'] is None:
    st.write("게임 모드를 선택하세요.")
    cl1, cl2 = st.columns(2)
    with cl1:
        if st.button("1인용 (AI와 대결)"):
            st.session_state['mode'] = 'ai'
            st.session_state['game'] = GomokuAI()
            st.session_state['turn'] = 1
            st.session_state['winner'] = None
    with cl2:
        if st.button("2인용 (친구와 대결)"):
            st.session_state['mode'] = 'pvsp'
            st.session_state['game'] = GomokuAI()
            st.session_state['turn'] = 1
            st.session_state['winner'] = None
    st.stop()  # 모드 선택 후 종료

gomoku = st.session_state['game']
turn = st.session_state['turn']
winner = st.session_state['winner']

def new_game():
    st.session_state['game'] = GomokuAI()
    st.session_state['turn'] = 1
    st.session_state['winner'] = None

if st.button("🔄 게임 다시 시작"):
    new_game()
    st.experimental_rerun()

# --- 격자점 위 돌 표시 (테이블 형태) ---
def stone_emoji(val):
    if val == 1:
        return "⚫"  # 흑
    elif val == 2:
        return "⚪"  # 백
    else:
        return "△"  # 빈 격자점 (작은 삼각형: 마치 교차점처럼)

board = gomoku.board

st.write(f"**{'AI(백)' if st.session_state['mode']=='ai' and turn==2 else '플레이어'} 차례: {'⚫' if turn==1 else '⚪'}**")
if winner:
    st.success(f"{'⚫' if winner == 1 else '⚪'} 승리!")
    st.write("게임을 새로 시작하려면 위의 버튼을 누르세요.")

# interactive 오목판
for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        disp = stone_emoji(board[i, j])
        disabled = (winner is not None) or (board[i, j] != 0)
        # 버튼에 교차점 이모지로!
        if st.session_state['mode'] == "pvsp" or (st.session_state['mode'] == "ai" and turn == 1):
            if cols[j].button(disp, key=f"{i}_{j}", disabled=disabled):
                if gomoku.make_move((i, j), turn):
                    if gomoku.is_winner(turn):
                        st.session_state['winner'] = turn
                    else:
                        st.session_state['turn'] = 2 if turn == 1 else 1
                    st.experimental_rerun()
        else:  # AI 차례
            cols[j].write(disp)

# AI 동작
if st.session_state['mode'] == "ai" and turn == 2 and winner is None:
    move = gomoku.ai_move()
    if gomoku.is_winner(2):
        st.session_state['winner'] = 2
    else:
        st.session_state['turn'] = 1
    st.experimental_rerun()

if st.button("메뉴로 돌아가기"):
    st.session_state['mode'] = None
    st.experimental_rerun()

st.caption("⚫ : 흑(플레이어1), ⚪ : 백(플레이어2/AI), △ : 빈 격자점")
