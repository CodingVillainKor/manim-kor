def check_next(board, now_pos):
    num_row, num_col = len(board), len(board[0])
    now_r, now_c = now_pos
    can_go = []
    if now_r!=0         and board[now_r-1][now_c] == 0:
        can_go.append([now_r-1, now_c])
    if now_r+1!=num_row and board[now_r+1][now_c] == 0:
        can_go.append([now_r+1, now_c])
    if now_c!=0         and board[now_r][now_c-1] == 0:
        can_go.append([now_r, now_c-1])
    if now_c+1!=num_col and board[now_r][now_c+1] == 0:
        can_go.append([now_r, now_c+1])
    return can_go

def solution(board, start, end):
    board[start[0]][start[1]] = 2
    can_go_list = [start]
    while can_go_list:
        position_now = can_go_list.pop()
        board[position_now[0]][position_now[1]] = 2
        can_go_list.extend(check_next(board, position_now))
        if end in can_go_list:
            return "YES"
    return "NO"