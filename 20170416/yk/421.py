from flask import Flask
from flask import request
import pymysql

app = Flask(__name__)


@app.route('/', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><code>用户名</code><input name="username"></p>
              <p><code>密  码</code><input name="password" type="password"></p>
              <button type="submit">登录</button>
              </form>
              <form action="/logon" method="get">
              <button type="submit">注册</button>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    try:
        tname = request.form['username']
        tpassword = request.form['password']
        results = select(tname)
        if results:
            for row in results:
                upassword = row[1]
                nickname = row[2]
                id = row[3]
                if tpassword == upassword:
                    return '''<h3>Hello, %s!你的用户id为%d</h3>
                            <form action="/mima" method="get">
                            <p><button type="submit">修改密码</button></p>
                            </form>''' % (nickname, id)

            return '<h3>用户名或密码错误</h3>'
    except:
        return '<h3>发生了意外错误</h3>'


@app.route('/logon', methods=['GET'])
def logon_1():
    return '''<form action="/logon" method="post">
              <p><code>用户名</code><input name="zusername"></p>
              <p><code>昵  称</code><input name="znickname"></p>
              <p><code>密  码</code><input name="zpassword" type="password"></p>
              <p><button type="submit">注册</button></p>
              </form>'''


@app.route('/logon', methods=['post'])
def logon_2():

    username = request.form['zusername']
    nickname = request.form['znickname']
    password = request.form['zpassword']
    flag = insert(username,nickname,password)
    if flag:
        return '''<form action="/" method="get">
                     <h3>用户注册成功</h3>
                     <p><button type="submit">跳转至登录界面</button></p>
                     </form>'''
    else:
        return '''<form action="/" method="get">
                        <h3>注册失败</h3>
                        <p><button type="submit">跳转至登录界面</button></p>
                        </form>
                        </form>
                        <form action="/logon" method="get">
                        <button type="submit">重新注册</button>
                        </form>'''


@app.route('/mima', methods=['GET'])
def xiugaimima():

    return '''
              <form action="/mima" method="post">
              <p><code>用户id</code><input name="id" </p>
              <p><code>新密码</code><input name="newpassword" </p>
              <p><button type="submit">修改密码</button></p>
              </form>'''


@app.route('/mima', methods=['post'])
def mima():
    id = request.form['id']
    password = request.form['newpassword']
    flag = updata(id, password)
    if flag:
        return '''
                  <form action="/" method="get">
                  <h3>密码修改成功</h3>
                  <p><button type="submit">回到登录界面</button></p>
                  </form>'''
    else:
        return '''
                          <form action="/" method="get">
                          <h3>密码修改失败</h3>
                          <p><button type="submit">回到登录界面</button></p>
                          </form>'''


def select(username):
    with open('sql.txt', 'r') as f:
        us = f.read()
    s = us.split()
    un = s[0]
    pw = s[1]
    try:
        db = pymysql.connect("112.74.215.22", un, pw, "yk")
        cursor = db.cursor()
        sql = "select * from user where username = '%s'" % username
        cursor.execute(sql)
        results = cursor.fetchall()
    finally:
        db.close()
    return results


def insert(username, nickname, password):
    with open('sql.txt', 'r') as f:
        us = f.read()
    s = us.split()
    un = s[0]
    pw = s[1]
    try:
        db = pymysql.connect("112.74.215.22", un, pw, "yk")
        cursor = db.cursor()
        sql = "insert into user (username, password, nickname)values('"+username+"','" + password + "','"+nickname+"')"
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()


def updata(id, newpassword):
    with open('sql.txt', 'r') as f:
        us = f.read()
    s = us.split()
    un = s[0]
    pw = s[1]
    try:
        db = pymysql.connect("112.74.215.22", un, pw, "yk")
        cursor = db.cursor()
        sql = "Update user set password = '"+newpassword+"'where id = '"+id+"'"
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()


if __name__ == '__main__':
    app.run()