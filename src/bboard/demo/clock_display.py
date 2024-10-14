import datetime as dt

import pytz
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
    zone = pytz.timezone("America/Los_Angeles")
    now = dt.datetime.now(zone).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return f"webserver time: {now}"


def stop_watch() -> str:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>stop watch</title>
      <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #282c34;
            font-family: 'Arial', sans-serif;
            color: #61dafb;
        }

        h1 {
            font-size: 5rem;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: color 0.5s;
        }

        h1.finished {
            color: #ff4757;
        }
    </style>
    </head>
    <body>
        <h1 id="timer"></h1>
        <script>
        let seconds = 0;
        let minutes = 0;
        const counter = setInterval(Timer, 1000);

        function Timer(){
            seconds += 1;
            if (seconds === 60) {
                seconds = 0;
                minutes += 1;
            } else if (minutes === 1 && seconds === 30) {
                clearInterval(counter);
                return document.querySelector("h1").textContent = "FINISH";
            }
            document.querySelector("h1").textContent =
              `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        </script>
    </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()
