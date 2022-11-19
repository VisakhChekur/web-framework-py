# Web Framework

This is an implementation of a backend framework in Python similar to Flask made purely for the purpose of scratching my itch to understand such frameworks a bit better.

# Features

- provide custom paths with for each method in a controller

  - NOTE: each path provided is suffixed with the controller name in the url (refer example for a more clear understanding)

- allow multiple HTTP methods in each path

  - if HTTP methods are not provided, then the method name itself must match an HTTP method

- modify headers and other details directly on the response object

- all responses will have content-type as 'application/json' by default but that can be changed

# Stuff I Want to Improve/Make

- routing
  - I don't like the way i've implemented it
  - I want to change it so that variables can be supported
    - example: /user/{id: int} should allow the user to access a variable called 'id' within the method

**NOTE: If someone could help point me in the right direction on how I could improve the routing system I have, I would greatly appreciate that.**

# Example

```python
# imports assuming we are in the same directory as src
from app import App
from base_controller import BaseController
from http_parser.request import Request
from http_parser.response import Response

app = App()

# all controllers need to inherit from BaseController
# actually I don't think it needs to be for it work, but
# it was how I set it up in an earlier implementation
# also it helps with type hinting
class User(BaseController):

    # HTTP method supported will automatically be only GET
    @app.route("users")
    def get(self, req: Request, resp: Response):

        # logic goes here
        # no need to return anything
        # the response object, `resp`, will be automatically
        # used as the HTTP response

    @app.route("user/add", methods=["POST"])
    def add_user(self, req: Request, resp: Response):

        # logic

# register_controller needs an intance of the Controller class
app.register_controller(User())

if __name__ == "__main__":

    app.run()
```
