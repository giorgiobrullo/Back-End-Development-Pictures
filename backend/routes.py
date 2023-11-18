from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    pic = next((item for item in data if item['id'] == id), None)
    return (jsonify(None), 404) if pic is None else (jsonify(pic), 200)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    newpic = request.get_json()
    if next((item for item in data if item['id'] == newpic['id']), None) is not None:
        return {"Message": f"picture with id {newpic['id']} already present"}, 302
    else:
        data.append(newpic)
        
    return jsonify(newpic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    uppic = request.get_json()
    if next((item for item in data if item['id'] == uppic['id']), None) is not None:
        for item in data:
            if item['id'] == uppic['id']:
                item.update(uppic)
                return {"Message": "updated"}, 200
    else:
        return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    index = next((i for i, item in enumerate(data) if item['id'] == id), None)

    if index is None:
        return {"message": "picture not found"}, 404
    else:
        data.pop(next((i for i, item in enumerate(data) if item['id'] == id), None))
        return {} 204

