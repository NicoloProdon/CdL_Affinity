from bnlearn import query2df, make_DAG, parameter_learning, inference
from interface import valid_answer
from pgmpy.factors.discrete import TabularCPD


# booting bayesian network system
def start_bayes(dataset, method: str = "ideal" or "maximumlikelihood"):

    # user input values collecting
    evidences = {
        'Life': int(valid_answer("\n1) Pensi che la tecnologia stia influenzando tanto la tua vita?")),
        'Work': int(valid_answer("2) L'informatica e' per te importante nel mondo del lavoro?")),
        'Stem': int(valid_answer("\n3) Sei interessato alle materie di indirizzo tecnologico-scientifico?")),
        'Math': int(valid_answer("4) Sei disposto ad approfondire argomenti matematici?")),
        'Institute': int(valid_answer("5) Hai frequentato un istituto secondario di 2° grado, settore Informatica?")),
        'AsoProg': int(valid_answer(
            "\n6) Ti piacerebbe conoscere il mondo della programmazione o l'architettura di una macchina?")),
        'AiReti': int(valid_answer(
            "7) Ti interessa sviluppare intelligenze artificiali o conoscere il funzionamento delle reti?")),
        'BasiAsd': int(valid_answer(
            "8) Ti piacerebbe gestire basi di dati o studiare algoritmi e strutture dati?"))
    }
    bayes_network = BayesDiagnostic()

    # if user choose second method, system requires learning from existing dataset
    if method == "maximumlikelihood":
        bayes_network.learn_from_dataset(dataset.training, method)

    # calculating of total probability using inference
    res = query2df(bayes_network.inference(evidences))
    affinity = (res["p"])[1] * 100
    print("\nLa compatibilita' con il CdL in Informatica e' del %d" % affinity + "%")

    if affinity >= 75:
        print("\n**Complimenti! La facolta' soddisfa molto le tue esigenze, iscrizione CALDAMENTE consigliata**")
    elif affinity >= 60:
        print("\n**La facolta' soddisfa mediamente le tue esigenze, iscrizione CONSIGLIATA**")
    elif affinity >= 40:
        print("\n**La facolta' soddisfa solo ALCUNE tue esigenze, si consiglia RIFLESSIONE prima dell'iscrizione**.")
    elif affinity >= 20:
        print("\n**La facolta' soddisfa POCO le tue esigenze, iscrizione NON consigliata**.")
    else:
        print("\n**Siamo spiacenti! La facolta' non potrebbe in ALCUN MODO soddisfarti. Iscrizione NON consigliata**")

    if evidences['AsoProg'] == 1 or evidences['AiReti'] == 1 or evidences['BasiAsd'] == 1:
        print("\n**IL SISTEMA HA VALUTATO POSITIVAMENTE L'INTERESSE VERSO:")
        if evidences['AsoProg'] == 1:
            print("- Arichitettura degli Eleboratori e Sistemi Operativi, Programmazione")
        if evidences['AiReti'] == 1:
            print("- Ingegneria della Conoscenza e Reti di Calcolatori")
        if evidences['BasiAsd'] == 1:
            print("- Basi Di Dati e Algoritmi e Strutture Dati")

    if evidences['AsoProg'] == 0 or evidences['AiReti'] == 0 or evidences['BasiAsd'] == 0:
        print("\n**IL SISTEMA HA VALUTATO NEGATIVAMENTE IL DISINTERESSE VERSO:")
        if evidences['AsoProg'] == 0:
            print("- Arichitettura degli Eleboratori e Sistemi Operativi, Programmazione")
        if evidences['AiReti'] == 0:
            print("- Ingegneria della Conoscenza e Reti di Calcolatori")
        if evidences['BasiAsd'] == 0:
            print("- Basi Di Dati e Algoritmi e Strutture Dati")


class BayesDiagnostic:

    def __init__(self):
        self.Edges = [('Affinity', 'Life'),
                      ('Affinity', 'Work'),
                      ('Affinity', 'Stem'),
                      ('Affinity', 'Math'),
                      ('Affinity', 'Institute'),
                      ('Affinity', 'AsoProg'),
                      ('Affinity', 'AiReti'),
                      ('Affinity', 'BasiAsd'),
                      ]

        self.LifeCPT = TabularCPD(variable='Life',
                                  variable_card=2,
                                  values=[[0.53, 0.47], [0.47, 0.53]],
                                  evidence=['Affinity'],
                                  evidence_card=[2])
        self.WorkCPT = TabularCPD(variable="Work",
                                  variable_card=2,
                                  values=[[0.53, 0.47], [0.47, 0.53]],
                                  evidence=['Affinity'],
                                  evidence_card=[2])
        self.StemCPT = TabularCPD(variable='Stem',
                                  variable_card=2,
                                  values=[[0.65, 0.35], [0.35, 0.65]],
                                  evidence=['Affinity'],
                                  evidence_card=[2])
        self.MathCPT = TabularCPD(variable='Math',
                                  variable_card=2,
                                  values=[[0.65, 0.35],
                                          [0.35, 0.65]],
                                  evidence=['Affinity'],
                                  evidence_card=[2])
        self.InstituteCPT = TabularCPD(variable="Institute",
                                       variable_card=2,
                                       values=[[0.65, 0.50], [0.35, 0.50]],
                                       evidence=['Affinity'],
                                       evidence_card=[2])
        self.AsoProgCPT = TabularCPD(variable='AsoProg',
                                     variable_card=2,
                                     values=[[0.80, 0.20], [0.20, 0.80]],
                                     evidence=['Affinity'],
                                     evidence_card=[2])
        self.AiRetiCPT = TabularCPD(variable="AiReti",
                                    variable_card=2,
                                    values=[[0.80, 0.20], [0.20, 0.80]],
                                    evidence=['Affinity'],
                                    evidence_card=[2])
        self.BasiAsdCPT = TabularCPD(variable='BasiAsd',
                                     variable_card=2,
                                     values=[[0.80, 0.20], [0.20, 0.80]],
                                     evidence=['Affinity'],
                                     evidence_card=[2])
        self.AffinityCPT = TabularCPD(variable='Affinity',
                                      variable_card=2,
                                      values=[[0.50],
                                              [0.50]])

        self.DAG = make_DAG(self.Edges,
                            CPD=[self.LifeCPT, self.WorkCPT, self.StemCPT, self.InstituteCPT,
                                 self.MathCPT, self.AsoProgCPT, self.AiRetiCPT, self.BasiAsdCPT, self.AffinityCPT],
                            verbose=0
                            )

    def inference(self, evidences):
        return inference.fit(self.DAG, variables=['Affinity'], evidence=evidences, verbose=0)

    # only if user choose bayesian diagnostic with MLE
    def learn_from_dataset(self, dataset, method):
        self.DAG = make_DAG(self.Edges, verbose=0)
        self.DAG = parameter_learning.fit(self.DAG, dataset, methodtype=method, verbose=0)
