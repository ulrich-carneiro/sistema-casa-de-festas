from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta_projeto'

def iniciar_banco():
    conn = sqlite3.connect('festas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            tipo_festa TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

iniciar_banco()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        tipo_festa = request.form['tipo_festa']

        conn = sqlite3.connect('festas.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM agendamentos WHERE data = ?', (data,))
        festa_existente = cursor.fetchone()
        
        if festa_existente:
            flash('Erro: Já existe um evento marcado para esta data!', 'erro')
        else:
            cursor.execute('INSERT INTO agendamentos (nome, data, tipo_festa) VALUES (?, ?, ?)', (nome, data, tipo_festa))
            conn.commit()
            flash('Agendamento realizado com sucesso!', 'sucesso')
        
        conn.close()
        return redirect(url_for('home'))

    # Puxa os agendamentos para a tabela
    conn = sqlite3.connect('festas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agendamentos ORDER BY data')
    lista_agendamentos = cursor.fetchall()
    conn.close()

    # Cria uma lista apenas com as datas ocupadas para enviar ao calendário
    datas_ocupadas = [festa[2] for festa in lista_agendamentos]

    # Envia os dados para o HTML (agendamentos para a tabela, datas_ocupadas para o calendário)
    return render_template('index.html', agendamentos=lista_agendamentos, datas_ocupadas=datas_ocupadas)

# Nova Rota para excluir a festa
@app.route('/excluir/<int:id_festa>')
def excluir(id_festa):
    conn = sqlite3.connect('festas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM agendamentos WHERE id = ?', (id_festa,))
    conn.commit()
    conn.close()
    
    flash('Agendamento excluído com sucesso!', 'sucesso')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)