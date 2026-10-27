import pika 

conexao = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
canal = conexao.channel()

canal.queue_declare(queue='tarefa', durable=True)

canal.basic_publish(
    exchange="",
    routing_key="tarefa",
    body="Minha primeira mensagem!",
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print("Mensagem enviada!")

conexao.close()