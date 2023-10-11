from labs.common.http import check_http_response_step


def test__http_request_connection_fails():
    step = check_http_response_step("http://0.0.0.1", fatal=False)
    assert step.has_failed()
    assert "Error connecting to" in step.secondary_messages[0]


def test__http_request_expects_200(httpserver):
    httpserver.expect_request("/").respond_with_data(status=200)
    url = httpserver.url_for("/")

    step = check_http_response_step(url)
    step.has_succeeded()


def test__http_request_expects_200_explict(httpserver):
    httpserver.expect_request("/").respond_with_data(status=200)
    url = httpserver.url_for("/")

    step = check_http_response_step(url, response_code_is=200)
    step.has_succeeded()


def test__http_request_fails_expecting_200(httpserver):
    httpserver.expect_request("/").respond_with_data(status=404)
    url = httpserver.url_for("/")

    step = check_http_response_step(url, fatal=False)
    assert step.has_failed()


def test__http_request_expects_404(httpserver):
    httpserver.expect_request("/").respond_with_data(status=404)
    url = httpserver.url_for("/")

    step = check_http_response_step(url, response_code_is=404)
    assert step.has_succeeded()


def test__http_request_expects_body(httpserver):
    httpserver.expect_request("/").respond_with_data("Hello there", status=200)
    url = httpserver.url_for("/")

    step = check_http_response_step(url, response_body_includes="Hello t")
    step.has_succeeded()


def test__http_request_expects_body_failure(httpserver):
    httpserver.expect_request("/").respond_with_data("Hello there", status=200)
    url = httpserver.url_for("/")

    step = check_http_response_step(
        url,
        response_body_includes="Response does not contain this",
        fatal=False
    )
    step.has_failed()


def test__http_request_failure_extra_long_message(httpserver):
    httpserver.expect_request("/").respond_with_data("Hello there", status=200)
    url = httpserver.url_for("/")

    step = check_http_response_step(
        url,
        response_body_includes=100*"Response does not contain this",
        fatal=False
    )
    assert len(step.secondary_messages[0]) < 100
