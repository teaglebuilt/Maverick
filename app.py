from src.maverick import API


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

@app.route("/age/{age:d}")
def tell_age(request, response, age):
	response.text = f"Your age is {age}"
	

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


def contact_me(request, response):
	response.text = "Contact me"


app.add_route('/contact', contact_me)


def custom_exception_handler(request, response, exception_cls):
    response.text = "Oops! Something went wrong. Please, contact our customer support at +1-202-555-0127."

app.add_exception_handler(custom_exception_handler)

@app.route("/home")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be user")