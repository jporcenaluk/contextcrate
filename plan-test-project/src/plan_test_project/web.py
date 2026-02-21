"""Simple Flask UI for smoke and browser tests."""

from flask import Flask, render_template_string

app = Flask(__name__)

_TEMPLATE = """
<!doctype html>
<html lang=\"en\">
  <head><meta charset=\"utf-8\"><title>Toggle</title></head>
  <body>
    <button id=\"toggle-text\" type=\"button\" onclick=\"toggleText()\">hey</button>
    <script>
      function toggleText() {
        const button = document.getElementById('toggle-text');
        button.textContent = button.textContent === 'hey' ? 'what' : 'hey';
      }
    </script>
  </body>
</html>
"""


@app.get("/")
def home() -> str:
    """Render a tiny interactive page for UI automation checks."""
    return render_template_string(_TEMPLATE)
