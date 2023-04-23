from flask import Flask, render_template, request, redirect,url_for
from features.dbhandler import DatabaseHandler
import os 


app = Flask(__name__)

app_version = '1.1.0'
port = 5001
static_folder = 'static'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
app.config['UPLOAD_PATH'] = static_folder
app.config['STATIC'] = static_folder


def filter_db_data(data):
    processed_data=[]
    for item in data:
        data_type=item[1]
        if data_type==0:
            processed_data.append(item[2])
        elif data_type==1:
            processed_data.append(item[3])
        else:
            raise Exception
    return processed_data

def retrieve_data(handler,filtering=True):
    db_data = handler.list_elements()
    db_data.reverse()
    if filtering:
        return filter_db_data(db_data)
    else:
        return db_data


@app.route("/",methods=['GET', 'POST'])
def route_root():
    
    if request.method == 'POST' or request.method == 'GET':
        handler=DatabaseHandler()
        db_data=retrieve_data(handler)
        print(db_data)
    if request.method == 'POST' :
        form_data = request.get_json()
        input_value = form_data['input_field']
        userInput = input_value
        # userInput = request.form['userInput']
        handler.insert_data(textdata=userInput)
        db_data=retrieve_data(handler)
        return render_template('base.html', output=db_data)
    else:
        return render_template('base.html',output=db_data)

@app.route("/delete")
def route_delete():
    # if request.method == 'GET':
        handler=DatabaseHandler()
        db_data=retrieve_data(handler=handler,filtering=False)
        for i in db_data:
            response=handler.delete_item(i[0])
            if response == False:
                print("Error")
        return redirect(url_for('route_root'))
    

@app.route("/simple")
def route_simple():
    return render_template("simpleJS.html", port=str(port), link="result")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True)