# NetCat Tool

A ferramenta NetCat é uma implementação básica para estabelecer conexões de rede, enviar e receber dados, e executar comandos. Baseada no conceito do `netcat`, ela suporta várias operações de rede e manipulação de arquivos.

## Uso

Para ver as opções disponíveis, execute:

```bash
python3 netcat.py --help

usage: netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

Net Tool

options:
  -h, --help            Show this help message and exit
  -c, --command         Shell de comando
  -e EXECUTE, --execute EXECUTE
                        Executar comando especificado
  -l, --listen          Ouvir
  -p PORT, --port PORT  Porta especificada
  -t TARGET, --target TARGET
                        IP especificado
  -u UPLOAD, --upload UPLOAD
                        Fazer upload de arquivo

