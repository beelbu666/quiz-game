import requests as req
import json
import html

url = 'https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=boolean'
def get_quiz():
    try:
        response = req.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        with open('quiz.json', 'w') as f:
            json.dump(data, f, indent=4)
        if data['response_code'] == 0:
            return data['results']
        else:
            print("Error fetching quiz data:", data['response_code'])
            return []
        
    except req.RequestException as e:
        print("Request failed:", e)
        return []
def format_question(question):
    # Decode HTML entities in the question text
    return html.unescape(question['question'])
def format_answer(answer):
    # Decode HTML entities in the answer text
    return html.unescape(answer['correct_answer'])

def main():
    get_quiz()
    with open('quiz.json','r') as f:
        data=json.load(f)
    questions = data.get('results', [])
    score = 0
    numofquestion= 0
    
    for i, question in enumerate(questions, start=1):
        formatted_question = format_question(question)
        formatted_answer = format_answer(question)
        while True:
            print('\n')
            print(f"Q{i}: {formatted_question}")
            print("true or false?")
            answer=input("(T\F): ").strip().upper()
            if answer not in ['T', 'F']:
                print("Invalid input. Please enter 'T' for True or 'F' for False.")
            if answer in ['T', 'F']:
                break
        if answer == 'T':
            answer = 'True'
            if answer == formatted_answer:
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
        elif answer == 'F':
            answer = 'False'
            if answer == formatted_answer:
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
        print('\n')
        numofquestion=i

    print(f"Your score is {score} out of {numofquestion}")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the quiz game. Tata!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting the quiz game. Tata!")
        exit(1)
