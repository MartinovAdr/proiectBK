



import certifi as certifi
import pymongo
from operatiuni import *
from input_utils import introdu_nume, introdu_numar
from IPython.display import clear_output
#from admin_date import *

db_client = pymongo.MongoClient("mongodb+srv://Bank:q1w2e3r4t5y6@cluster0.kxf8asm.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

db = db_client["bankingDB"]
clients_collection = db["clienti"]


while True:
    print("""
    Meniu:

    1. Creaza Client nou
    2. Afiseaza clientii (scrie filtru optional)
    3. Verifica soldul unui client
    4. Modifica soldul (depunere / retragere)
    5. Transfer intre clienti
    6. Genereaza extras de cont
    7. Sterge date client (inchidere cont)
    8. Exit
    """)
    optiune = input('alege un numar din meniu: ')

    if optiune == '1':
        client_nou = creaza_client(clients_collection)
        if client_nou:
            print(f"Clientul {client_nou.nume} a fost creat cu succes!")
        else:
            print("A aparut o eroare la crearea clientului.")

    elif optiune == '2':
        print("""--------------------------------------------------------
Lista clientilor:
        """)
        clients_names = clients_collection.find({}, {"_id": 0, "nume": 1})
        for name in clients_names:
            print(name["nume"])
        print('Clientul a fost adaugat cu succes!')

    elif optiune == '3':
        nume_client = introdu_nume('Numele clientului: ')
        balanta_clienti = clients_collection.find({"nume" : nume_client}, {"balanta": 1, "_id": 0})
        for clienti in balanta_clienti:
            print(clienti)

    elif optiune == '4':
        nume_client = introdu_nume('Numele clientului: ')

        valoare = introdu_numar(f'Valoarea cu care se modifica soldul clientului "{nume_client}": ')

        balanta_client = clients_collection.find_one({"nume": nume_client}, {"balanta": 1, "_id": 0})
        clients_collection.update_one({"nume": nume_client}, {"$set": {"balanta": balanta_client["balanta"] + valoare}})
        print(balanta_client)
        print()

    elif optiune == '5':
        valoare = introdu_numar('Valoarea transferului: ')
        nume_expeditor = introdu_nume('Numele clientului expeditor: ')
        nume_destinatar = introdu_nume('Numele clientului destinatar: ')
        balanta_client = clients_collection.find_one({"nume": nume_expeditor}, {"balanta": 1, "_id": 0})
        balanta_client_destinatar = clients_collection.find_one({"nume": nume_destinatar}, {"balanta": 1, "_id": 0})
        clients_collection.update_one({"nume": nume_expeditor}, {"$set": {"balanta": balanta_client["balanta"] - valoare}})
        clients_collection.update_one({"nume": nume_destinatar},
                                      {"$set": {"balanta": balanta_client_destinatar["balanta"] + valoare}})
        print("Transferul a fost efectuat cu succes.")



    elif optiune == '6':

        nume_client = introdu_nume('Numele clientului: ')

        client = clients_collection.find_one({"nume": nume_client})

        if client:

            print(f"Extras de cont pentru clientul {client}:")

            transactions = client["tranzactii"]

            for transaction in transactions:
                print(f"{transaction}")
                if transaction["type"] == "Depunere":

                    print(f"{transaction['timestamp']}: Depunere {transaction['amount']} RON")

                elif transaction["type"] == "Retragere":

                    print(f"{transaction['timestamp']}: Retragere {transaction['amount']} RON")

                elif transaction["type"] == "Transfer":

                    print(
                        f"{transaction['timestamp']}: Transfer {transaction['amount']} RON catre {transaction['counterparty']}")

            print(f"Sold curent: {client['balanta']} RON")

        else:

            print(f"Clientul {nume_client} nu exista in baza de date.")



    elif optiune == '7':
        nume_client = introdu_nume('Numele clientului: ')
        sterge_client(nume_client, clients_collection)


    elif optiune == '8' or optiune == 'exit':
        db_client.close()
        print("La revedere!")
        break

