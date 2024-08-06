python3 netcat.py --help
usage: netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

Net Tool

options:
  -h, --help            show this help message and exit
  -c, --command         Shell de comando
  -e EXECUTE, --execute EXECUTE
                        Executar comando especificado
  -l, --listen          Ouvir
  -p PORT, --port PORT  Porta especificada
  -t TARGET, --target TARGET
                        IP especificado
  -u UPLOAD, --upload UPLOAD
                        Fazer upload de arquivo

Exemplo:
        netcat.py -t 192.168.1.108 -p 5555 -l -c
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt
        netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" 
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135

        netcat.py -t 192.168.1.108 -p 5555
