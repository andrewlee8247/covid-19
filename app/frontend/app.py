from flask import Flask, request, render_template, make_response, after_this_request, redirect
import secrets
import logging

app = Flask(__name__)
token = secrets.access_token()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        request.form.get('first_name')
        request.files.get('payload')
        request.headers.get('Content-Type: multipart/form-data')
        request.headers.get('x-access-token: {}'.format(token))
        #request.post("https://covid-api-3ghvym5f7q-uc.a.run.app/api/prediction")
        return redirect("https://covid-api-3ghvym5f7q-uc.a.run.app/api/prediction", code=307)
    return render_template("index.html")

@app.route("/test")
def home():
    return render_template("app_front.html")


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port="8080")
