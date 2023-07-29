import pandas as pd
import tkinter.font as font
from tkinter import *
from tkinter import filedialog
from sklearn.linear_model import LogisticRegression
import textract


class TrainModel:
    def training(self):
        info = pd.read_csv('training_dataset.csv')
        array = info.values

        for i in range(len(array)):
            if array[i][0] == "Male":
                array[i][0] = 1
            else:
                array[i][0] = 0

        data = pd.DataFrame(array)

        maindata = data[[0, 1, 2, 3, 4, 5, 6]]
        mainarray = maindata.values

        personality = data[7]
        train_p = personality.values

        self.mul_lr = LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.mul_lr.fit(mainarray, train_p)

    def testing(self, test_data):
        try:
            predict_test = list()
            for i in test_data:
                predict_test.append(int(i))
            p_pred = self.mul_lr.predict([predict_test])
            return p_pred
        except:
            print("All Factors For Finding Personality Not Entered!")


def predict_person():
    root.withdraw()

    top = Toplevel()
    top.geometry('700x500')
    top.configure(background='#2b6777')
    top.title("Personality Prediction")

    title = font.Font(family='Edwardian Script ITC', size=35, weight='bold')
    Label(top, text="Personality Prediction", fg='white', bg='#2b6777', font=title, pady=30).pack()

    qstn_font = font.Font(family='Baskerville Old Face', size=12)
    Label(top, text="What is your name?", fg='white', bg='#2b6777', font=qstn_font).place(x=70, y=130)
    Label(top, text="How old are you?", fg='white', bg='#2b6777', font=qstn_font).place(x=70, y=160)
    Label(top, text="You identify as", fg='white', bg='#2b6777', font=qstn_font).place(x=70, y=190)
    Label(top, text="Attach your CV (PDF/DOCX):", fg='white', bg='#2b6777', font=qstn_font).place(x=70, y=220)

    sName=Entry(top)
    sName.place(x=450, y=130, width=160)
    age=Entry(top)
    age.place(x=450, y=160, width=160)
    gender = IntVar()
    R1 = Radiobutton(top, text="Male", variable=gender, value=1, padx=14)
    R1.place(x=450, y=190)
    R2 = Radiobutton(top, text="Female", variable=gender, value=0, padx=6)
    R2.place(x=534, y=190)
    file_entry = Entry(top, width=40)
    file_entry.place(x=450, y=220, width=160)
    browse_btn = Button(top, text="Browse", bg='black', fg='white', font=('Bookman Old Style', 8), command=lambda: select_file(file_entry))
    browse_btn.place(x=500, y=250)

    submitBtn = Button(top, text="Analyze and Predict", fg='white', bg='PaleGreen4', font=('Bookman Old Style', 12))
    submitBtn.config(command=lambda: analyze_cv_and_predict_and_show_result(top, sName, gender.get(),age.get(),file_entry.get()))
    submitBtn.place(x=250, y=300, width=200)

    top.mainloop()


def analyze_cv_and_predict_and_show_result(top, name_entry, gender_entry, age_entry, file_path):
    gender = gender_entry
    age = age_entry
    if not file_path:
        print("Please select a CV file.")
        return

    personality_values = analyze_cv_and_predict(gender, age, file_path)
    if personality_values is None:
        print("Failed to analyze the CV.")
        return

    prediction_result(top, name_entry, personality_values)


def analyze_cv_and_predict(gender, age, file_path):
    try:
        # Extract scores from the CV using the provided extraction logic
        openness, neuroticism, conscientiousness, agreeableness, extraversion = extract_scores_from_cv(file_path)

        return [gender, age, openness, neuroticism, conscientiousness, agreeableness, extraversion]
    except Exception as e:
        print("Error:", e)
        return None


