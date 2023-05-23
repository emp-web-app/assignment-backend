########################################################
#             BACKEND ASSIGNMENT STARTS HERE
#
# All your assignment code instances must be removed from
# the internet after your next interview, do not share
# them with anyone.
#
########################################################

import time
from typing import Dict, List, Tuple
from flask import Flask, request, render_template, Response

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from geojson import LineString, Feature, FeatureCollection, GeoJSON
from models import Line, Category

app = Flask(__name__)


# TODO: familiarize youself with the GeoJSON format: https://geojson.org/

# TODO: Setup a valid origin URL for recognizing your Codesandbox frontend.
# Hint: Access /origin from your frontend and see the resulting Flask console output.

origin = "https://<your-frontend-ID>.csb.app"


@app.after_request
def set_cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = origin
    return response


@app.route("/origin")
def show_origin():
    origin = request.headers.get("Origin")
    print("origin:", origin)
    return f"Access-Control-Allow-Origin: {origin}"


@app.route("/")
def index():
    return render_template("base.html")


# TODO: Implement an API endpoint that returns a GeoJSON `FeatureCollection`.
# Hint: You need to retrieve data from the database and convert it to GeoJSON format. We recommend using SQLAlchemy.
# Hint: If you are not familiar with SQLAlchemy's ORM or ORMs in general, you may write SQL statements directly.

# Hint: You can find models for SQLAlchemy in models.py.
# Hint: The `Features` need to have a type of `LineString`.
# Hint: For your reference, the converted GeoJSON should be look like the `geo_data` dictionary in geodata.py.
# Hint: Backend URL should be like: https://instance-name.username.repl.co/geo

engine = create_engine(
    "sqlite:///my_database", connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine)
session = Session()


def read() -> Dict:
    result = (
        session.query(
            Category.cat,
            Line.project_id,
            Line.longitude,
            Line.latitude,
        )
        .join(Category, Line.id == Category.line_id)
        .all()
    )

    cat_proj_map: Dict[Tuple[int, int], List[Tuple[float, float]]] = {}

    for row in result:
        if (row.cat, row.project_id) not in cat_proj_map:
            cat_proj_map[(row.cat, row.project_id)] = []

        cat_proj_map[row.cat, row.project_id].append([row.longitude, row.latitude])

    return FeatureCollection(
        [
            Feature(
                properties={"cat": cat, "project_id": project_id},
                geometry=LineString(coordinates=cat_proj_map[cat, project_id]),
            )
            for cat, project_id in cat_proj_map
        ]
    )


@app.route("/geo", methods=["GET"])
def geo() -> GeoJSON:

    return GeoJSON(read())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
