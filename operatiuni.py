
from input_utils import *


class Client:
    
    def __init__(self, nume, cnp, nr_telefon, adresa):
        self.nume = nume
        self.cnp = cnp
        self.nr_telefon = nr_telefon
        self.adresa = adresa
        self.balanta = 0
        self.tranzactii = []
        
        

    def __str__(self):

        return self.nume + str(self.balanta)

    def retragere(self , suma):

        if self.balanta < suma :
            print("n-ai bani")
            return

        self.balanta = self.balanta - suma
        self.tranzactii.append(Tranzactie("retragere" ,self, suma ))




    def depunere(self, suma):

        self.balanta = self.balanta + suma
        self.tranzactii.append(Tranzactie("depunere" ,self  , suma))

    def transfer(self, destinatar , suma):
        if self.balanta < suma:
            print("No money")
            return
        self.balanta = self.balanta - suma
        destinatar.balanta = destinatar.balanta + suma
        self.tranzactii.append(Tranzactie("transfer" , self,  suma , destinatar))

    def statement(self):
            """
            Returns a list of all transactions made by the client.
            Each transaction is represented as a dictionary with the following keys:
            - timestamp: the timestamp of the transaction
            - type: the type of transaction (withdrawal, deposit, transfer)
            - amount: the amount of money involved in the transaction
            - counterparty: the name of the counterparty in case of a transfer (None otherwise)
            """
            statement = []
            for transaction in self.tranzactii:
                statement.append({
                    "timestamp": transaction.timestamp,
                    "type": transaction.tip_tranzactie,
                    "amount": transaction.suma,
                    "counterparty": transaction.destinatar.nume if transaction.destinatar else None
                })
            return statement

class Tranzactie:
    
    def __init__(self, tip_tranzactie ,expeditor, suma, destinatar = None):
        self.timestamp = transaction_timestamp()
        self.tip_tranzactie = tip_tranzactie
        self.expeditor = expeditor
        self.suma = suma
        self.destinatar = destinatar
        


    def __str__(self):
        if self.destinatar == None:

            return self.expeditor.nume + "|" +str(self.suma) + "|" + self.tip

        return self.expeditor.nume  + "|" + str(self.suma) + "|" + self.destinatar + "|" + self.tip


def creaza_client(clients_collection) -> Client:

    cnp = input('Intordu CNP: ')
    nume = introdu_nume('Numele noului client: ')
    telefon = input('Numar de telefon: ')
    adresa = input('Adresa: ')

    new_client = Client(nume, cnp, telefon, adresa)
    clients_collection.insert_one(new_client.__dict__)
    return new_client
    
    

def modifica_sold(client, valoare, dict_clients):
    """
    Functie care modifica soldul unui cont
    :param nume_client: text Numele clientului al carui sold trebuie modificat
    :param valoare: float Valoare cu care soldul va fi modificat. Poate fi pozitiva sau negativa.
    :return sold: float Soldul dupa ce a fost facuta mofidicarea
    """
    if valoare < 0:
        if abs(valoare) < dict_clients[nume_client]['sold']:
            client.retragere(valoare)
            rescrie_fisier_clienti(dict_clients)
        else:
            print('Sold insuficient pentru tranzactia dorita.')
    else:
        if valoare > 0:
            client.depunere(valoare)
    

def transfer(valoare, expeditor ,destinatar):
    # implementeaza logica pentru situatia "fonduri insuficiente"
    """
    Functie care face transferul unei sume de bani intre 2 conturi, cu conditia ca expeditorul sa dispuna de valoare care trebuie transferata
    :param valoare: float Valoare care urmeaza sa fie transferata
    :param nume_expeditor: str Numele expeditorului
    :param nume_destinatar: str Numele destinatarului
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """

    if valoare <= 0:
        print('Valoarea transferata trebuie sa fie pozitiva. Transferul nu a fost efectuat.')
    else:
        if expeditor.balanta >= valoare:
            print(f"Soldul initial al clientului {expeditor.name}: {expeditor.balanta}")
            print(f"Soldul initial al clientului {destinatar.name}: {destinatar.balanta}")
            expeditor.transfer(destinatar, valoare)
            print(f"Soldul final al clientului {expeditor.name}: {expeditor.balanta}")
            print(f"Soldul final al clientului {destinatar.name}: {destinatar.balanta}")
        else:
            print('Expeditorul nu are fonduri suficiente. Transferul nu a fost efectuat.')
    

def sterge_client(nume_client, clients_collection):

    result = clients_collection.delete_one({"nume": nume_client})
    if result.deleted_count == 1:
        print(f"Clientul {nume_client} a fost sters cu succes.")
    else:
        print(f"Nu s-a gasit clientul {nume_client} in baza de date.")





