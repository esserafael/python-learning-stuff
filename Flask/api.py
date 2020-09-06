import flask
from flask import request, jsonify

class RequestError:
    def __init__(self, code, request):
        self.code = code
        self.message = f"The request with argument {request.args.to_dict()} does not exist."   
        

app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route("/", methods=["GET"])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route("/glub", methods=["GET"])
def glub():
    return "<h1>Você caiu no glub glub do galão de água.</h1>"

@app.route("/v1/books/all", methods=["GET"])
def all_books():
    return jsonify(books)

@app.route("/v1/books", methods=["GET"])
def books_search():
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return jsonify(RequestError("BadRequest", request).__dict__)

    results = [book for book in books if book["id"] == id]

    return jsonify(results)

app.run()