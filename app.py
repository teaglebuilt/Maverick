from src import API


app = API()


@app.route('/')
def home(request, response):
	response.text = "Hello from home page"

@app.route('/about')
def about(request, response):
	response.text = "Hello from the About Page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/tell/{age}")
def age(request, response, age):
	response.text = f"Age is {age}"


@app.route("/posts")
class PostHandler:

	def get(self, request, response):
		response.text = "Posts Page"

	def post(self, request, response):
		response.text = "endpoint to create post"


@app.route('/show/template')
def handler_with_template(request, response):
	response.text = app.template("example.html", context={"title": "Test title", "body": "Testing body content"})
	response.content_type = "text/html"