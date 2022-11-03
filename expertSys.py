from experta import KnowledgeEngine, Fact, DefFacts, Rule, OR, AND
from interface import valid_answer


# booting expert system
def start_expert():
    engine = ExpertSys()
    engine.reset()
    engine.run()


class ExpertSys(KnowledgeEngine):

    # initial question
    @DefFacts()
    def _initial_action(self):
        yield Fact(question=True)

    # minimum interest questions
    @Rule(Fact(question=True))
    def ask_min(self):
        self.declare(Fact(life=valid_answer("\n1) Pensi che la tecnologia stia influenzando tanto la tua vita?")))
        self.declare(Fact(work=valid_answer("2) L'informatica e' per te importante nel mondo del lavoro?")))

    # medium interest questions
    @Rule(Fact(min_interest=True))
    def ask_med(self):
        self.declare(Fact(stem=valid_answer("\n3) Sei interessato alle materie di indirizzo tecnologico-scientifico?")))
        self.declare(Fact(math=valid_answer("4) Sei disposto ad approfondire argomenti matematici?")))
        self.declare(Fact(school=valid_answer(
            "5) Hai frequentato un istituto secondario di 2° grado, settore Informatica?")))

    # high interest questions
    @Rule(AND(Fact(mid_interest=True), Fact(school=True)))
    def ask0_high(self):
        self.declare(Fact(feedback0=valid_answer("\n6) Ti sono piaciuti gli argomenti trattati nei 5 anni di scuola?")))

    @Rule(AND(Fact(mid_interest=True), Fact(school=False)))
    def ask1_high(self):
        self.declare(Fact(feedback1=valid_answer(
            "\n6a) Ti piacerebbe conoscere il mondo della programmazione o l'architettura di una macchina?")))
        self.declare(Fact(feedback2=valid_answer(
            "6b) Ti interessa sviluppare intelligenze artificiali o conoscere il funzionamento delle reti?")))
        self.declare(Fact(feedback3=valid_answer(
            "6c) Ti piacerebbe gestire basi di dati o studiare algoritmi e strutture dati")))

    # interest absence rules
    @Rule(
        OR(
            AND(Fact(life=False), Fact(work=False)),
            AND(Fact(stem=False), Fact(math=False), Fact(school=False)),
            AND(Fact(school=False), Fact(feedback1=False), Fact(feedback2=False), Fact(feedback3=False))
        )
    )
    def no_interest(self):
        self.declare(Fact(min_interest=False), Fact(mid_interest=False))

    @Rule(Fact(min_interest=False))
    def null_interest(self):
        print("\n**Siamo spiacenti! La facolta' non potrebbe in ALCUN MODO soddisfarti. Iscrizione NON consigliata**")
        self.reset()

    # low interest rules
    @Rule(OR(Fact(life=True), Fact(work=True)))
    def min(self):
        self.declare(Fact(min_interest=True))

    @Rule(OR(
            Fact(feedback0=False),
            AND(Fact(min_interest=True), Fact(mid_interest=False), Fact(max_interest=False))
         )
    )
    def minimum_interest(self):
        print("\n**La facolta' soddisfa POCHE tue esigenze, iscrizione NON consigliata**.")
        self.reset()

    # medium interest rules
    @Rule(OR(Fact(stem=True), Fact(math=True), Fact(school=True)))
    def mid(self):
        self.declare(Fact(mid_interest=True))

    @Rule(
        OR(
            AND(Fact(mid_interest=True), Fact(max_interest=False)),
            AND(Fact(school=False),
                OR(
                    AND(Fact(feedback1=True), Fact(feedback2=False), Fact(feedback3=False)),
                    AND(Fact(feedback1=False), Fact(feedback2=True), Fact(feedback3=False)),
                    AND(Fact(feedback1=False), Fact(feedback2=False), Fact(feedback3=True)),
                  )
                )
        )
    )
    def medium_interest(self):
        print("\n**La facolta' soddisfa MEDIAMENTE le tue esigenze, iscrizione CONSIGLIATA**")
        self.reset()

    # high interest rules for IT students
    @Rule(AND(Fact(school=True), Fact(feedback0=True)))
    def max_0(self):
        self.declare(Fact(max_interest=True))

    # high interest rules for other type of students
    @Rule(
        AND(
            Fact(school=False),
            OR(
                AND(Fact(feedback1=True), Fact(feedback2=True), Fact(feedback3=False)),
                AND(Fact(feedback1=True), Fact(feedback2=False), Fact(feedback3=True)),
                AND(Fact(feedback1=False), Fact(feedback2=True), Fact(feedback3=True)),
                AND(Fact(feedback1=True), Fact(feedback2=True), Fact(feedback3=True))
            )
        )
    )
    def max_1(self):
        self.declare(Fact(max_interest=True))

    @Rule(Fact(max_interest=True))
    def high_interest(self):
        print("\n**Complimenti! La facolta' soddisfa MOLTO le tue esigenze, iscrizione CALDAMENTE consigliata**")
        self.reset()
