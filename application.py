# -*- coding: utf-8 -*-
# @Time    : 2017/12/29 10:36
# @Author  : ha1g0
# @Site    : http://whc.dropsec.xyz
# @File    : application.py



import os

from flask import *
import wtforms
from flask_wtf import Form
import  json
import db



def data(db_name,db_set):
    con = db.selectDB(db_name,db_set)
    data = []
    data = con.find()
    return data


# class PostSchoolname(Form):
#     name = wtforms.StringField('输入学校名 如：中原工学院',validators=[wtforms.validators.DataRequired()])


def info(school):
    test1 = db.selectDB('test','test1')
    test2 = db.selectDB('test','test2')
    test3 = db.selectDB('test','test3')

    test1_info = test1.find_one({'school':school})
    test2_info = test2.find_one({'school':school})
    test3_info = test3.find_one({'school':school})
    return test1_info,test2_info,test3_info



app = Flask(__name__)

#修饰器修饰index,返回从数据库中取出的数据

@app.route('/', methods=['GET', 'POST'])
def index():
    test1 = data("test", "test1")
    test2 = data('test','test2')
    test3 = data('test','test3')
    if request.method == 'POST':
        school = request.form.to_dict()
        return redirect(url_for('search',school=school['school'],_external=True))
    html = render_template('index.html', result=json.dumps(test1))
    response = make_response(html)
    return response



@app.route('/search<school>')
def search(school):
    test1 = data("test", "test1")
    test2 = data('test', 'test2')
    test3 = data('test', 'test3')
    test1_info, test2_info, test3_info = info(school)
    html = render_template('search.html',test1_info=test1_info, test2_info=test2_info,
                                  test3_info=test3_info)
    if request.method == 'POST':
        school = request.form.to_dict()
        return redirect(url_for('search', school=school['school'], _external=True))
    response = make_response(html)
    return response



@app.route('/test')
def domain():
    test2 = data('test', 'test2')
    test3 = data('test', 'test3')
    text = test2[0]
    html = render_template('test.html', test2=text,test3=json.dumps(test3))
    response = make_response(html)
    return response


@app.route('/tree<school>')
def tree(school):
    # test1 = data('test','test1')
    test1_info, test2_info, test3_info = info(school)
    html = render_template('tree.html',test1_info = test1_info)

    response = make_response(html)
    print (1)








if __name__=='__main__':
    app.run(debug=True)

