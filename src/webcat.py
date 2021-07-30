#!/usr/bin/env python3
# webcat.py
# K0RNH0LI0 2021
#
# Web interface for printing to BlueTooth thermal cat printers.

import os
import asyncio
from flask import Flask, request, render_template, flash, redirect
from subprocess import Popen, PIPE, STDOUT

import config
import driver

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/print", methods=["GET", "POST"])
def catprint():
    if request.method == "POST":
        if os.path.exists("image.pbm"):
            flash("Printer is busy 3:")
            return redirect("/")

        if not "file" in request.files:
            flash("Please upload a file 3:")
            return redirect("/")

        # convert file to P4 PBM image
        file = request.files["file"].read()
        p = Popen(["convert", "-", "-resize", "384x", "-monochrome", "pbm:-"],
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE)
        convert = p.communicate(input=file)
        if convert[1] != b'':
            # error converting file
            flash("Please upload a valid image 3:")
            return redirect("/")

        with open("image.pbm", "wb") as f:
            f.write(convert[0])
        flash("Image sent to printer :3")
        return redirect("/")

if __name__ == "__main__":
    app.secret_key = config.SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = config.SIZE_LIMIT
    app.run("0.0.0.0", config.HTTP_PORT)
