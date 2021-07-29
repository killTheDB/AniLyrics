from flask import Flask,render_template,url_for,request
from werkzeug.utils import redirect
from myanimelyrics import search_lyrics
# from flask.wrappers import Request

app = Flask(__name__)

def myanilyrics(query,lang):
    lyrics_response = "N/A"
    try:
        lyrics_response = search_lyrics(query,lang)
        return lyrics_response
    except:
        return "Some error occured or service N/A"

@app.route('/',methods=['POST','GET'])
def index():
    ly_jp=''
    ly_en=''
    if request.method == 'POST':
        searchQuery = request.form['searchbar']
        if searchQuery:
            ly_jp = myanilyrics(searchQuery,"jp")
            ly_en = myanilyrics(searchQuery,"en")
            # print(ly_jp)
            # return redirect('/')
            return render_template("index.html",ly_jp = ly_jp, ly_en = ly_en)
        else:
            return redirect('/')
    else:
        return render_template("index.html",ly_jp = ly_jp, ly_en = ly_en)

if __name__ == "__main__":
    app.run(debug=True)
