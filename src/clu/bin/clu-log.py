#!/usr/bin/env python
import pika
import sys


def main(argv):
  severities = argv[1:]
  if not severities:
      print >> sys.stderr, "Usage: %s [info] [warning] [error]" %(argv[0],)
      sys.exit(1)
  
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='harry.lan'))
  channel = connection.channel()

  channel.exchange_declare(exchange='home.events',type='topic')

  #result = channel.queue_declare()
  result = channel.queue_declare(exclusive=True)
  queue_name = result.method.queue


  for severity in severities:
      print severity
      channel.queue_bind(exchange='home.events',queue=queue_name,routing_key=severity)

  print ' [*] Waiting for logs. To exit press CTRL+C'

  def callback(ch, method, properties, body):
      print " [x] %r:%r" % (method.routing_key, body,)

  channel.basic_consume(callback,queue=queue_name,no_ack=True)

  channel.start_consuming()

if __name__=="__main__":
  main(sys.argv)
