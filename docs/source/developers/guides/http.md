# Verifying HTTP requests

You can use the {py:func}`labs.common.http.check_http_response_step` function to verify the response of HTTP requests.

For example, to validate that a URL returns a 200 response code, you can use the `check_http_response_step` function as follows:

```python
from labs.activities import GuidedExercise
from labs.common.http import check_http_response_step

class ExampleLabScript(GuidedExercise):
    __LAB__ = "example"

    def grade(self):
        check_http_response_step("http://example.com")
```

You can specify the expected response code.
For example, you might want to verify that a particular URL returns a 404 code.

```python
check_http_response_step(
    "http://example.com", 
    response_code_is=404
)
```

You might also want to validate that the response includes a particular substring:

```python
check_http_response_step(
    "http://example.com", 
    response_body_includes="Hello"
)
```

You can combine both conditions:

```python
check_http_response_step(
    "http://example.com",
    response_code_is=404,
    response_body_includes="not found"
)
```

Similarly to other step functions, you can customize the step message, and whether the step is grading and fatal:

```python
check_http_response_step(
    "http://example.com",
    message="Verifying my example app",
    grading=False,
    fatal=False
)
```

## Making HTTP requests

DynoLabs also provides the {py:func}`labs.common.http.make_request` function to send HTTP requests.
This function wraps the `requests` library by adding error handling code that sends stack traces to the logs.
You can use this function as follows:

```python
from labs.common.http import make_request, HttpRequestError

// ...

with Step("my step") as step:
    try:
        response = make_request("http://example.com")
    except HttpRequestError as exception:
        # No need to log anything because "makes_request" sends the error to the logs
        return step.add_error(str(exception))

    body = response.json()
```

Note that even though the function logs the errors, it will still raise the `HttpRequestError` so that you can, for example, mark your step as failed.
