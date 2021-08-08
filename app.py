from flask import Flask,render_template,url_for,request
from werkzeug.utils import redirect
from myanimelyrics import search_lyrics
import urllib.request
import re
import random
# from flask.wrappers import Request

app = Flask(__name__)

def myanilyrics(query,lang):
    lyrics_response = "N/A"
    try:
        lyrics_response, title_response = search_lyrics(query,lang)
        # mytext = "<br>".join(lyrics_response.split("\n"))
        lyrics_response = lyrics_response.replace('\n', '<br>')
        return lyrics_response, title_response
    except:
        return "Some error occured or service N/A"

@app.route('/',methods=['POST','GET'])
def index():
    ly_jp=''
    ly_en=''
    song_name = 'Title'
    song_by = 'Artist'
    firstvideo_id = 'https://www.youtube.com/embed/dQw4w9WgXcQ'
    if request.method == 'POST':
        searchQuery = request.form['searchbar']
        if searchQuery:
            ly_jp, song_name = myanilyrics(searchQuery,"jp")
            ly_en, song_name = myanilyrics(searchQuery,"en")

            search_vid = song_name.replace(" ","-")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_vid)
            # # print(html.read().decode())
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            # print(video_ids)
            firstvideo_id = "https://www.youtube.com/embed/" + random.choice(video_ids)
            # return redirect('/')
            return render_template("index.html",song_name = song_name,song_by = song_by,ly_jp = ly_jp, ly_en = ly_en, firstvideo_id = firstvideo_id)
        else:
            return redirect('/')
    else:
        return render_template("index.html",song_name = song_name,song_by = song_by,ly_jp = ly_jp, ly_en = ly_en, firstvideo_id = firstvideo_id)

if __name__ == "__main__":
    app.run(debug=True)
