import requests as req
import json
import html
import random

url1 = "https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=boolean"
url2 = "https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple"


def get_quizTF():

    try:
        response = req.get(url1)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        if data["response_code"] == 0:
            return data["results"]
        else:
            print("Error fetching quiz data:", data["response_code"])
            return []

    except req.RequestException as e:
        print("Request failed:", e)
        return []


def get_quiz():
    try:
        response = req.get(url2)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        if data["response_code"] == 0:
            return data["results"]
        else:
            print("Error fetching quiz data:", data["response_code"])
            return []

    except req.RequestException as e:
        print("Request failed:", e)
        return []


def format_question(question):
    # Decode HTML entities in the question text
    return html.unescape(question["question"])


def format_answer(question):
    # Decode HTML entities in the answer text
    return html.unescape(question["correct_answer"])


def get_score():
    try:
        with open("score.json", "r") as f:
            scores = json.load(f)
            sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
            scores = sorted_scores[:10]  # Get top 10 scores
            print("🏆 Scoreboard:")
            for idx, score in enumerate(scores, start=1):
                print(f"{idx}. {score['name']}: {score['score']}")
    except FileNotFoundError:
        print("No previous scores found.")
        return []
    except IOError as e:
        print(f"Error reading score file: {e}")
        return []


def store_score(type, difficulty, category, score, name):
    score_data = {
        "name": name,
        "type": type,
        "difficulty": difficulty,
        "category": category,
        "score": score,
    }
    try:
        with open("score.json", "r") as f:
            score_list = json.load(f)
    except FileNotFoundError:
        score_list = []
    score_list.append(score_data)

    try:
        with open("score.json", "w") as f:
            json.dump(score_list, f, indent=4)
    except IOError as e:
        print(f"Error writing to score file: {e}")
        return


def get_name():
    while True:
        name = input("Enter your name: ").strip()
        if name:
            return name
        print("Name cannot be empty. Please enter a valid name.")


def main():
    print("\n")
    print("🎉 Welcome to the Quiz Game!")
    print("\nChoose what to do:")
    print("1. 🤔 Play True/False Quiz")
    print("2. 🧠 Play Multiple Choice Quiz")
    print("3. 📊 View Scoreboard")
    print("4. 🚪 Exit")

    while True:
        choice = input("\nEnter your choice (1/2/3/4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            break
        print("Invalid input. Please enter a valid option.")

    score = 0
    numofquestion = 0

    if choice == "1":
        print("Fetching True/False quiz questions...")
        questions = get_quizTF()
        print("Quiz questions fetched successfully!\n")
        if not questions:
            print("No questions available. Please try again later.")
            return

        name = get_name()
        for i, question in enumerate(questions, start=1):
            formatted_question = format_question(question)
            formatted_answer = format_answer(question)
            while True:
                print("\n")
                print(f"Q{i}: {formatted_question}")
                print("true or false?")
                answer = input("(T/F): ").strip().upper()
                if answer not in ["T", "F"]:
                    print("Invalid input. Please enter 'T' for True or 'F' for False.")
                if answer in ["T", "F"]:
                    break

            answer = "True" if answer == "T" else "False"

            if answer == formatted_answer:
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")

            numofquestion = i
        type = "T/F"
        difficulty = "Easy"
        category = "Animal"
        store_score(type, difficulty, category, score, name)
    elif choice == "2":
        print("Fetching Multiple Choice quiz questions...")
        questions = get_quiz()
        if not questions:
            print("No questions available. Please try again later.")
            return
        print("Quiz questions fetched successfully!\n")
        name = get_name()
        for i, question in enumerate(questions, start=1):
            formatted_question = format_question(question)
            formatted_choices = [html.unescape(question["correct_answer"])] + [
                html.unescape(ans) for ans in question["incorrect_answers"]
            ]
            random.shuffle(formatted_choices)
            formatted_correctanswers = format_answer(question)
            while True:
                print("\n")
                print(f"Q{i}: {formatted_question}")
                for idx, option in enumerate(formatted_choices, start=1):
                    print(f"{idx}. {option}")
                answer = input("Choose 1/2/3/4: ").strip().upper()
                if answer not in ["1", "2", "3", "4"]:
                    print("Invalid input. Please enter a valid choice")
                if answer in ["1", "2", "3", "4"]:
                    break
            selected_answer = formatted_choices[int(answer) - 1]
            if selected_answer == formatted_correctanswers:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer was: {formatted_correctanswers}")

            numofquestion = i
        type = "MCQ"
        difficulty = "Easy"
        category = "Animal"
        store_score(type, difficulty, category, score, name)
    elif choice == "3":
        get_score()
        return
    elif choice == "4":
        print("Exiting the quiz game. Tata!")
        return

    if score == 10:
        print("\n🎉 Woooooooo! You got a perfect score of 10/10! 🧠✨")
        print("You are a genius! 👑😎")
    elif 10 > score >= 6:
        print(f"\n👏 Great job! You scored {score} out of {numofquestion}. 🏅")
        print("Now, You are a quiz master! 🧠💡")
    elif 6 > score >= 4:
        print(f"\n👍 Good effort! You scored {score} out of {numofquestion}. 🤓")
        print("Try again! 🌀📚")
    elif 4 > score:
        print(f"\nYou scored {score} out of {numofquestion}. 🤦‍♂️")
        print("Congrats! You are considered dumb by me! 🐢💩")

    print("\n🎮 Thanks for playing the quiz game! 🥳")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the quiz game. Tata!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting the quiz game. Tata!")
        exit(1)
