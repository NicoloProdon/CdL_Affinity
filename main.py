from interface import menu, wait
from expertSys import start_expert
from bayesNet import start_bayes
from dataset import Dataset

if __name__ == '__main__':
    print("\nBENVENUTO NEL SISTEMA DI CALCOLO DELL'AFFINITA' AL CDL IN INFORMATICA")

    # first menu to choose a model
    title = "\nMODELLI A DISPOSIZIONE:"
    options = [
        "Valutazione tramite modello esperto ",
        "Valutazione tramite rete Bayesiana",
        "Uscita dal programma"
    ]

    choice = 0
    while choice != 3:
        choice = menu(title, options)

        if choice == 1:
            print("\n*Valutazione con MODELLO ESPERTO*")
            start_expert()

        # second menu to choose type of bayesian diagnostic
        if choice == 2:
            subTitle = "\nSONO DISPONIBILI 2 DIVERSE OPZIONI:"
            subOptions = [
                "Rete bayesiana ideale (senza apprendimento da dataset)",
                "Rete bayesiana con stimatore di massima verosimiglianza (con apprendimento da dataset)",
            ]

            subChoice = menu(subTitle, subOptions)
            if subChoice == 1:
                print("\n*Valutazione con rete bayesiana IDEALE*")
                dataset = None
                start_bayes(dataset, "normal")
            if subChoice == 2:
                print("\n*Valutazione con rete bayesiana con STIMATORE DI MASSIMA VEROSOMIGLIANZA*")
                dataset = Dataset("data/dataset.csv")
                Dataset.load_dataset(dataset)
                start_bayes(dataset, "maximumlikelihood")
        if choice != 3:
            wait()
