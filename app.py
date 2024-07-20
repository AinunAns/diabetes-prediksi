from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy user data for login
users = {
    "admin": "password"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('diagnosis'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    if request.method == 'POST':
        gender = request.form['gender']
        age = int(request.form['age'])
        hypertension = request.form['hypertension']
        heart_disease = request.form['heart_disease']
        smoking_history = request.form['smoking_history']
        bmi = float(request.form['bmi'])
        glucose_level = float(request.form['glucose_level'])
        blood_sugar_level = float(request.form['blood_sugar_level'])

        # Check for diabetes
        if blood_sugar_level > 180:
            result = "Diabetes"
        else:
            result = "No Diabetes"

        # Save to CSV
        with open('diabetes_prediction_dataset.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([gender, age, hypertension, heart_disease, smoking_history, bmi, glucose_level, blood_sugar_level, result])

        return redirect(url_for('history'))
    
    return render_template('diagnosis.html')

@app.route('/history', methods=['GET', 'POST'])
def history():
    data = []
    try:
        with open('diabetes_prediction_dataset.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
    except FileNotFoundError:
        pass

    if request.method == 'POST':
        if 'delete' in request.form:
            index = int(request.form['delete'])
            data.pop(index)
            with open('diabetes_prediction_dataset.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        elif 'edit' in request.form:
            index = int(request.form['edit'])
            return redirect(url_for('edit', index=index))

    return render_template('history.html', data=data)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    data = []
    try:
        with open('diabetes_prediction_dataset.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
    except FileNotFoundError:
        pass

    if request.method == 'POST':
        data[index] = [
            request.form['gender'],
            request.form['age'],
            request.form['hypertension'],
            request.form['heart_disease'],
            request.form['smoking_history'],
            request.form['bmi'],
            request.form['glucose_level'],
            request.form['blood_sugar_level'],
            data[index][8]  # keeping the result the same
        ]
        with open('diabetes_prediction_dataset.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        return redirect(url_for('history'))

    return render_template('edit.html', data=data[index])

if __name__ == '__main__':
    app.run(debug=True)
