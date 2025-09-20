from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the board
board = [""] * 9
current_player = "X"

def check_winner(b):
    # All winning combinations
    wins = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for w in wins:
        if b[w[0]] == b[w[1]] == b[w[2]] != "":
            return b[w[0]]
    if "" not in b:
        return "Draw"
    return None

@app.route("/")
def index():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return render_template("main.html")

@app.route("/move", methods=["POST"])
def move():
    global board, current_player
    data = request.get_json()
    idx = int(data["index"])
    
    if board[idx] != "":
        return jsonify({"status":"invalid"})
    
    board[idx] = current_player
    winner = check_winner(board)
    
    if winner:
        return jsonify({"status":"win", "winner": winner, "board": board})
    
    # Switch player
    current_player = "O" if current_player == "X" else "X"
    return jsonify({"status":"ok", "board": board, "current_player": current_player})

if __name__ == "__main__":
    app.run(debug=True)
