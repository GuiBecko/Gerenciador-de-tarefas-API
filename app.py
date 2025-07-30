from flask import Flask, jsonify, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__) #inicializa a aplicação

tarefas_salvas = [] 
next_id = 1

#rota homepage
@app.route('/')
def homepage():
    return render_template("homepage.html")


#rota de vizualização das tarefas, retorna um html juntamente com a lista de tarefas salvas
@app.route('/pegartarefas')
def pegartarefas():
    return render_template("pegartarefas.html", tarefas=tarefas_salvas)

#rota de criação de uma nova tarefa, recebe os dados da homepage e cria um objeto tarefa, depois insere-o na lista de tarefas 
@app.route('/criartarefa', methods=['POST'])
def criartarefa():
    global next_id
    dados_recebidos = request.form 

    nova_tarefa = { 
        'id': next_id,
        'titulo': dados_recebidos['titulo'],
        'data': dados_recebidos['data']
    }

    tarefas_salvas.append(nova_tarefa) 
    next_id +=1
    
    return redirect(url_for("homepage"))

#rota para editar tarefas, retorna um html para editar a tarefa e o objeto tarefa a ser editado
@app.route('/editartarefas/<int:id>') 
def pagina_editar_tarefa(id):
    tarefa_para_editar = None
    for tarefa in tarefas_salvas: 
        if tarefa['id'] == id:
            tarefa_para_editar = tarefa
            break
    
    if tarefa_para_editar:
        return render_template('editartarefas.html', tarefa=tarefa_para_editar)
    
    return redirect(url_for('pegartarefas'))


#rota para processar a edição, recebe os dados do form "editartarefas.html" e os altera na lista "tarefas_salvas"
@app.route('/processaredicao', methods=['POST'])
def processaredicao():
    dados_editados = request.form
    task_id = int(dados_editados['id'])

    index_para_substituir = -1
    for i, tarefa in enumerate(tarefas_salvas):
        if tarefa['id'] == task_id:
            index_para_substituir = i
            break

    if index_para_substituir != -1:
        tarefas_salvas[index_para_substituir] = {
            'id': task_id,
            'titulo': dados_editados['titulo-novo'],
            'data': dados_editados['data-nova']
        }
        return redirect(url_for('pegartarefas'))
    

#rota para excluir a tarefa, recebe o id da tarefa a ser excluida da rota "pegartarefas" e a exclui na lista tarefas_salvas, retorna para a pagina "pegartarefas"
@app.route('/excluirtarefa', methods = ['POST'])
def excluirtarefa():
    dados = request.form 
    id_a_excluir = int(dados['tarefa_id']) 
    i=0
    for tarefa in tarefas_salvas:
        if tarefa['id'] == id_a_excluir:
            tarefas_salvas.pop(i)
        i+=1

    
    return redirect(url_for('pegartarefas'))
    
    

if __name__ == "__main__":
    app.run(debug=True)

