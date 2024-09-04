import datetime as dt

from bs4 import BeautifulSoup


def clock_display() -> str:
    html = """<!DOCTYPE html><html lang="en">
    <head>
      <title>current time</title>
        <link crossorigin="anonymous"
         href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
         integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
         rel="stylesheet"/>
      <script src="https://unpkg.com/htmx.org@1.5.0"></script>
    </head>
    <body style="margin: 1em;">
      <h1 style="margin-bottom: 1em;">Tick, tock.</h1>
      <div style="font-family: monospace;">
        <div hx-get="/transit/clock-value" hx-trigger="every 1s">(clock goes here)</div>
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()


def clock_reading() -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return f"webserver time: {now}"