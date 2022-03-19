# encoding: utf-8
from project.app import MyMicroservice
from flask import jsonify, current_app, request

def create_app():
    """Initialize the Flask app, register blueprints and intialize all libraries like Swagger, database, the trace system...
    return the app and the database objects.
    :return:
    """
    ms = MyMicroservice(path=__file__)
    return ms.create_app()


app = create_app()
'''
#my added Code

@app.route("/")
def index():
    app.logger.info("There are my headers: \n{}".format(request.headers))
    return jsonify({"main": "hello world {}".format(current_app.config["APP_NAME"])})
'''

if __name__ == '__main__':
    app.run()
