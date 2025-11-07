import socket
import threading
import time

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 5050))

apelido_global = None
instrucoes_mostradas = False

#Cleinte apelido
def receber():
    global apelido_global
    global instrucoes_mostradas
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            
            # Servidor pedindo apelido
            if mensagem == 'NICK':
                if apelido_global is None:
        
                    novo_apelido = input("\n[SISTEMA] Escolha seu apelido: ")
                    cliente.send(novo_apelido.encode())
                    apelido_global = novo_apelido 
                else:
           
                    novo_apelido = input("\n[SISTEMA] Apelido em uso. Tente outro: ")
                    cliente.send(novo_apelido.encode())
                    apelido_global = novo_apelido 
                
       
            elif mensagem == 'ERR apelido_em_uso':
                print("[ERRO] Este apelido já está em uso. Tente novamente.")
                apelido_global = None
                
          
            elif mensagem:
            
                print(mensagem) 
            else:
                break
        except:
            print("Conexão encerrada pelo servidor.")
            cliente.close()
            break
# ----------------------------------------------------------------------


thread_receber = threading.Thread(target=receber)
thread_receber.daemon = True
thread_receber.start()

# LOOP Comandos e Mensagens
while True:
    if apelido_global: 
        try:
            if not instrucoes_mostradas:
                 print("\n[SISTEMA] Conectado! Use: @apelido (DM), WHO (listar) ou QUIT/SAIR (sair).")
                 instrucoes_mostradas = True

            mensagem = input("Você: ") 
            
            # 1. Checa (QUIT)
            if mensagem.upper() == 'QUIT' or mensagem.lower() == 'sair':
                cliente.sendall('QUIT'.encode())
                print("Desconectando...")
                break
            
            # 2. Checa (WHO)
            elif mensagem.upper() == 'WHO':
                cliente.sendall("MSG WHO".encode())
            
            # 3. Checa (DM) 
            elif mensagem.startswith('@'):
                
                 cliente.sendall(f"MSG {mensagem}".encode()) 
            
            # 4. Mensagem (Broadcast)
            else:
      
                cliente.sendall(f"MSG {mensagem}".encode()) 
            
        except:
            break
    else:
    
        time.sleep(0.1) 
        
cliente.close()