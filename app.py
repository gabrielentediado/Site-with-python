from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    matricula = db.Column(db.Integer)

    def __init__(self, nome, idade, matricula):
        self.nome = nome
        self.idade = idade
        self.matricula = matricula


@app.route('/cria_alunos', methods=["GET", "POST"])
def cria_alunos():
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    matricula = request.form.get('matricula')

    if request.method == 'POST':
        aluno = Aluno(nome, idade, matricula)
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('lista_alunos'))
    return render_template("novo_aluno.html")


@app.route('/')
def lista_alunos():
    return render_template('alunos.html', alunos=Aluno.query.all())


@app.route('/<int:id>/atualiza_aluno', methods=["GET", "POST"])
def atualiza_aluno(id):
    aluno = Aluno.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form["nome"]
        idade = request.form["idade"]
        matricula = request.form["matricula"]

        aluno.query.filter_by(id=id).update({"nome": nome, "idade": idade, "matricula": matricula})
        db.session.commit()
        return redirect(url_for('lista_alunos'))
    return render_template("atualiza_aluno.html", aluno=aluno)


@app.route('/<int:id>/remove_aluno')
def remove_aluno(id):
    aluno = Aluno.query.filter_by(id=id).first()
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('lista_alunos'))


if __name__ == "__main__":
    app.run(debug=True)
