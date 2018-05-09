from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/register/")
def register():
    return render_template('register.html')

@app.route("/adduser", methods=['POST', 'GET'])
def adduser():
    user_name = request.form.get('username')
    print(user_name)

    cnx = mysql.connector.connect(user='root', database='bottle')
    cursor = cnx.cursor()

    add_code = "INSERT INTO point (id, name, score) VALUES (NULL, '" + user_name + "', '0')"
    print(add_code)
    cursor.execute(add_code)
    cnx.commit()

    cursor.close()
    cnx.close()

    return render_template('user.html')

@app.route("/addcode", methods=['POST', 'GET'])
def addcode():
    coder = request.args.get('code')
    print(coder)

    cnx = mysql.connector.connect(user='root', database='bottle')
    cursor = cnx.cursor()

    add_code = "INSERT INTO code (id, name, state) VALUES (NULL, '" + coder + "', '0')"

    data_code = (coder)
    print(coder)
    print(add_code)
    cursor.execute(add_code)
    cnx.commit()

    cursor.close()
    cnx.close()

    return coder

@app.route("/addpoint", methods=['POST', 'GET'])
def addpoint():
    user_code = request.form.get('code')
    user_name = request.form.get('username')
    print(user_code)
    print(user_name)

    cnx = mysql.connector.connect(user='root', database='bottle')
    cursor = cnx.cursor()

    check_state = "SELECT state FROM code WHERE name='" + user_code + "'"
    cursor.execute(check_state)
    try:
        state = int(cursor.fetchone()[0])
        print(state)
    except:
        state = ''

    cursor.execute("SELECT name FROM code")
    all_code = [row[0] for row in cursor]
    print(all_code)

    cursor.execute("SELECT name FROM point")
    all_name = [row[0] for row in cursor]
    print(all_name)

    if (user_code in all_code) and (state == 0) and (user_name in all_name):
        get_point = "SELECT score FROM point WHERE name='" + user_name + "'"
        cursor.execute(get_point)
        old_point = int(cursor.fetchone()[0])
        print(old_point)
        new_point = str(old_point + 1)
        print(new_point)

        add_point = "UPDATE point SET score=" + new_point + " WHERE name='" + user_name + "'"
        print(add_point)
        cursor.execute(add_point)
        cnx.commit()

        change_state = "UPDATE code SET state=1 WHERE name='" + user_code + "'"
        cursor.execute(change_state)
        cnx.commit()

        #cursor.execute("SELECT score FROM point WHERE name='ton'")
        #new_point = int(cursor.fetchone()[0])
        print(new_point)

        cursor.close()
        cnx.close()

        return render_template('point.html', new_point = new_point)

    else:
        cursor.close()
        cnx.close()

        return render_template('fail.html', statement = state, wrong_code = not(user_code in all_code), no_name = not(user_name in all_name))

if __name__ == "__main__":
    app.run(host="0.0.0.0")