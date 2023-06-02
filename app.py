from typing import List, Union, Any

# this function serves to reduce unnecessary code prints


def print_message(message: str):
    '''Prints a formatted message.

    Args:
        message (str): The message that will be printed.

    Returns: 
        str: Formatted message.
    '''
    print()
    print(message)
    print()


class App():
    '''Application's main controller class.'''

    def __init__(self):
        '''Initialize the application'''
        App.title("The shape of us!")
        print_message("=> Informe alguns dados para começar:")
        App.generateHeader()

    @classmethod
    def padding(cls):
        '''Prints padding in the application.'''
        print("\n\n")

    @classmethod
    def generateHeader(cls):
        '''Generate the header of the application.'''
        print("OBS: O Nivel de atividade varia de 1 (Sedentário) a 4 (Muito Ativo) !")
        print("Ex: {:^8s} {:^22s} {:^14s} {:^20s} {:^10s} \n".format(
            "1.70", "70.0", "M", "3", "20"))

    @classmethod
    def printRow(cls):
        '''Prints a row in the application.'''
        print('*' * 81)

    @classmethod
    def printRowTable(cls):
        '''Prints a row for the table in the application.'''
        print(f"+{'-' * 25}++{'-' * 25}++{'-' * 25}+")

    @classmethod
    def title(cls, title: str):
        '''Prints a title with a row.

        Args:
            title (str): The title text.
        '''
        App.printRow()
        print('*{:^79s}* \n'.format(title))
        App.printRow()

    @classmethod
    def collectUserData(cls):
        '''Collects user data

        Returns:
            list: A list of user data.
        '''
        print("{:^16s}".format("Altura (m):"), end="")
        print("{:^18s}".format("Peso (Kg):"), end="")
        print("{:^18s}".format("Sexo (M/F):"), end="")
        print("{:^18s}".format("Nvl de Ativ:"), end="")
        print("{:^16s}".format("Idade :"))

        userData = input("")
        userData = userData.split(" ")
        print()
        App.printRow()

        return userData

    @classmethod
    def listUserData(cls, values: List[str]) -> List[Union[str, float]]:
        '''Returns a list of user data

        Args:
            values (List[str]): A list of user data values.

        Returns:
            List[Union[str, float]]: A list of user data values where numeric values are formatted to float.
        '''
        list = []
        for i in values:
            if i != "":
                if (i in "Mm" or i in "Ff"):
                    list.append(i)
                else:
                    list.append(float(i))
        return list

    @classmethod
    def validateData(cls, values: List[str]) -> List[Union[str, float]]:
        '''Validates the user data

            The function catches like IndexError and ValueError 
            that can occur during the user data validation process.

        Args:
            values (List[str]): A list of user data values.

        Returns:
            List[Union[str, float]]: A list of user data values where numeric values are formatted to float.
        '''
        while True:
            try:
                list = App.listUserData(values)
                userData = App.generateDict(list)

            except IndexError:
                print_message(
                    "Preencha todos os dados para prosseguir!".upper())
                App.generateHeader()
                values = App.collectUserData()

            except ValueError:
                print_message('Valor inválido!'.upper())
                App.generateHeader()
                values = App.collectUserData()

            else:
                list = App.listUserData(values)
                break

        return list

    @classmethod
    def generateDict(cls, list: List[Union[str, float]]) -> dict:
        '''Generates a dictionary of user data values

            The function takes in a list of values, where each value in the list corresponds to a 
            specific field of user data, such as height, weight, gender, activity level, and age.

        Args:
            list (List[Union[str, float]]): A list of user data values.

        Returns:
            dict: A dictionary with keys 'altura', 'peso', 'sexo', 'nvlAtiv', and 'idade'.
        '''
        dic = {'altura': None, 'peso': None,
               'sexo': None, 'nvlAtiv': None, 'idade': None}
        cont = 0
        for k, v in dic.items():
            dic[k] = list[cont]
            cont += 1

        return dic

    @classmethod
    def printResult(cls, list: List[List[Any]]):
        '''Prints the result.

        Args:
            list (List[List[Any]]): A nested list containing the result.

        Returns:
            This function returns the display of a row of the 
            table in the console, with the given values in the list list.
        '''
        print()
        App.printRow()
        print('|{:^25s}||{:^25s}||{:^25s}|'.format(str(list[0][0]), str(list[0][1]),
                                                   str(list[0][2])))
        App.printRow()

    @classmethod
    # (imc, status)
    def creatTableImc(cls, imc: float, status: str):
        '''Creates an IMC table.

        Args: 
            imc (float): The IMC value.
            status (str): The status of the IMC.

        Returns:
            list: A list containing the IMC analyze.
        '''
        content = [['Tabela de IMC', 'Intervalo', ' Status'],
                   ['Menos do que: ', '18,5', 'Abaixo do Peso !'],
                   ['Entre: ', '18,5 e 24,9', 'Peso Normal!'],
                   ['Entre: ', '25,0 e 29,9', 'Sobrepeso!'],
                   ['Entre: ', '30,0 e 34,9', 'Obesidade Grau 1!'],
                   ['Entre: ', '35,0 e 39,9', 'Obesidade Grau 2!'],
                   ['Mais do que: ', '40,0', 'Obesidade Grau 3!'],
                   ]

        result = [['SEU IMC: ', str(imc), status]]
        print()
        for printRow in range(0, len(content)):
            App.printRowTable()
            print('|{:^25s}||{:^25s}||{:^25s}|'.format(content[printRow][0], content[printRow][1],
                                                       content[printRow][2]))
            if printRow == 6:
                App.printRowTable()
                App.printResult(result)

    @classmethod
    def creatTableQtdCal(cls, dict):
        '''Creates a table displaying the quantity of calories for each nutrient.

        Args:
            dict (dict): A dictionary containing nutrient data, including 'carboidratos',
            'proteinas', and 'gorduras' as keys.

        Returns:
            The resulting table has three columns: the first column contains the nutrient names, 
            the second column contains the amount of calories in string format concatenated with the string "kcal",
            and the third column contains the amount of grams in string format concatenated with the string "g"
    '''
        content = [
            ["Carboidratos: ", dict["carboidratos"], round(
                float((dict["carboidratos"])) / 4.0, 2)],
            ["Proteínas: ", dict["proteinas"], round(
                float((dict["proteinas"])) / 4.0, 2)],
            ["Gorduras", dict["gorduras"], round(
                float((dict["gorduras"])) / 9.0, 2)]
        ]

        for printRow in range(0, len(content)):
            App.printRowTable()
            print('|{:^25}||{:^25}||{:^25}|'.format(str(content[printRow][0]), str(content[printRow][1]) + " kcal",
                                                    str(content[printRow][2]) + " g"))
            App.printRowTable()

    @classmethod
    def menu(cls, response):
        '''Displays an interactive menu with options related to calculating BMI, BMR and calorie count.

        Args:
            response (dict): A dictionary containing the calculation results.

        Returns:
            If the user selects option 1, the program will calculate and display the user’s 
            Body Mass Index (IMC) and its significance. 

            If the user selects option 2, the program will calculate and display the user’s 
            Basal Metabolic Rate (TMB) and its significance. 

            If the user selects option 3, the program will display information about calorie intake and its importance, and show a table with 
            the approximate number of calories the user should consume. 

            If the user selects option 4, the program will display a thank you message and exit. 

            If an invalid option is selected, an error message will be displayed.
        '''
        while True:
            App.padding()
            print("=> Selecione uma opção: \n")
            print('{:^16s}{:^18s}{:^18s}{:^18s}{:2s}'.format("1 - IMC", "2 - TMB", "3 -  QTD KCAL", "4 - SAIR", ""),
                  end="\t")
            opt = input()
            App.padding()

            if opt == "1":
                App.title("IMC")
                print("{:^81s}".format(
                    "O Indice de Massa Corporal (IMC) é um parâmetro"))
                print("{:^81s}".format(
                    "utilizado para saber se o peso está de acordo com a altura de um"))
                print(
                    "{:^81s}".format("indivíduo, o que pode interferir diretamente na sua saúde e qualidade de vida!"))
                App.creatTableImc(response["imc"], response["statusImc"])

            elif opt == "2":
                App.title("Taxa Metabólica Basal: ")
                print("{:^81s}".format(
                    "A Taxa de Metabolismo Basal (TMB) é a quantidade"))
                print("{:^81s}".format(
                    "mínima de energia (calorias) necessária para manter as"))
                print("{:^81s}".format(
                    "funções vitais do organismo em repouso. Essa taxa pode variar"))
                print("{:^81s}".format(
                    "de acordo com o sexo, peso, altura, idade e nível de atividade física."))

                result = [['RESULTADO :', 'SUA TMB:',
                           str(response['tmb']) + " kcal"]]
                App.printResult(result)

            elif opt == "3":
                nut = response["nutrientes"]
                App.title("Quantidade de Calorias: ")
                print("{:^81s}".format(
                    "Calorias são a quantidade de energia que um determinado alimento"))
                print("{:^81s}".format(
                    "fornece após ser consumido, contribuindo para as funções essenciais do"))
                print(
                    "{:^81s}".format("organismo, como respiração, produção de hormônios, e funcionamento do cérebro."))

                print()
                print("{:^81s}".format("Você deve consumir aproximadamente: \n"))
                App.creatTableQtdCal(nut)

                result = [['RESULTADO :', 'SUA QTD DE KCAL:',
                           str(response['cal']) + " kcal"]]
                App.printResult(result)

            elif opt == "4":
                print('{:^79s}'.format("Obrigado por usar nosso App !"))
                App.padding()
                App.printRow()
                break

            else:
                print("Erro: Opção Inválida!")
