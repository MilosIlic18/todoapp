from flask import Flask,render_template,request,redirect
import pymongo
from bson import ObjectId
from pymongo import MongoClient
cluster = MongoClient("") #Connect to mongoDB. EXAMPLE mongodb://localhost:78659/
db = cluster['test']
app =Flask(__name__,template_folder="template")

@app.route("/")
def index():
    return render_template("index.html",todolist=[i for i in db['todoApp'].find()])

@app.route("/create",methods=["POST"])
def create():
    if request.method=="POST":
        db['todoApp'].insert_one({"text":request.form.get("txt")})
        return redirect("/")

@app.route("/delete")
def delete():
        db["todoApp"].drop()
        return redirect("/")

@app.route("/update/<string:id>",methods=["GET"])
def update(id):
    return render_template("update.html",c=db["todoApp"].find_one({"_id": ObjectId(id)}))

@app.route("/update",methods=["POST"])
def updateP():
    if request.method=="POST":
        db['todoApp'].update_one({"_id":ObjectId(request.form.get("id"))}, {"$set":{"text": request.form.get("txt")}})
        return redirect("/")
        
@app.route("/delete/<string:id>",methods=["GET"])
def deleteP(id):
    db["todoApp"].delete_one({"_id": ObjectId(id)})
    return redirect("/")
    
if __name__ == "__main__":
    app.run()