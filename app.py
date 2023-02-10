from flask import Flask, request, render_template, redirect, jsonify, session

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

from boggle import Boggle

boggle_game = Boggle()

@app.route('/')
def home():
    """Show board."""
    #board should be in a session
    #use jinja - use an html template (index.html)
    
    #call the make_board method
    board = boggle_game.make_board()
    
    #store the board in a session
    session['board'] = board
    
    
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    #use jinja to call the html template. 
    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)
    

@app.route("/check-word", methods=['GET'])
def check_word():
    """Check if word is in dictionary."""
  
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})
    
    
    # post = request.get_json()
    # word = post['word']
    # board= session["board"]
    # validity = boggle_game.check_valid_word(board,word)
    # print(validity)
    # return validity 
    
@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)