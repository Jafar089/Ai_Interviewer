# import the libraries
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
import spacy
nlp = spacy.load("en_core_web_sm")

# for text to speech
import pyttsx3
import speech_recognition as sr
import time

# for communication skills
from textstat import textstat

# Initialization of the TTS engine
my_engine = pyttsx3.init()
voices = my_engine.getProperty('voices')
my_engine.setProperty('voice', voices[1].id)

# download the necessary resources for the nltk library

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('vader_lexicon')

class TakingInterview:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def Info_About_Ai_Hr(self):
        information = (f"Hi,{self.name}, I am an Ai assistant and my duty is to take an interview from you. And I already know you are applying for the position of {self.role}, I go through your resume, So let's start the interview.")
        print(information)
        
        # set the properties of the TTS engine that how the voice should be
        my_engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        my_engine.setProperty('volume', 1)  # Volume 0-1

        # speak the information of the candidate
        my_engine.say(information)

        # Blocks while processing all the incoming and outgoing messages
        my_engine.runAndWait()


    def Get_User_Answers_List(self, question_list, timeout):
        recognizer = sr.Recognizer()
        user_responses = []
        count = 0

        for question in question_list:
            print(f"Question: {count+1} => {question}")
            if count == 1:
                my_engine.say("Great, let's move to the next question")
                my_engine.runAndWait()
            if count == 2:
                my_engine.say("Sounds good, now my third question is")
                my_engine.runAndWait()
            
            if count == 3:
                my_engine.say("ok, and the next question is")
                my_engine.runAndWait()
            
            if count == 4:
                my_engine.say("tell me about like")
                my_engine.runAndWait()

            my_engine.say(question)
            my_engine.runAndWait()
            print("You have 2 minutes to speak your answer.")

            with sr.Microphone() as source:
                print("Listening for your answer...")
                recognizer.adjust_for_ambient_noise(source)
                try:
                    # Listen for the answer (with a timeout of 2 minutes)
                    audio = recognizer.listen(source, timeout=timeout)
                    # Recognize speech using Google Speech Recognition
                    answer = recognizer.recognize_google(audio)
                    print(f"Your answer: {answer}")
                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio.")
                    answer = "Unintelligible answer"
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    answer = "Request error"
                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for phrase to start.")
                    answer = "Timeout"
                
                # Append the answer to the answer list
                user_responses.append(answer)
            count += 1

        return user_responses


    def Get_Response_From_Api(self, url):
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, params={"action":'interviewQuestions'})  # Send as JSON
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response as a dictionary
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    
    def Return_list_of_questions(self, response_data):

        if response_data:

            question_list = ['Can you Please Introduce yourself?']  # Create an empty list to store questions

            # Iterate over the list of questions
            for idx, question in enumerate(response_data, start=1):
                question_text = question.get('question_text')  # Get the question text
                
                # Check if question text exists
                if question_text:
                    # Create a variable for each question
                    locals()[f'question_{idx}'] = question_text
                    
                    # Add the question to the list
                    question_list.append(question_text)
            # return the list of questions
            question_list.append('And now my last question to you is Why do you want to work with us?')
            return question_list
        else:
            print("Failed to retrieve data from the API.")


    # Function to analyze sentiment
    def analyze_sentiment(self, text):
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        # print(f"Sentiment Analysis: {sentiment}")

        confidence_level = sentiment['compound']
        if confidence_level >= 0.5:
            confidence = "High"
        elif confidence_level > 0:
            confidence = "Moderate"
        else:
            confidence = "Low"

        print(f"\nConfidence Level: {confidence}")

    # check the communicaiton skills of the candidate
    def communication_skills(self, text):
        # check the readability score
        readability = textstat.flesch_reading_ease(text)
        
        doc = nlp(text)
        # check the sentence complexity
        complex_sentences = sum(1 for sent in doc.sents if len(sent) > 20)

        # check the unique words
        doc1 = nlp(text)
        tokens = [token.text for token in doc1 if token.is_alpha]
        unique_tokens = set(tokens)
        ttr = len(unique_tokens) / len(tokens)

        # check the part of speech tagging
        doc2 = nlp(text)
        # Check for part-of-speech tagging errors
        pos_errors = sum(1 for token in doc2 if token.pos_ == 'X')

        assessment = {
        "Readability Score": readability,
        "Complex Sentences": complex_sentences,
        "Type-Token Ratio": ttr,
        "POS Errors": pos_errors
        }

        print("\nCommunication Skills Assessment:")
        for key, value in assessment.items():
            print(f"{key}: {value}")



# Create an instance of the TakingInterview class
interview = TakingInterview("Jafar", "Data Scientist")

# call function to get the response from the api and store it in a variable
response_data = interview.Get_Response_From_Api('https://bestfithiring.com/api/index.php')

# # call the function to give the information about the Ai Hr
interview.Info_About_Ai_Hr()

# call the function to return the list of questions
mylist = interview.Return_list_of_questions(response_data)

# call the function to get the user answers
timeout = 120
Answers = interview.Get_User_Answers_List(mylist, timeout)
# print(Answers)

# call the function to check the confidence level
for i in Answers:
    interview.analyze_sentiment(i)

# call the function to check the communication skills
for text in Answers:
    interview.communication_skills(text)