from flask import Flask, jsonify, request, abort
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

clients = []
next_id = 1

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """
    Получить список всех клиентов
    ---
    responses:
      200:
        description: Список всех клиентов
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Иван Иванов"
              phone_number:
                type: string
                example: "+7 123 456 78 90"
              expenses:
                type: number
                example: 1500.50
    """
    return jsonify(clients)

@app.route('/api/clients', methods=['POST'])
def create_client():
    """
    Добавить нового клиента
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Иван Иванов"
            phone_number:
              type: string
              example: "+7 123 456 78 90"
    responses:
      201:
        description: Новый клиент добавлен
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            phone_number:
              type: string
            expenses:
              type: number
    """
    global next_id
    if not request.json or 'name' not in request.json or 'phone_number' not in request.json:
        abort(400)
    client = {
        'id': next_id,
        'name': request.json['name'],
        'phone_number': request.json['phone_number'],
        'expenses': 0.0  # Новые клиенты начинают с 0 расходов
    }
    next_id += 1
    clients.append(client)
    return jsonify(client), 201

@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """
    Обновить данные клиента
    ---
    parameters:
      - name: client_id
        in: path
        required: true
        type: integer
        description: ID клиента для обновления
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Иван Иванов"
            phone_number:
              type: string
              example: "+7 123 456 78 90"
    responses:
      200:
        description: Данные клиента обновлены
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            phone_number:
              type: string
            expenses:
              type: number
      400:
        description: Некорректный ввод
      404:
        description: Клиент не найден
    """
    client = next((c for c in clients if c['id'] == client_id), None)
    if client is None:
        abort(404, description="Client not found")
    if not request.json:
        abort(400, description="Invalid input")
    client['name'] = request.json.get('name', client['name'])
    client['phone_number'] = request.json.get('phone_number', client['phone_number'])
    return jsonify(client)



@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """
    Удалить клиента по ID
    ---
    parameters:
      - name: client_id
        in: path
        required: true
        type: integer
        description: ID клиента для удаления
    responses:
      200:
        description: Клиент удален
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
      404:
        description: Клиент не найден
    """
    global clients
    client = next((c for c in clients if c['id'] == client_id), None)
    if client is None:
        abort(404)
    clients = [c for c in clients if c['id'] != client_id]
    return jsonify({'result': True})


@app.route('/api/clients/<int:client_id>/expenses', methods=['GET'])
def get_client_expenses(client_id):
    """
    Получить расходы клиента по ID
    ---
    parameters:
      - name: client_id
        in: path
        required: true
        type: integer
        description: ID клиента
    responses:
      200:
        description: Расходы клиента
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            phone_number:
              type: string
            expenses:
              type: number
    """
    client = next((c for c in clients if c['id'] == client_id), None)
    if client is None:
        abort(404)
    return jsonify(client)

@app.route('/api/clients/reset', methods=['DELETE'])
def reset_clients():
    """
    Сбросить информацию о клиентах и расходах
    ---
    responses:
      200:
        description: Все данные клиентов сброшены
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
    """
    global clients, next_id
    clients = []
    next_id = 1
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
