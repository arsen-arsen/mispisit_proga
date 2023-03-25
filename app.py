from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/mispisit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mispisit(db.Model):
    __tablename__ = 'mispisit'
    user_id = db.Column(db.Integer, primary_key=True)
    req_data = db.Column(db.String(255))
    report_info = db.Column(db.String(255))
    other_info = db.Column(db.String(255))

    def __init__(self, req_data, report_info, other_info):
        self.req_data = req_data
        self.report_info = report_info
        self.other_info = other_info


@app.route("/")
def homepage():
    data = Mispisit.query.all()
    if data is None:
        data = []
    return render_template("index.html", data=data)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    mispisit = None

    if request.method == 'POST':
        req_data = request.form['req_data']
        report_info = request.form['report_info']
        other_info = request.form['other_info']
        new_entry = Mispisit(req_data=req_data, report_info=report_info, other_info=other_info)
        db.session.add(new_entry)
        db.session.commit()
        data = Mispisit.query.all()
        if data is None:
            data = []
        return render_template('index.html', data=data)

    if request.method == 'GET':
        search_query = request.args.get('search_query')
        if search_query is not None:
            data = Mispisit.query.filter(Mispisit.req_data.contains(search_query) | Mispisit.report_info.contains(search_query) | Mispisit.other_info.contains(search_query)).all()
        else:
            data = []

    return render_template("index.html", data=data)

@app.route('/delete/<int:user_id>', methods=['GET'])
def delete(user_id):
    entry = Mispisit.query.get(user_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    entry = Mispisit.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        req_data = request.form['req_data']
        report_info = request.form['report_info']
        other_info = request.form['other_info']

        entry.req_data = req_data
        entry.report_info = report_info
        entry.other_info = other_info

        db.session.merge(entry)
        db.session.commit()

        return redirect(url_for('homepage'))

    return render_template('edit.html', entry=entry)

if __name__ == '__main__':
    app.run(debug=True)
