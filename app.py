from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

site = Flask(__name__)

site.config["SECRET_KEY"] = "secretkey1235ffgs"

examples = [{"name":"Main", "url":"main_page"},
            {"name":"About", "url":"about_page"},
            {"name":"Contacts", "url":"contact"}]

@site.route('/')
def main():
    print(url_for('main'))
    return render_template('index.html',  title="Hello Flask", examples=examples)

@site.route('/about/<values>')
def about(values):
    print(url_for('about', values=1234))
    return "Hello"
@site.route("/main_page")
def page1():
    return "Main"

@site.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        if len(request.form["username"]) > 2:
            flash("Send success", category='success')
        else:
            flash("Send ERROR", category='error')
        print(request.form)
    return render_template('contacts.html', title="Обратная связь", examples=examples)

@site.errorhandler(404)
def error_pages(error):
    return render_template('page404.html', title='ERROR', examples=examples)

@site.route("/profile/<username>")
def profile(username):
    if "userLogged" not in session or session['userLogged'] != username:
        about(403)
    else:
        return f"Profile username: {username}"

@site.route("/login", methods=['POST', 'GET'])
def login():
    if "userLogged" in session:
        return redirect(url_for('profile', username=session["userLogged"]))
    elif request.method == 'POST' and request.form['username'] == 'Dima' and request.form["psw"] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title="Авторизация", examples=examples)


if __name__ == "__main__":
    site.run(debug=True)
