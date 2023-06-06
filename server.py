# server.py
import socket
import json
import threading


def processingDataClient(received):
    '''Process received client data.

    Args:
        received (dict): Dictionary containing client data.

    Returns:
        dict: Dictionary with processed client data.
    '''
    def generateImc(dict):
        '''Generate IMC using height and weight.

        Args:
            h (dict): Client height.
            p (dict): Client weight.

        Returns:
            float: IMC value.
        '''
        h = dict['altura']
        p = dict['peso']
        return round(float(p / (h * h)), 2)

    # Adding the imc to data sent by the user.
    received['imc'] = generateImc(received)

    # Status IMC.
    def analyseImc(imc):
        '''Analyze IMC and determine status.

        Args:
            imc (float): IMC value.

        Returns:
            str: Status message.

        '''
        if imc > 0 and imc < 18.5:
            status = "Abaixo do Peso!"
        elif imc <= 24.9:
            status = "Peso normal!"
        elif imc <= 29.9:
            status = "Sobrepeso!"
        elif imc <= 34.9:
            status = "Obesidade Grau 1!"
        elif imc <= 39.9:
            status = "Obesidade Grau 2!"
        elif imc <= 40.0:
            status = "Obesidade Grau 1!"
        else:
            status = "Valores inválidos"
        return status

    # Adding the status of the imc to data sent by the user.
    received['statusImc'] = analyseImc(received['imc'])

    # TMB (Bala Metabolic Rate).
    def generateTMB(dict):
        '''Generate TBM based on user data.

        Args: 
            dict (dict): User data.

        Returns:
            float: TBM value.
        '''
        sex = dict['sexo']

        if sex in 'Mm':
            tmb = 5 + (10 * dict['peso']) + (6.25 *
                                             (dict['altura'] * 100)) - (5 * dict['idade'])

        else:
            tmb = (10 * dict['peso']) + (6.25 *
                                         (dict['altura'] * 100)) - (5 * dict['idade']) - 5

        return tmb

    # Adding the tmb to data sent by the user.
    received['tmb'] = generateTMB(received)

    def generateCal(dict):
        '''Generate cal based on user data.

        Args:
        dict (dict): 
            - nvlAtiv (int): Level of physical activity.
            - tmb (float): Bala Metabolic Rate.

        Returns:
            float: Cal value.
        '''
        if dict['nvlAtiv'] == 1:
            fatorAtiv = 1.2

        elif dict['nvlAtiv'] == 2:
            fatorAtiv = 1.375

        elif dict['nvlAtiv'] == 3:
            fatorAtiv = 1.725

        else:
            fatorAtiv = 1.9

        return round((dict['tmb'] * fatorAtiv), 2)

    # adding the cal to data sent by the user
    received['cal'] = generateCal(received)

    def generateNutrients(dict):
        """Generate Nutrients from cal value.

        Args: 
            dict (dict): Dict containing cal value.

        Returns:
            dict: Dict containing nutrients values.
                - 'carboidratos' (str): Value of carbohydrates.
                - 'proteinas' (str): Value of proteins.
                - 'gorduras' (str): Value of fats.
        """
        carb = str(round((dict['cal'] * 0.45), 2))
        prot = str(round((dict['cal'] * 0.3), 2))
        fat = str(round((dict['cal'] * 0.25), 2))

        return {"carboidratos": carb, "proteinas": prot, "gorduras": fat}

    # adding the nutrients to data sent by the user
    received["nutrientes"] = generateNutrients(received)
    return received


def handleClient(clientSocket, addr):
    '''Makes connection with the client and receives their data.

    Args: 
        clientSocket (socket): The socket object of the connection to the client.
        addr (tuple): The tuple containing the IP address and port of the client.


    Returns:
        str: Sends to the client the result of processing the received data in JSON format.
    '''
    print('Conectado a {}'.format(str(addr)))

    # Recive client data.
    received = clientSocket.recv(1024).decode()
    print('Os dados recebidos do cliente são: {}'.format(received))

    # Server processing.
    received = json.loads(received)
    data = processingDataClient(received)
    print('O resultado do processamento é {}'.format(data))

    # Serialising.
    result = json.dumps(data)

    # Send a result.
    clientSocket.send(result.encode('ascii'))
    print('Os dados do cliente: {} foram enviados com sucesso!'.format(addr))

    # Finish a connection.
    clientSocket.close()


# Create a socket object.
print('ECHO SERVER para cálculo do IMC')
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get a local machine name.
host = '127.0.0.1'
port = 9999

# Bind to the port.
serverSocket.bind((host, port))

# Start listening requests.
serverSocket.listen()
print('Serviço rodando na porta {}.'.format(port))

while True:
    # Establish a connection.
    clientSocket, addr = serverSocket.accept()
    t = threading.Thread(target=handleClient, args=(clientSocket, addr))
    t.start()
