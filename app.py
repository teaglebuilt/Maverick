from api import API


app = API()


@app.route('/')
def home(request, response):
	response.text = "Hello from home page"

@app.route('/about')
def about(request, response):
	response.text = "Hello from the About Page"