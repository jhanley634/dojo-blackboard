from bs4 import BeautifulSoup


def clock_display() -> str:
    html = """<!DOCTYPE html><html lang="en">
    <head>
      <title>Dojo Blackboard</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
      <script src="https://unpkg.com/htmx.org@1.5.0"></script>
    </head>
    <body style="margin: 1em;">
      <h1>Tick, tock.</h1>
      <p hx-target="#clock" hx-swap="beforeend" class="mb-3">(clock goes here)
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()
