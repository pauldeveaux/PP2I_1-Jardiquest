from jardiquest.model.path.suggestion_model import glouton_solution
from time import monotonic as time
import random
from datetime import date
import matplotlib.pyplot as plt

nb_Tests = 10
step_data_size = 500

times = {}



class Recolte:
    def __init__(self, idRecolte, quantity, date, cost, qtt_recommandee, idCatalogue, idJardin):
        self.idRecolte = idRecolte
        self.quantity = quantity
        self.date = date
        self.cost = cost
        self.qtt_recommandee = qtt_recommandee
        self.idCatalogue = idCatalogue
        self.idJardin = idJardin


for data_size in range(1, nb_Tests*step_data_size+1, step_data_size):
    
    # Creation of dataset
    recoltes = []
    for i in range(1, data_size):
        recolte = Recolte(i, random.randint(1,100), date.today(), random.randint(1,100), random.randint(1,20), random.randint(1,97), 1)
        recoltes.append(recolte)

    startTime = time()
    glouton_solution(recoltes, 999999999999)
    totalTime = time() - startTime
    times[data_size] = totalTime

plt.plot(list(times.keys()), list(times.values()))
plt.xlabel("Data size")
plt.ylabel("Execution time in seconds")
plt.show()
