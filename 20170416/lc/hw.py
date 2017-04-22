from flask import Flask
from flask import request
import pymysql


def getSqlPassword():
    f = open("sql.txt", "r")
    content = f.readline()
    return content


def getUser(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        sno = row[0]
    return sno


def doSql(sql):
    cursor.execute(sql)
    db.commit()


db = pymysql.connect("112.74.215.22", "lc", getSqlPassword(), "lc")
cursor = db.cursor()

app = Flask(__name__)

username = ''
password = ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    return '''<p>用户名：<input name="username"></p>
              <p>密码：<input name="password" type="password"></p>
              <p>昵称：<input name="nickname"></p>
              <p>id：<input name="id"></p>
              <p><button onclick="register()">注册</button></p>'''


@app.route('/', methods=['GET'])
def home_form():
    return '''<form action="/home" method="post">
              <p>用户名：<input name="username"></p>
              <p>密码：<input name="password" type="password"></p>
              <p><button type="submit">登陆</button></p>
              </form>
              <p><button onclick="{location.href='/login'}">注册</button></p>'''


@app.route('/home', methods=['GET', 'POST'])
def home():
    global username, password
    sqlU = 'select username from user where username = \'%s\'' % request.form['username']
    sqlP = 'select password from user where username = \'%s\'' % request.form['username']
    username = getUser(sqlU)
    password = getUser(sqlP)
    if request.form['username'] == username and request.form['password'] == password:
        sql3 = 'select nickname from user where username = \'%s\'' % request.form['username']
        nickname = getUser(sql3)
        return '''<h3>Hello,%s!</h3>
                  <p><button onclick="{location.href='/revise'}">修改密码</button></p>''' % nickname
    return '<h3>Bad username or password!</h3>'


@app.route('/revise', methods=['GET', 'POST'])
def revise():
    global username, password
    return '''<form action="/home" method="post" id="form1">
              <p>用户名：<input name="username" value="%s"></p>
              <p>密码：<input name="password" type="password" value="%s"></p>
              <p>新密码：<input name="newpassword" type="password"></p>
              <input type="submit" value="修改密码" formaction="/ok">
              <input type="submit" value="返回主界面">''' % (username, password)


@app.route('/ok', methods=['POST'])
def OK():
    tempUsername = request.form['username']
    newPassword = request.form['newpassword']
    sqlUpdate = 'update user set password = \'%s\' where username = \'%s\'' % (newPassword, tempUsername)
    doSql(sqlUpdate)
    return '''<html>
              <head>
              <script language="javascript">
              alert("修改成功")
              </script>
              </head>
              </html>'''


if __name__ == '__main__':
    app.run()
