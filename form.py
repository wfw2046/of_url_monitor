# -*- coding: utf-8 -*-
from flask import Flask
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxxx'
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)


class UrlForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    passwd = StringField('password', validators=[DataRequired()])
    metricname = StringField('metricname', validators=[DataRequired()])
    address = StringField('URL', validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route('/url', methods=['GET', 'POST'])
def url_add():
    address = None
    name = None
    passwd = None
    metricname = None
    url = UrlForm()

    if url.validate_on_submit():
        address = url.address.data
        name = url.name.data
        passwd = url.passwd.data
        metricname = url.metricname.data
        if name == "admin" and passwd == "adminwfw":

            if os.path.exists("/home/wangfw/project-py/url_monitor/shell/60_" + address + ".sh"):
                print "file exist"
                error_mess = "Url had already exist！！！"
                return render_template('error.html', error_mess=error_mess)
            else:
                os.system(
                    "cp /home/wangfw/project-py/url_monitor/template.sh  /home/wangfw/project-py/url_monitor/shell/60_"
                    + address + ".sh")
                f = open("/home/wangfw/project-py/url_monitor/shell/60_" + address + ".sh", "r")
                flist = f.readlines()
                flist[1] = "metric=\"" + metricname + "\"\n"
                flist[4] = "url=\"" + address + "\"\n"
                f.close()
                f = open("/home/wangfw/project-py/url_monitor/shell/60_" + address + ".sh", "w")
                f.writelines(flist)
                f.close()
                # os.system(
                #     "cd  /home/wangfw/project-py/url_monitor/shell/ && git add 60_" + address +".sh&&git commit -m 'tset' &&git push")
                return render_template('index.html', form=url, address=address, name=name, passwd=passwd,
                                       metricname=metricname)
        else:
            error_mess = "Invalid name or password！！！"
            return render_template('error.html', error_mess=error_mess)
    return render_template('index.html', form=url, address=address, name=name, passwd=passwd, metricname=metricname)


if __name__ == '__main__':
    app.run()
/home/wangfw/Desktop/form
