import customtkinter
import sqlite3
import bcrypt
from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

open_eye_img = customtkinter.CTkImage(light_image=Image.open("open_eye_light.png"), dark_image=Image.open("open_eye_dark.png"), size=(26, 20))
closed_eye_img = customtkinter.CTkImage(light_image=Image.open("closed_eye_light.png"),dark_image=Image.open("closed_eye_dark.png"), size=(26,26))
close_btn_img = customtkinter.CTkImage(light_image=Image.open("close_btn_light.png"), dark_image=Image.open("close_btn_dark.png"), size=(20,20))

activeFrameLst = []

activeUser = None #Contains the User() object if a user is signed in (None if not). A GLOBAL DECLARATION MUST BE USED TO EDIT THE VARIABLE (NOT READ IT) 

class NewUserCourseSelection(customtkinter.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.place(relwidth=1, relheight=1)

        activeFrameLst.append(self)
        
        if(activeUser != None):
            self.userRecommendedCourses = self.generateClasses(activeUser.grade)
        else:
            loadFrame(UserLogin, container)


        self.userChosenCourses = []

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter a course:", justify='center', font=generateFont("Roboto", 25))
        self.entry.place(relwidth=0.4, relheight=0.1, relx=0.05, rely=0.1)

        self.submit_course_button = customtkinter.CTkButton(self, text="Register Course", command=lambda:self.chooseClass())
        self.submit_course_button.place(relwidth=0.2, relheight=0.05, relx=0.5, rely=0.125)

        self.confirm_courses_button = customtkinter.CTkButton(self, text="Confirm All Courses", command=lambda:self.initUserCoursesDB())
        self.confirm_courses_button.place(relwidth=0.2, relheight=0.05, relx=0.75, rely=0.125)
        self.scrollableFrame = customtkinter.CTkScrollableFrame(self)
        self.scrollableFrame.place(relwidth = 0.9, relheight=0.65, relx=0.05, rely=0.25)

        self.pickClasses()

    def initUserCoursesDB(self):
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        tableName = activeUser.username + "_grades"
        finalUserChosenCourses = []
        for course in self.userChosenCourses:
            course = course.replace(" ", "_")
            course = course.replace(":", "")
            course = course.replace("-", "_")
            course = course.lower()
            finalUserChosenCourses.append(course)

        columns = ', '.join(finalUserChosenCourses)
        createTableQuery = f" CREATE TABLE IF NOT EXISTS {tableName} ({columns})"
        cur.execute(createTableQuery)
        conn.commit()
        conn.close()
    def chooseClass(self):
        if(not self.entry.get().isspace() and len(self.entry.get()) > 0):
            self.userChosenCourses.append(self.entry.get())
            self.entry.delete(0, 'end')

    
    def pickClasses(self):
        self.searchingCourses = []
        self.courseLabels = []
        for course in self.userRecommendedCourses:
            label = customtkinter.CTkLabel(self.scrollableFrame, text=course)
            label.pack()
            self.courseLabels.append(label)
        self.update_label()  # Initial GUI update
        
    def update_label(self):
        for label in self.courseLabels:
            label.bind("<Button-1>", lambda event:self.label_clicked(event))
            if(label.cget("text").lower().count(self.entry.get().lower()) <= 0 and len(self.entry.get()) >0 ):
                label.pack_forget()
                self.courseLabels.remove(label)
            

        for course in self.userRecommendedCourses:
            if(course.count(self.entry.get()) > 0 and course not in [label.cget("text") for label in self.courseLabels]):
                label = customtkinter.CTkLabel(self.scrollableFrame, text=course)
                label.pack()
                self.courseLabels.append(label)  
        
        self.after(100, self.update_label)  # Schedule the next update


    def label_clicked(self, event):
        clicked_label = event.widget
        self.entry.delete(0, 'end')
        self.entry.insert(0, clicked_label.cget("text"))
   
    def generateClasses(self, grade):
        if(grade <= 5):
            raw_recommendedClasses = ["Language Arts", "Mathematics", "Science", "Social Studies", "Physical Education", "Art"]
            recommendedClasses = [i + " " + str(grade) for i in raw_recommendedClasses]
            
        elif(grade <= 8):
            raw_recommendedClasses = ["Health", "World Cultures", "Science", "Physical Education", "Spanish", "French", "Latin", "Mathematics", "Language Arts", "Business Computer Science", "Art", "Family Consumer Science", "Technology Education", "College and Career Readiness", "Algebra 1", "Geometry", "American History", "American Music"]
            recommendedClasses = [i + " " + str(grade) for i in raw_recommendedClasses]
            
        else:
            raw_recommendedClasses = ["Art", "Music", "Health", "French", "Spanish", "Latin", "Physical Education", "English", "Algebra 1", "Geometry", "Algebra 2", "Precalculus", "Trignometry"]
            nonAPRecommendedClasses = [i + " " + str(grade) for i in raw_recommendedClasses]
            apClasses = ["AP Research", "AP Seminar", "AP Art History", "AP Music Theory", "AP English Language and Composition", "AP English Literature and Composition", "AP Comparative Government and Politics", "AP European History", "AP Human Geography", "AP Macroeconomics", "AP Microeconomics", "AP Psychology", "AP United States Government and Politics", "AP United States History", "AP World History: Modern", "AP Calculus AB", "AP Calculus BC", "AP Computer Science A", "AP Computer Science Principles", "AP Precalculus", "AP Statistics", "AP Biology", "AP Chemistry", "AP Environmental Science", "AP Physics 1: Algebra-Based", "AP Physics 2: Algebra-Based", "AP Physics C Electricity and Magnetism", "AP Physics C: Mechanics", "AP Chinese Language and Culture", "AP French Language and Culture", "AP French Language and Culture", "AP German Language and Culture", "AP Italian Language and Culture", "AP Japanese Language and Culture", "AP Latin", "AP Spanish Language and Culture", "AP Spanish Literature and Culture"]
            nonAPRecommendedClasses.extend(apClasses)
            recommendedClasses = nonAPRecommendedClasses 
            
        return recommendedClasses
            
            
class User():
    def __init__(self, first_name:str, last_name:str, username:str, grade:int, password:str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.grade = grade
        self.password = password
    def returnAllAttrs(self):
        return [self.first_name, self.last_name, self.username, self.grade, self.password]


class UserRegistration(customtkinter.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)
        self.container = container
        activeFrameLst.append(self)
        
        # Sign Up UI
        self.close_button=customtkinter.CTkButton(self, image = close_btn_img, fg_color="transparent", text=None, command=lambda:[forgetAllFrames()])
        self.close_button.place(relwidth=0.1, relheight=0.1, relx=0.9, rely=0.02)
        
        self.first_name = customtkinter.CTkEntry(self, placeholder_text="First Name", font=generateFont('Roboto', 20), justify='center')
        self.first_name.setvar("name0", "First Name")
        self.first_name.place(relwidth=0.25, relheight=0.1, relx=0.163, rely=0.1)

        self.last_name = customtkinter.CTkEntry(self, placeholder_text="Last Name",font=generateFont('Roboto', 20), justify='center')
        self.last_name.setvar("name1", "Last Name")        
        self.last_name.place(relwidth=0.25, relheight=0.1, relx=0.576, rely=0.1)

        self.username = customtkinter.CTkEntry(self, placeholder_text="Username",font=generateFont('Roboto', 20), justify='center')
        self.username.setvar("name2", "Username")           
        self.username.place(relwidth=0.25, relheight=0.1, relx=0.163, rely=0.3)
        
        self.grade = customtkinter.CTkEntry(self, placeholder_text="Grade",font=generateFont('Roboto', 20), justify='center')
        self.grade.setvar("name3", "Grade")
        self.grade.place(relwidth=0.25, relheight=0.1, relx=0.576, rely=0.3)
        
        self.password = customtkinter.CTkEntry(self, placeholder_text="Password", show="*",font=generateFont('Roboto', 20), justify='center')
        self.password.setvar("name4", "Password")        
        self.password.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.5)
        
        self.view_password_button = customtkinter.CTkButton(self, image = open_eye_img, fg_color="transparent", text=None, command=lambda:[togglePasswordVisiblity(self.password, self.view_password_button)])
        self.view_password_button.place(relwidth=0.1, relheight=0.1, relx=0.8, rely=0.5)

        self.sign_up_button = customtkinter.CTkButton(master=self, border_width=2, text="Sign Up", text_color=("gray10", "#DCE4EE"), command=lambda:self.sign_up(),font=generateFont('Roboto', 20))
        self.sign_up_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.8)
        
        self.form_options = [self.first_name, self.last_name, self.username, self.grade, self.password]

    def sign_up(self):
        global activeUser
        #Opens and sets up Database for entry of user data
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        
        #Initializes Error Msg txt if needed
        self.errorMsg = customtkinter.CTkLabel(self, text='', text_color='red')
        self.errorMsg.place(relwidth=1, relheight=0.1, rely=0.6)
        
        #Checks if any forms are empty and returns appropriate error msg
        empty_form_fields = []
        isEmptyForms = False
        for idx, option in enumerate(self.form_options):
            
            if(option.get() == ''):
                isEmptyForms = True
                print("ERROR_emptyFormEntry")
                var = "name" + str(idx)
                print(option, option.getvar(var))
                empty_form_fields.append(option.getvar(var))

        if(isEmptyForms):
            self.errorMsg.configure(text=f"The following fields are empty: {[i for i in empty_form_fields]}")
            for option in self.form_options:
                    option.delete(0, 'end')
    
            self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
            return
        
        #Converts password to bytes and hashes it
        password = self.password.get().encode('utf-8')
        if(len(password) >= 72):
            print("ERROR_passwordTooLong")
            self.errorMsg.configure(text='Password Exceeds 72 Characters')
            for option in self.form_options:
                option.delete(0, 'end')
   
            self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
            return
        else:
            hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
            
        #Checks if username is already in database
        res = cur.execute("SELECT username FROM users")
        usernames = res.fetchall()
        self.errorMsg = customtkinter.CTkLabel(self, text='', text_color='red')
        self.errorMsg.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.6)
        for username in usernames:
            if(username[0] == self.username.get()):
                print("ERROR_usernameTaken")
                self.errorMsg.configure(text='Username Taken')
                for option in self.form_options:
                    option.delete(0, 'end')
   
                self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
                return 
            
        #Checks if self.grade is an int, if it is, saves values for entry into users.db
        try:
            form_entries = [self.first_name.get(), self.last_name.get(), self.username.get(), int(self.grade.get()), hashedpw]
            
        except ValueError:
            print("ERROR_gradeNotInt")
            self.errorMsg.configure(text='Grade Must Be a Number')
            for option in self.form_options:
                option.delete(0, 'end')
            self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
            return
        if(int(self.grade.get()) > 12):
            print("ERROR_gradeExceed12")
            self.errorMsg.configure(text='Grade Exceeds 12')
            for option in self.form_options:
                option.delete(0, 'end') 
            self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
            return
        
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", form_entries)
        conn.commit()
        conn.close()

        activeUser = User(*form_entries)
        loadFrame(NewUserCourseSelection, self.container)

