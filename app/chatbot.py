import spacy
from nltk.corpus import stopwords
import nltk
import random
import json

nltk.download('stopwords')

class ChatBot:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")
        self.stop_words = set(stopwords.words('portuguese'))
        self.current_state = "init_message"
        self.sentiment = None  # Atributo para manter o sentimento detectado
        
        # Carregando palavras-chave de sentimentos do arquivo JSON
        with open('../static/sentiment_keywords.json', 'r') as file:
            self.sentiment_keywords = json.load(file)

        self.responses = {
            "init_message": "Olá! Como posso ajudar hoje?",
            "restart_message": "Espero que tenha te ajudado! Gostaria de me informar novamente como está se sentindo?",
            "follow_up": [
                "Como você está se sentindo hoje?",
                "Como foi o seu dia até agora?",
                "Está tudo bem por aí?"
            ],
            "negative_choice": "Sinto muito por isso... Você gostaria de um conselho ou um poema para ajudar a melhorar seu dia?",
            "positive_choice": "Fico feliz por isso! Você gostaria de um conselho ou um poema para melhorar ainda mais o seu dia?",
            "neutral_choice": "Entendi! Mas você gostaria de um conselho ou um poema para melhorar seu dia?",
            "conselho": {
                "positive": [
                    "Continue assim! Manter uma atitude positiva é ótimo para a saúde mental.",
                    "Mantenha o bom trabalho e lembre-se de cuidar de si mesmo.",
                    "A positividade é uma escolha diária com grande impacto na nossa vida.",
                    "Cultivar pensamentos positivos trará mais felicidade à sua vida.",
                    "Cada pequeno sorriso pode iluminar seu dia e o de outros também.",
                    "Celebre suas conquistas, não importa o quão pequenas elas sejam."
                ],
                "neutral": [
                    "A vida é uma série de altos e baixos, estar no meio é um bom lugar para começar.",
                    "Encontrar um equilíbrio é crucial; nem muito alto, nem muito baixo.",
                    "Manter a calma é a chave para superar os momentos de tédio ou indecisão.",
                    "Às vezes, ficar neutro é o melhor estado para fazer escolhas objetivas.",
                    "Explore novos interesses para adicionar um pouco de cor à sua rotina.",
                    "Permita-se ficar tranquilo, nem sempre precisamos estar em movimento."
                ],
                "negative": [
                    "Lembre-se, é completamente normal ter dias ruins.",
                    "Não perca a esperança, cada dia é uma nova oportunidade para mudar.",
                    "É importante aceitar os sentimentos negativos para superá-los.",
                    "Buscar ajuda e falar sobre seus sentimentos é um passo corajoso.",
                    "Todos nós passamos por momentos difíceis, você não está sozinho.",
                    "Faça pequenos passos todos os dias para sair deste estado, você consegue."
                ]
            },
            "poema": {
                "positive": [
                    "A alegria da vida vem em momentos simples, vividos de coração.",
                    "O sol brilha, trazendo energia e promessas de novos começos.",
                    "Cada sorriso seu ilumina o mundo, mantenha a luz brilhando.",
                    "Celebre a felicidade como se fosse uma constante renovação de esperança.",
                    "Viva cada dia com entusiasmo, como se fosse uma festa inesperada.",
                    "Sinta a energia positiva fluindo como uma poderosa onda de alegria."
                ],
                "neutral": [
                    "Caminhe calmamente, entre o barulho e a pressa, e lembre-se da paz que pode existir no silêncio.",
                    "A vida se desdobra em camadas, não apresse o processo, viva-o.",
                    "O mundo é vasto e suas possibilidades inúmeras, explore-as sem pressa.",
                    "Cada passo no meio termo é uma base sólida para o futuro.",
                    "Na tranquilidade, encontramos respostas que o tumulto esconde.",
                    "O equilíbrio é uma arte, pintada com as cores do cotidiano."
                ],
                "negative": [
                    "Mesmo na escuridão mais sombria, uma luz brilha em algum lugar. Segure-se a ela, mesmo que pequena.",
                    "Quando tudo parece perdido, lembre-se do renovo que cada amanhecer traz.",
                    "Dentro da noite mais escura, sussurros de esperança podem ser encontrados.",
                    "Não desista, a maré vai virar e trazer novos horizontes.",
                    "O abraço da noite esconde também estrelas brilhantes, olhe para cima.",
                    "O sol está apenas em uma pausa, logo retornará para iluminar seus dias."
                ]
            }
        }

    def preprocess(self, text):
        doc = self.nlp(text.lower())
        result = [token.text for token in doc if token.text not in self.stop_words and not token.is_punct]
        return result

    def analyze_sentiment(self, text):
        processed_text = self.preprocess(text)  # Retorna uma lista de palavras processadas
        positive_hits = sum(word in self.sentiment_keywords['positive'] for word in processed_text)
        negative_hits = sum(word in self.sentiment_keywords['negative'] for word in processed_text)
        
        if positive_hits > negative_hits:
            self.sentiment = "positive"
        elif negative_hits > positive_hits:
            self.sentiment = "negative"
        else:
            self.sentiment = "neutral"


    def respond(self, text):
        if self.current_state == "init_message":
            self.current_state = "follow_up"
            return random.choice(self.responses["follow_up"])
        elif self.current_state == "follow_up":
            self.analyze_sentiment(text)  # Certifique-se de passar o texto original aqui
            choice_state = self.sentiment + "_choice"
            self.current_state = choice_state
            return self.responses[choice_state]
        elif "choice" in self.current_state:
            choice = text.strip().lower()
            if choice in ["conselho", "poema"]:
                response = random.choice(self.responses[choice][self.sentiment])
                self.current_state = "restart_message"  # Reset state after response
                return response
            else:
                return "Você pode escolher entre 'conselho' ou 'poema'. Qual você prefere?"
        elif self.current_state == "restart_message":
            self.current_state = "init_message"  # Reset to initial state
            return self.responses["restart_message"]

if __name__ == '__main__':
    bot = ChatBot()
    user_input = ""  # Inicializa user_input para entrar no loop corretamente

    while True:
        if bot.current_state != "restart_message":
            user_input = input("Você: ")
        else:
            user_input = ""

        # Processa a entrada do usuário (ou vazia, se o estado for 'restart_message')
        response = bot.respond(user_input)
        print("Bot: ", response, "\n")