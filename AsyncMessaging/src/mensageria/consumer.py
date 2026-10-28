import pika 

conexao = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
canal = conexao.channel()

canal.queue_declare(queue='tarefa', durable=True)

def processar_mensagem(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

canal.basic_consume(queue='tarefa', on_message_callback=processar_mensagem)
print("Aguardando mensagens. Para sair pressione CTRL+C")
canal.start_consuming()