class UserLogin(customtkinter.CTkFrame):
    def __init__(self, container):
        
        super().__init__(container)
        self.container = container

        self.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)

        activeFrameLst.append(self)

        #Login UI        
        self.close_button=customtkinter.CTkButton(self, image = close_btn_img, fg_color="transparent", text=None, command=lambda:[forgetAllFrames()])
        self.close_button.place(relwidth=0.1, relheight=0.1, relx=0.9, rely=0.02)

        self.inputted_username = customtkinter.CTkEntry(self, placeholder_text="Username", font=generateFont('Roboto', 20), justify='center')
        self.inputted_username.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.1)
        
        self.inputted_password = customtkinter.CTkEntry(self, placeholder_text="Password", show="*", font=generateFont('Roboto', 20), justify='center')
        self.inputted_password.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.3)

        self.view_password_button = customtkinter.CTkButton(self, image = open_eye_img, fg_color="transparent", text=None, command=lambda:[togglePasswordVisiblity(self.inputted_password, self.view_password_button)])
        self.view_password_button.place(relwidth=0.1, relheight=0.1, relx=0.8, rely=0.3)

        self.log_in_button = customtkinter.CTkButton(self, border_width=2, text="Log In", font=generateFont('Roboto', 20), text_color=("gray10", "#DCE4EE"), command=lambda:self.log_in())
        self.log_in_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.6)

        self.form_options = [self.inputted_username, self.inputted_password]

    def log_in(self):
        global activeUser
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        
        res = cur.execute("SELECT password FROM users WHERE username=?",(self.inputted_username.get(),))
        
        raw_password = res.fetchone()
        # conn.close()

        
        self.errorMsg = customtkinter.CTkLabel(self, text='', text_color='red')
        self.errorMsg.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.4)

        if(raw_password != None):
            hashedpw = raw_password[0]
        else:
            print("ERROR_usernameNotFound")
            self.errorMsg.configure(text='Username Not Found')
            for option in self.form_options:
                option.delete(0, 'end')
            
            self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
            return
        if(not bcrypt.checkpw(self.inputted_password.get().encode('utf-8'), hashedpw)):
            print("ERROR_invalidPassword")
            self.errorMsg.configure(text='Invalid Password')
            for option in self.form_options:
                option.delete(0, 'end')
            self.errorMsg.after(5000, lambda:self.errorMsg.configure(text=''))
            return
        else:
            self.log_in_confirmation_txt = customtkinter.CTkLabel(self, text = "Log In Successful!", font=generateFont('Roboto', 20))
            self.log_in_confirmation_txt.place(relheight=1, relwidth=1)
            self.close_button.lift()
            res = cur.execute("SELECT  first_name, last_name, username, grade, password FROM USERS where username=?", (self.inputted_username.get(),))
            # print(res)
            userDetails = res.fetchall()
            print(userDetails)
            print(*userDetails[0])
            activeUser = User(*userDetails[0])
            conn.close()

