import socket
import threading

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 5050))
servidor.listen()

print('aguardando conexão.....')

clientes_apelidos = {} 

def broadcast(mensagem, conexao_remetente):

    for conexao in clientes_apelidos.values():

        if conexao != conexao_remetente:
            try:
                conexao.sendall(mensagem.encode())
            except:

                pass
#apelidos ------------------------------------------------------------------------ 

def alvo(conex, ender):
    print('bem vindo', ender)
    apelido = None 

    #Registro apelido
    conex.send('NICK'.encode())
    while True:
        try:
            apelido_tentativa = conex.recv(1024).decode()
            
            # validação pra usar apelido
            if apelido_tentativa in clientes_apelidos.keys():
                conex.send('ERR apelido_em_uso'.encode()) 
                conex.send('NICK'.encode())
                continue 
            
            apelido = apelido_tentativa
            break
        except:
         
            return
            
    # armazenar e notificar + dicionário
    clientes_apelidos[apelido] = conex 
    
    # notificar
    conex.send(f'[SISTEMA] Bem-vindo(a), {apelido}!'.encode())
    broadcast(f'[SISTEMA] User {apelido} joined', conex) 
    # ----------------------------------------------------------------------------

    # loop 
    while True:
        try:
            mensagem_raw = conex.recv(1024)
            if not mensagem_raw:
                break 

            mensagem_completa = mensagem_raw.decode()
        
            if mensagem_completa.upper() == 'QUIT' or mensagem_completa.upper() == 'MSG QUIT' or mensagem_completa.lower() == 'Sair':
                break
            
            # comando WHO (Listar usuários)
            elif mensagem_completa.upper() == 'MSG WHO':
                lista_usuarios = ", ".join(clientes_apelidos.keys())
                resposta = f'[SISTEMA] Usuários conectados: {lista_usuarios}'
                conex.send(resposta.encode())
                
                # mensagens
            elif mensagem_completa.startswith("MSG @"):
                
                parte_do_comando = mensagem_completa[5:] 
                
                if ' ' in parte_do_comando:
                   
                    apelido_destino, conteudo = parte_do_comando.split(' ', 1)
                    
                    if apelido_destino in clientes_apelidos:
                        conexao_destino = clientes_apelidos[apelido_destino]
                        
                        mensagem_dm = f'FROM {apelido} [dm]: {conteudo}'
                        conexao_destino.send(mensagem_dm.encode())
                        conex.send(f'[DM enviada para {apelido_destino}]'.encode()) 
                        
                    else:
                    
                        conex.send('ERR user_not_found'.encode())
                        
                else:
                    conex.send('[AVISO] Formato DM inválido. Use: @apelido mensagem'.encode())

         
            elif mensagem_completa.startswith("MSG "):
                conteudo = mensagem_completa[4:]
                
                mensagem_broadcast = f'FROM {apelido} [all]: {conteudo}'
                print(f'[{apelido}] Broadcast: {conteudo}')
                
                broadcast(mensagem_broadcast, conex)
        
            else:
                 print(f'Mensagem sem protocolo de {apelido}: {mensagem_completa}')

        except:
            break 
            #-------------------------------------------------------------------------------------------
    # Desconexão
    print(f'{apelido} ({ender}) desconectado.')
    if apelido in clientes_apelidos:
        del clientes_apelidos[apelido]
        broadcast(f'[SISTEMA] {apelido} left the chat.', conex) 
        
    conex.close()

# Loop aceite p/ conexões
while True:
    conex, ender = servidor.accept()
    direc = threading.Thread(target= alvo, args=(conex, ender))
    direc.start()


