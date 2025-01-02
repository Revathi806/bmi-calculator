import datetime
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QPushButton,QWidget,QVBoxLayout,QStackedWidget,QLineEdit,QRadioButton,QButtonGroup,QMessageBox,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QFont
import sys
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN PAGE")
        self.setGeometry(0,0,500,500)
        self.initUI()
        self.initDB()
        self.display_window = None
    
    def initDB(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            weight REAL,
                            height REAL,
                            date TEXT,
                            bmi REAL,
                            bmi_category TEXT,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                )
          ''')
        self.conn.commit()    
    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.name=QLineEdit(self)
        self.pwd=QLineEdit(self)
        
        
        self.loginPage = QWidget()
        self.loginLayout=QVBoxLayout()
        self.loginPage.setLayout(self.loginLayout)

        enter_name=QLabel("Enter Username:",self)
        enter_pwd=QLabel("Enter Password",self)
        enter_name.setFont(QFont("Arial",20))
        enter_pwd.setFont(QFont("Arial",20))

        self.name.setPlaceholderText("enter username")
        self.pwd.setPlaceholderText("ENter password")
        self.pwd.setEchoMode(QLineEdit.Password)

        login_button=QPushButton("login",self)
        login_button.setFont(QFont("Arial",20))
        login_button.setGeometry(30,100,200,300)
        login_button.clicked.connect(self.bmiCalculator)
        
        register_button = QPushButton("Register", self)
        register_button.setFont(QFont("Arial", 20))
        register_button.clicked.connect(self.showRegistrationPage)

        self.loginLayout.addWidget(enter_name)
        self.loginLayout.addWidget(self.name)
        self.loginLayout.addWidget(enter_pwd)
        self.loginLayout.addWidget(self.pwd)
        self.loginLayout.addWidget(login_button)
        self.loginLayout.addWidget(register_button)

        #for the panel
        self.loginLayout.setContentsMargins(100, 100, 100, 100)
        self.loginLayout.setSpacing(20)

        self.stacked_widget.addWidget(self.loginPage)

        # Registration Page
        self.regPage = QWidget()
        self.regLayout = QVBoxLayout()
        self.regPage.setLayout(self.regLayout)

        reg_enter_name = QLabel("Enter Username:", self)
        reg_enter_pwd = QLabel("Enter Password:", self)
        reg_enter_name.setFont(QFont("Arial", 20))
        reg_enter_pwd.setFont(QFont("Arial", 20))

        self.reg_name = QLineEdit(self)
        self.reg_pwd = QLineEdit(self)
        self.reg_name.setPlaceholderText("enter username")
        self.reg_pwd.setPlaceholderText("Enter password")
        self.reg_pwd.setEchoMode(QLineEdit.Password)

        register = QPushButton("Register", self)
        register.setFont(QFont("Arial", 20))
        register.clicked.connect(self.registerUser )

        to_login = QPushButton("Back to Login", self)
        to_login.setFont(QFont("Arial", 20))
        to_login.clicked.connect(self.showLoginPage)

        self.regLayout.addWidget(reg_enter_name)
        self.regLayout.addWidget(self.reg_name)
        self.regLayout.addWidget(reg_enter_pwd)
        self.regLayout.addWidget(self.reg_pwd)
        self.regLayout.addWidget(register)
        self.regLayout.addWidget(to_login)

       
        self.stacked_widget.addWidget(self.regPage)

        #bmi calculation page
        self.bmiCalc=QWidget()
        bmiLayout=QVBoxLayout()
        self.bmiCalc.setLayout(bmiLayout)

        weight = QLabel("Enter wieght (in kg):", self)
        weight.setFont(QFont("Arial", 24))
        height = QLabel("Enter wieght (in m or cm):", self)
        height.setFont(QFont("Arial", 24))

        self.height_group=QButtonGroup(self)
        self.height1=QRadioButton("m",self)
        self.height2=QRadioButton("cm",self)
        self.height1.setFont(QFont("Arial", 20))
        self.height2.setFont(QFont("Arial", 20))

        self.weight_input = QLineEdit(self)
        self.weight_input.setPlaceholderText("Enter weight in kg")
        self.weight_input.setFont(QFont("Arial", 18))
        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("Enter height")
        self.height_input.setFont(QFont("Arial", 18))

        calculate_button=QPushButton("submit",self)
        calculate_button.setFont(QFont("Arial",20))
        calculate_button.setGeometry(30,100,200,300)
        calculate_button.clicked.connect(self.calculator)

        data_view=QPushButton("view previous submissions",self)
        data_view.setFont(QFont("Arial",20))
        data_view.setGeometry(30,100,200,300)
        data_view.clicked.connect(self.display)


        logout = QPushButton("Logout", self)
        logout.setFont(QFont("Arial", 20))
        logout.clicked.connect(self.showLoginPage)

        trend_analysis=QPushButton("View BMI trend analysis",self)
        trend_analysis.setFont(QFont("Arial",20))
        trend_analysis.clicked.connect(self.bmiTrendAnalysis)

        bmiLayout.addWidget(logout)
        bmiLayout.addWidget(weight)
        bmiLayout.addWidget(height)
        bmiLayout.addWidget(self.weight_input)
        bmiLayout.addWidget(self.height_input)
        bmiLayout.addWidget(self.height1)
        bmiLayout.addWidget(self.height2)
        bmiLayout.addWidget(calculate_button)
        bmiLayout.addWidget(data_view)
        bmiLayout.addWidget(trend_analysis)

        self.stacked_widget.addWidget(self.bmiCalc)



    def showRegistrationPage(self):
        self.stacked_widget.setCurrentWidget(self.regPage)

    def showLoginPage(self):
        self.stacked_widget.setCurrentWidget(self.loginPage)
    
    def showBmiPage(self):
        self.stacked_widget.setCurrentWidget(self.bmiCalc)

    def bmiCalculator(self):
        n = self.name.text()
        p = self.pwd.text()
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (n, p))
        if self.cursor.fetchone():
            self.stacked_widget.setCurrentIndex(2) 
        else:
            print("Invalid username or password.")
    
    def calculator(self):
        try:
            output=QWidget()
            outputLayout=QVBoxLayout()
            output.setLayout(outputLayout)
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            
            if self.height2.isChecked(): 
                height /= 100
            bmi = weight / (height ** 2)
            self.insert_bmi(weight, height, bmi)

            output_bmi = QLabel(f"Your BMI is: {bmi:.2f}")
            output_bmi.setFont(QFont("Arial", 20))
            outputLayout.addWidget(output_bmi)
            self.visualize_bmi(bmi)
            if bmi<18.5:
                category="you are underweight"
            elif bmi>=18.5 and bmi<=24.9:
                category="you have normal weight"
            elif bmi>=25 and bmi<=29.9:
                category='you are overweight'
            elif bmi>=30:
                category='you are obese'
            category_type=QLabel(category)
            category_type.setFont(QFont("Arial",16))
            outputLayout.addWidget(category_type)
            
            go_back_button = QPushButton("Go Back", self)
            go_back_button.setFont(QFont("Arial", 20))
            go_back_button.clicked.connect(self.showBmiPage)  
            outputLayout.addWidget(go_back_button)

            self.stacked_widget.addWidget(output)
            self.stacked_widget.setCurrentWidget(output)
        except ValueError:
            error_msg = QLabel("Error: Please enter valid numeric values for weight and height.")
            error_msg.setFont(QFont("Arial", 16))
            error_msg.setStyleSheet("color: red;")
            self.stacked_widget.addWidget(error_msg)
            self.stacked_widget.setCurrentWidget(error_msg)
        
    def visualize_bmi(self,bmi):
        categories=['Underweight','Normal weight','Overweight','Obese']
        values=[18.5,24.9,29.9,40]

        plt.figure(figsize=(8,4))
        plt.bar(categories,values,color=['blue','green','orange','red'])
        plt.axhline(y=bmi,color='black',linestyle='--',label=f'Your BMI:{bmi:.2f}')
        plt.title('BMI Categories')
        plt.xlabel('Categories')
        plt.ylabel('BMI')
        plt.legend()
        plt.ylim(0,40)
        plt.grid(axis='y')
        plt.show()    
    
    def registerUser (self):
        username = self.reg_name.text()
        password = self.reg_pwd.text()
        if username and password:
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                print("User  registered successfully!")
                self.showLoginPage()  # Navigate back to login page after registration
            except sqlite3.IntegrityError:
                print("Username already exists. Please choose a different username.")
        else:
            print("Please enter both username and password.")

    def insert_bmi(self, weight, height, bmi):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        username = self.name.text() 
        self.cursor.execute('SELECT id FROM users WHERE username=?', (username,))
        user_id = self.cursor.fetchone()
        
        if user_id:
            user_id = user_id[0]  
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi <= 24.9:
                category = "Normal"
            elif 25 <= bmi <= 29.9:
                category = "Overweight"
            else:
                category = "Obese"
            
            self.cursor.execute('''
                INSERT INTO user_data (user_id, weight, height, date, bmi, bmi_category)
                VALUES (?, ?, ?, ?, ?, ?);
            ''', (user_id, weight, height, current_date, bmi, category))
            self.conn.commit()
        else:
            print("User  not found. Cannot insert BMI data.")

    def display(self):
        username=self.name.text()
        self.cursor.execute('SELECT weight,height,date,bmi,bmi_category FROM user_data WHERE user_id=(SELECT id FROM users where username=?)',(username,))
        record=self.cursor.fetchall()

        if record:
                output=QWidget()
                outputLayout=QVBoxLayout()
                output.setLayout(outputLayout)

                table = QTableWidget()
                table.setRowCount(len(record)) 
                table.setColumnCount(5) 
                table.setHorizontalHeaderLabels(["Weight (kg)", "Height (m)", "Date", "BMI", "Category"])  # Set column headers
                for row_index, record in enumerate(record):
                    weight, height, date, bmi, category = record
                    table.setItem(row_index, 0, QTableWidgetItem(str(weight)))
                    table.setItem(row_index, 1, QTableWidgetItem(str(height)))
                    table.setItem(row_index, 2, QTableWidgetItem(date))
                    table.setItem(row_index, 3, QTableWidgetItem(f"{bmi:.2f}"))
                    table.setItem(row_index, 4, QTableWidgetItem(category))

                outputLayout.addWidget(table)  # Add the table to the layout
                back = QPushButton("Go Back", self)
                back.setFont(QFont("Arial", 20))
                back.clicked.connect(self.showBmiPage)
                outputLayout.addWidget(back)
                self.stacked_widget.addWidget(output)  # Add the output widget to the stacked widget
                self.stacked_widget.setCurrentWidget(output)
        else:
            QMessageBox.information(self,"NO DATA TO BE SHOWN")

    def bmiTrendAnalysis(self):
        username=self.name.text()
        self.cursor.execute('SELECT date,bmi FROM user_data WHERE user_id=(SELECT id FROM users where username=?)',(username,))
        record=self.cursor.fetchall()
        
        if record:
            output=QWidget()
            outputLayout=QVBoxLayout()
            output.setLayout(outputLayout)
            for row in record:
                dates=[datetime.datetime.strptime(row[0],"%Y-%m-%d")]
                bmis=[row[1]]
            
            avg_bmi=sum(bmis)/len(bmis)
            max_bmi=max(bmis)
            min_bmi=min(bmis)

            stats_label = QLabel(f"Average BMI: {avg_bmi:.2f}\nMax BMI: {max_bmi:.2f}\nMin BMI: {min_bmi:.2f}")
            stats_label.setFont(QFont("Arial", 16))
            outputLayout.addWidget(stats_label)

            figure,ax=plt.subplots(figsize=(8,4))
            ax.plot(dates,bmis,marker='o',label='BMI')
            ax.axhline(y=18.5,color="blue",linestyle="--",label="Underweight (18.5)")
            ax.axhline(y=24.9,color="green",linestyle="--",label=" Normal Weight (18.5-24.9)")
            ax.axhline(y=29.9,color="orange",linestyle="--",label="Overweight (25-29.9)")
            ax.axhline(y=30,color="red",linestyle="--",label="Obese (30+)")

            ax.set_title("BMI Trend Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("BMI")
            ax.legend()
            ax.grid()

            canvas = FigureCanvas(figure)
            outputLayout.addWidget(canvas)

            back = QPushButton("Go Back", self)
            back.setFont(QFont("Arial", 20))
            back.clicked.connect(self.showBmiPage)
            outputLayout.addWidget(back)

            self.stacked_widget.addWidget(output)
            self.stacked_widget.setCurrentWidget(output)

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__=="__main__":
    main()