class Main(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("Not Schoology - Main")
        self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
        self.init_db()

        #Home UI
        self.titleUI = customtkinter.CTkLabel(self, text="Welcome to Not Schoology", font=generateFont('Roboto', 64))
        self.titleUI.place(relx=0, rely=0.1, relwidth=1)

        self.sign_up_button = customtkinter.CTkButton(self, text='Sign Up', font=generateFont('Roboto', 20), command=lambda:[loadFrame(UserRegistration, self)])
        self.sign_up_button.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.05)

        self.log_in_button = customtkinter.CTkButton(self, text='Log In', font=generateFont('Roboto', 20), command=lambda:[loadFrame(UserLogin, self)])
        self.log_in_button.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.05)

    #Intializes the users.db database to create the users table if it doesn't already exist.
    def init_db(self):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        cur.execute(""" CREATE TABLE IF NOT EXISTS users(
                first_name text, 
                last_name text,
                username text,
                grade integer,
                password text
            ) """)
        conn.commit()
        conn.close()

#Returns a CTKFont object using the given fontName and fontSize
def generateFont(fontName:str, fontSize:int):
    return customtkinter.CTkFont(family = fontName,size = fontSize)

#Toggles the visibilities of the given entry from showing raw text to showing **** and toggles the image displaying for the toggle button
def togglePasswordVisiblity(entry:customtkinter.CTkEntry, btn:customtkinter.CTkButton):
    if entry._entry.cget('show') == '':
        entry.configure(show='*')
        btn.configure(image=closed_eye_img)
    else:
        entry.configure(show='')
        btn.configure(image=open_eye_img)


#Forgets all active frames and removes them from activeFrameLst
def forgetAllFrames():
    for frame in activeFrameLst:
        frame.place_forget()
        activeFrameLst.remove(frame)

#Forgets all current frames and loads the given frame in the given container
def loadFrame(frame, container):
        forgetAllFrames()
        frame(container)

#Launches Application
if __name__ == "__main__":
    app = Main()
    app.mainloop()