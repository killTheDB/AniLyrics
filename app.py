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
        lyrics_response = search_lyrics(query,lang)
        # mytext = "<br>".join(lyrics_response.split("\n"))
        lyrics_response = lyrics_response.replace('\n', '<br>')
        return lyrics_response
    except:
        return "Some error occured or service N/A"

@app.route('/',methods=['POST','GET'])
def index():
    ly_jp=''
    ly_en=''
    firstvideo_id = 'https://www.youtube.com/embed/dQw4w9WgXcQ'
    if request.method == 'POST':
        searchQuery = request.form['searchbar']
        if searchQuery:
            ly_jp = myanilyrics(searchQuery,"jp")
            ly_en = myanilyrics(searchQuery,"en")
            searchly_jp = ly_jp
            searchly_jp = searchly_jp.replace('<br>', '\n')
            jply = ''
            # jply += searchly_jp.split('\n')[0]+' '+searchly_jp.split('\n')[1]+' '+searchly_jp.split('\n')[2]+' '+searchly_jp.split('\n')[3]+' '
            res = searchly_jp.split('\n')
            # print(res)
            for line in range(0,4):
                if line != '\n':
                    jply = jply + res[line]

            # print(ly_jp)
            # print(ly_en)
            # print(searchly_jp)
            # print(searchly_en)
            jply = jply.replace("\xa0", "+").strip()
            jply = jply.replace("\r", "+").strip()
            print(jply)
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + jply)
            # # print(html.read().decode())
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            print(video_ids)
            firstvideo_id = "https://www.youtube.com/embed/" + random.choice(video_ids)
            # return redirect('/')
            return render_template("index.html",ly_jp = ly_jp, ly_en = ly_en, firstvideo_id = firstvideo_id)
        else:
            return redirect('/')
    else:
        return render_template("index.html",ly_jp = ly_jp, ly_en = ly_en, firstvideo_id = firstvideo_id)

if __name__ == "__main__":
    app.run(debug=True)
