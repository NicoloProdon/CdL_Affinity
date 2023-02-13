from random import choice
from pandas import DataFrame, read_csv
from os import path


class Dataset:

    training: DataFrame = None

    def __init__(self, training: str):
        self.training_path = training

    # dataset creation
    @classmethod
    def generate(cls):
        dataset = DataFrame(columns=('Life', 'Work', 'Stem', 'Math', 'Institute',
                                     'AsoProg', 'AiReti', 'BasiAsd', 'Affinity'), dtype=int)
        possible_val = [0, 1]
        life = []
        work = []
        stem = []
        math = []
        institute = []
        subjects1 = []
        subjects2 = []
        subjects3 = []
        affinity = []

        # for every item choose 0 or 1, create 10000 combinations
        for i in range(0, 10000):
            life.append(choice(possible_val))
            work.append(choice(possible_val))

            stem_val = choice(possible_val)
            math_val = choice(possible_val)
            institute_val = choice(possible_val)

            sub1_val = choice(possible_val)
            sub2_val = choice(possible_val)
            sub3_val = choice(possible_val)

            stem.append(stem_val)
            math.append(math_val)
            institute.append(institute_val)
            subjects1.append(sub1_val)
            subjects2.append(sub2_val)
            subjects3.append(sub3_val)

            # affinity value decision
            if sub1_val == 1 and sub2_val == 1 and sub3_val == 1:
                affinity.append(1)
            elif ((sub1_val + sub2_val + sub3_val) / 3) > 0.6 \
                    and (stem_val == 1 or math_val == 1 or institute_val == 1):
                affinity.append(1)
            else:
                affinity.append(0)

        dataset["Life"] = life
        dataset["Work"] = work
        dataset["Stem"] = stem
        dataset["Math"] = math
        dataset["Institute"] = institute
        dataset["AsoProg"] = subjects1
        dataset["AiReti"] = subjects2
        dataset["BasiAsd"] = subjects3
        dataset["Affinity"] = affinity

        return dataset

    # load an existing dataset or generate a new one
    def load_dataset(self):
        if path.exists("data/dataset.csv"):
            self.training = read_csv("data/dataset.csv")
            print("\nDATASET CARICATO CON SUCCESSO!")
        else:
            self.training = self.generate()
            self.training.to_csv(self.training_path)
            print("\nDATASET CREATO CON SUCCESSO!")
