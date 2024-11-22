from flask import Flask, render_template,request,redirect,jsonify,abort
from essentials import apis,syntax
from essentials import xero
import random

app = Flask(__name__)

apikey=None
api=None
selected_api=None
is_first_prompt = False

back_images = ["cool.jpg","cool2.jpg","cool3.jpg","cool4.jpg"]
select_background = xero.ReplaceRandom(back_images)

def list_to_dict(ls):
    d={}
    for i in range(len(ls)):
        d[str(i)] = ls[i]
    return d

@app.route("/req",methods=['POST'])
def req():#
    if "request_messages" in list(request.form.keys()) and api!=None:
        return jsonify(list_to_dict(api.get_formatted_messages()))
    else: 
        abort(404,description="API is not set.")

@app.route("/ajax",methods=["POST","GET"])
def ajax():
    global apikey,api,is_first_prompt,selected_api
    if request.method=="POST" or "newMessage" in list(request.form.keys()):
        print("In")
        newMessage = request.form['newMessage']
        print(newMessage)
        if newMessage == 'breakpoint':
            breakpoint()
        if newMessage == "RESET_CHAT":
            if apikey and api and selected_api:
                api = apis.select_api[selected_api](apikey)
                api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
                is_first_prompt=True
                return jsonify({"REFRESH":"TRUE"})
        if newMessage == "RESET_API":
            apikey = None
            api=None
            selected_api=None
            is_first_prompt = False
            return redirect("/login")
        if apikey != None:
            if selected_api == None:
                return redirect("/login")
            if api == None:
                api=apis.select_api[selected_api](apikey=apikey)
                if is_first_prompt == False:
                    api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
                    is_first_prompt=True
                api.user_message(newMessage)
            else:
                if is_first_prompt == False:
                    api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
                    is_first_prompt=True
                api.user_message(newMessage)
        else:
            return redirect("/login")
        return jsonify({"successful":"true"})
    else:
        if apikey == None:
            return redirect("/login")
        else:
            if api == None:
                return render_template("ajax.html")
            else:
                return render_template("ajax.html",messages=api.get_formatted_messages())

@app.route("/",methods=["POST","GET"])
def index():
    global apikey,api,is_first_prompt,selected_api
    if request.method=="POST":
        newMessage = request.form['newMessage']
        if newMessage == 'breakpoint':
            breakpoint()
        if newMessage == "RESET_CHAT":
            if apikey and api and selected_api:
                api = apis.select_api[selected_api](apikey)
                api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
                is_first_prompt=True
                return redirect("/")
        if newMessage == "RESET_API":
            apikey = None
            api=None
            selected_api=None
            is_first_prompt = False
            return redirect("/login")
        if apikey != None:
            if selected_api == None:
                return redirect("/login")
            if api == None:
                api=apis.select_api[selected_api](apikey=apikey)
                if is_first_prompt == False:
                    api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
                    is_first_prompt=True
                api.user_message(newMessage)
            else:
                if is_first_prompt == False:
                    api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
                    is_first_prompt=True
                api.user_message(newMessage)
        else:
            return redirect("/login")
        return redirect("/")
    else:
        if apikey == None:
            return redirect("/login")
        else:
            if api == None:
                return render_template("index.html",random_back=select_background.Next())
            else:
                return render_template("index.html",messages=api.get_formatted_messages(),random_back=select_background.Next())

@app.route("/login",methods=['POST',"GET"])
def login():
    global apikey,api,is_first_prompt,selected_api
    if request.method == "POST":
        apikey = request.form['apikey']
        selected_api=request.form['apiplatform']
        api=apis.select_api[selected_api](apikey=apikey)
        if is_first_prompt == False:
            api.system_message(syntax.official_assistant_formatting_v1.FORMAT,False)
            is_first_prompt=True

        return redirect('/')
    else:
        return render_template("login.html")
@app.route("/test")
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)