import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import pandas as pd
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
import seaborn as sns

# Database Setup
def setup_database():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE,
                 password TEXT)''')
    conn.commit()
    conn.close()

setup_database()

# Main Application Class
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("User Sign-In and Sign-Up")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f0f0")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_login_ui()

    def create_login_ui(self):
        self.clear_frame()

        tk.Label(self.root, text="Login", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.root, text="Username", bg="#f0f0f0").pack(pady=5)
        tk.Entry(self.root, textvariable=self.username).pack(pady=5)

        tk.Label(self.root, text="Password", bg="#f0f0f0").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password, show="*").pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login, bg="#4caf50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.create_signup_ui, bg="#2196f3", fg="white").pack(pady=10)

    def create_signup_ui(self):
        self.clear_frame()

        tk.Label(self.root, text="Sign Up", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.root, text="Username", bg="#f0f0f0").pack(pady=5)
        tk.Entry(self.root, textvariable=self.username).pack(pady=5)

        tk.Label(self.root, text="Password", bg="#f0f0f0").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password, show="*").pack(pady=5)

        tk.Button(self.root, text="Sign Up", command=self.signup, bg="#4caf50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.create_login_ui, bg="#f44336", fg="white").pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, {}!".format(username))
            self.create_home_ui()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def signup(self):
        username = self.username.get()
        password = self.password.get()
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Sign up successful")
            self.create_login_ui()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    def create_home_ui(self):
        self.clear_frame()

        tk.Label(self.root, text="Home", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)
        tk.Button(self.root, text="Upload CSV File", command=self.upload_file, bg="#4caf50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_login_ui, bg="#f44336", fg="white").pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        dataframe = pd.read_csv(file_path)
        messagebox.showinfo("File Upload", "File uploaded successfully")

        # Preprocessing
        print("Input Data:")
        print(dataframe.head(20))

        print("\nChecking Missing Values:")
        print(dataframe.isnull().sum())

        label_encoder = preprocessing.LabelEncoder()
        dataframe = dataframe.apply(lambda col: label_encoder.fit_transform(col) if col.dtypes == 'object' else col)

        print("\nData After Encoding:")
        print(dataframe.head(20))

        # Feature Selection
        x = dataframe.drop('defects', axis=1)
        y = dataframe['defects']
        x_kbest = SelectKBest(chi2, k=10).fit_transform(x, y)
        print(f"Original Features: {x.shape[1]}, Reduced Features: {x_kbest.shape[1]}")

        # Data Splitting
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
        print(f"Training Data: {x_train.shape[0]}, Test Data: {x_test.shape[0]}")

        # ANN Model
        classifier = Sequential()
        classifier.add(Dense(activation="relu", input_dim=x.shape[1], units=8, kernel_initializer="uniform"))
        classifier.add(Dense(activation="relu", units=14, kernel_initializer="uniform"))
        classifier.add(Dense(activation="sigmoid", units=1, kernel_initializer="uniform"))
        classifier.compile(optimizer='adam', loss='mae', metrics=['mae', 'accuracy'])
        history = classifier.fit(x_train, y_train, batch_size=100, epochs=10, verbose=0)

        acc_ann = max(history.history['accuracy']) * 100
        print(f"ANN Accuracy: {acc_ann:.2f}%")

        # Visualization
        plt.plot(history.history['accuracy'])
        plt.title('ANN Training Accuracy')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()