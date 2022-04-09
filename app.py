
from flask import Flask, redirect
from flask import render_template as render
from flask import request
import requests
from data import data as databank

from datetime import datetime
api_key = "eb14bb8013e84541b3bc433899f28f27"

app = Flask(__name__)

def few_words(val):
    if type(val) != type(""):
        val = str(val)
    val = val.split()
    num = len(val)
    new = []
    if num >= 20:
        for x, i in zip(val, range(len(val))):
            if i < 20:
                new.append(x)
            else:
                new.append(' ...')
                break
        return ' '.join(new)         
    else:
        remaining = 20 - len(val)
        remaining = [ "  " for x in range(remaining - 1) ] +[" ..."]

        return ' '.join(val + remaining)

app.jinja_env.globals.update(few_words = few_words)

@app.route("/")
@app.route("/headlines", methods=["GET"])
def index():
    try:
        url = ('https://newsapi.org/v2/top-headlines?'+
            'country=us&'+
            f'apiKey={api_key}')
        res = requests.get(url).json()
    except:
        res = {"articles" : [{"title" : "", "description" : f"no news found", "source":""}]}
    return render("index.html",title='headlines' ,data = res)
    
@app.route("/search")
def search():
    q = request.args.get('search')

    
    if q == None or q.strip() == ""  :
        data = {"articles" : [{"title" : "", "description" : "enter keyword to search", "source":""}]}
      
    else:
        try:
            date=str(datetime.now()).split(" ")[0]
            qr = requests.utils.quote(q.encode("utf-8"))
            url = ('https://newsapi.org/v2/everything?'+
        f'q={qr}&'+
        'from={date}&'+
        'sortBy=popularity&'+
            f'apiKey={api_key}')
            data = requests.get(url).json()
        except:
            data  = {"articles" : [{"title" : "", "description" : f"no result found for search {q}", "source":""}]}
        
        q = str(q).strip() 
        
    return render('search.html',title='search', data = data, query = q if q != None and q != "" else '')
        
@app.route('/about')    
def about():
   return render('about.html')
   


if __name__ == "__main__": 
    app.run(debug = True)