def extract_scores_from_cv(cv_path):
    # Read the CV file using textract
    cv_text = textract.process(cv_path).decode("utf-8")

    # Initialize variables to store scores
    scores = {
        'openness': 4,
        'neuroticism': 4,
        'conscientiousness': 4,
        'agreeableness': 4,
        'extraversion': 4
    }

    # Define keywords for each personality trait
    keywords = {
        'openness': ['openness', 'inventive', 'curious', 'variety', 'imaginative', 'creative', 'adventurous', 'innovative', 'unconventional', 'broad-minded'],
        'neuroticism': ['neuroticism', 'sensitive', 'nervous', 'emotional', 'anxious', 'moody', 'temperamental', 'fragile', 'vulnerable', 'tense', 'worried'],
        'conscientiousness': ['conscientiousness', 'organized', 'disciplined', 'diligent', 'dependable', 'methodical', 'efficient', 'precise', 'punctual', 'systematic'],
        'agreeableness': ['agreeableness', 'friendly', 'compassionate', 'kind', 'helpful', 'sympathetic', 'tolerant', 'courteous', 'empathetic', 'considerate', 'nurturing'],
        'extraversion': ['extraversion', 'outgoing', 'energetic', 'sociable', 'enthusiastic', 'assertive', 'vibrant', 'gregarious', 'lively', 'daring', 'bold']
    }

    # Extract scores for each personality trait
    for trait, trait_keywords in keywords.items():
        for keyword in trait_keywords:
            if keyword in cv_text.lower():
                scores[trait] = min(scores[trait]+1,7)  # Assigning a score of 1 if any keyword for the trait is found

    # Convert the scores dictionary to a list representing personality values
    personality_values = [scores[trait] for trait in ['openness', 'neuroticism', 'conscientiousness', 'agreeableness', 'extraversion']]

    # Print the extracted personality values for debugging
    print("Extracted Personality Values:", personality_values)

    return personality_values


def prediction_result(top, name, personality_values):
    top.withdraw()
    applicant_data = {"NAME OF USER": name.get()}
    age = personality_values[1]

    print("\n******************** ENTERED DATA *********************\n")
    print(applicant_data, personality_values)

    personality = model.testing(personality_values)
    print("\n**************** PERSONALITY PREDICTED ****************\n")
    print(personality)

    result = Tk()
    result.geometry('700x500')
    result.configure(background='ivory2')
    result.title("Predicted Personality")

    Label(result, text="Result", fg='OrangeRed3', bg='ivory2', font=('Bookman Old Style', 30, font.BOLD), pady=10,
          anchor=CENTER).pack(fill=BOTH)

    Label(result, text=str('{} : {}'.format("Name:", name.get())).title(), fg='black', bg='ivory2',
          font=("Britannic Bold", 15)).pack(fill=BOTH)
    Label(result, text=str('{} : {}'.format("Age:", age)), fg='black', bg='ivory2',
          font=("Britannic Bold", 15)).pack(fill=BOTH)
    Label(result, text = str("predicted personality: "+personality).title(), fg='black', bg='ivory2',
          font=("Britannic Bold",15)).pack(fill=BOTH)
    
    Label(result, text="-------------------------------------------------------------------------------", fg='black',
          bg='ivory2', font=("Britannic Bold", 15)).pack(fill=BOTH)
    quitBtn = Button(result, text="Exit", bg='OrangeRed3', fg='white', font=('Bookman Old Style', 8),
                     padx=5, command=lambda: result.destroy()).pack()

    terms_mean = """
    OPENNESS TO EXPERIENCE – (inventive/curious vs. consistent/cautious).
    Appreciation for art, emotion, adventure, unusual ideas, curiosity, and variety of experience.

    CONSCIENTIOUSNESS – (efficient/organized vs. easy-going/careless).
    A tendency to show self-discipline, act dutifully, and aim for achievement;
    planned rather than spontaneous behavior.

    EXTRAVERSION – (outgoing/energetic vs. solitary/reserved).
    Energy, positive emotions, urgency, and the tendency to seek stimulation
    in the company of others.

    AGREEABLENESS – (friendly/compassionate vs. cold/unkind).
    A tendency to be compassionate and cooperative rather than suspicious
    and antagonistic towards others.

    NEUROTICISM – (sensitive/nervous vs. secure/confident).
    A tendency to experience unpleasant emotions easily, such as anger,
    anxiety, depression, or vulnerability.
    """

    Label(result, text=terms_mean, fg='SteelBlue4', bg='ivory2', font=('Lucida Sans Typewriter', 9, font.BOLD),
          justify=CENTER).pack(fill=BOTH)
    result.mainloop()


def select_file(file_entry):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("DOCX Files", "*.docx")])
    if file_path:
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)


if __name__ == "__main__":
    model = TrainModel()
    model.training()
    root = Tk()
    root.geometry('700x500')
    root.configure(background='chartreuse4')
    root.title("Personality Prediction System")
    title = font.Font(family='Lucida Handwriting', size=40, weight='bold')
    homeBtnFont = font.Font(size=12, weight='bold')
    Label(root, text="Personality\nPrediction\nSystem", bg='chartreuse4', fg='white', font=title, pady=50).pack()
    b2 = Button(root, padx=4, pady=4, width=30, text="Predict Personality", bg='black', fg='white', bd=1,
                font=homeBtnFont, command=predict_person).place(relx=0.5, rely=0.7, anchor=CENTER)
    root.mainloop()