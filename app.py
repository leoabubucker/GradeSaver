import customtkinter #App built using customtkinter GUI
import sqlite3 #User info stored using sqlite3 database
import bcrypt #Passwords hashed using bcrypt
from PIL import Image #Icons generated using Image from PIL
import math #Course frames equally distributed using math

#Customtkinter initializations
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Icon Definitions
open_eye_img = customtkinter.CTkImage(light_image=Image.open("Icons/open_eye_light.png"), dark_image=Image.open("Icons/open_eye_dark.png"), size=(26, 20))
closed_eye_img = customtkinter.CTkImage(light_image=Image.open("Icons/closed_eye_light.png"),dark_image=Image.open("Icons/closed_eye_dark.png"), size=(26,26))
close_btn_img = customtkinter.CTkImage(light_image=Image.open("Icons/close_btn_light.png"), dark_image=Image.open("Icons/close_btn_dark.png"), size=(20,20))
left_arrow_img = customtkinter.CTkImage(dark_image=Image.open("Icons/left_arrow.png"), light_image=None, size=(60, 80))
right_arrow_img = customtkinter.CTkImage(dark_image=Image.open("Icons/right_arrow.png"), light_image=None, size=(60, 80))

#Contains all customtkinter frames that are actively displayed
activeFrameLst = []

#Contains the User() object if a user is signed in (None if not). A GLOBAL DECLARATION MUST BE USED TO EDIT THE VARIABLE (NOT READ IT) 
activeUser = None 

class UserCourseDashboard(customtkinter.CTkFrame):
    """ 
    
    class UserCourseDashboard() - customTkinter Frame that serves as the dashboard to display a user's course

        def __init__() - Adds the Frame to the activeFrameLst, checks if the user is logged in, and configures the frame and login UI.
        Calls displayUserCourses() to show user courses.  

        def pullUserCoursesDB() - Pulls the user's course based on their id and converts the data into a readable form.
        RETURN lst of user courses

        def displayUserCourses() - Handles the logistics of sizing, filling, and placing the user course icons in the dashboard. Calls
        pullUserCoursesDB() to access the user's courses.

        def changeCoursePage() - Handles the switching of course pages and the appropriate placing/hiding of next/prev page buttons.
        
    """
    def __init__(self, container):
        super().__init__(container)
        self.place(relwidth=1, relheight=1)
        self.container = container
        activeFrameLst.append(self)
        
        #Checks if user is logged in, redirects to login frame if not
        if(activeUser == None):
            loadFrame(UserLogin, container)

        #Course Dashboard UI
        self.titleLabel = customtkinter.CTkLabel(container, text="Course Dashboard", font=generateFont('Roboto', 40, weight='bold'))
        self.titleLabel.place(relheight=0.1, relwidth=1)
        
        self.courseDashboardFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.courseDashboardFrame.place(relx=0.05, rely=0.1, relheight=0.9, relwidth=0.9)
        
        #Pulls the user's courses from main.db and displays them
        self.displayUserCourses()

    def pullUserCoursesDB(self):
        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        res = cur.execute("SELECT name FROM courses WHERE student_id=?", (activeUser.id,)) #Selects the user's course based on their id
        userCourseList = [i[0].replace("_", " ").title() for i in res.fetchall()] #Makes results readable 
        conn.close()
        return userCourseList

    def displayUserCourses(self):
        #Calculate num of courses to display
        userCourses = self.pullUserCoursesDB()
        numUserCourses = len(userCourses)

        # Initializiation of variables to place course frames correctly
        frameHeight = self.container.winfo_height()
        frameWidth = self.container.winfo_width()
        courseFrameHeight = 0.25 * frameHeight
        courseFrameWidth = (0.7 * frameWidth) / 4
        courseFrameLst = []
        courseTextLst = []
        #relativeX and relativeY position of first course frame 
        relx = 0.1
        rely = 0.1

        numCoursePages = math.ceil(numUserCourses/6) #calc # course pages to create (each page can hold up to 6 course frames)

        self.pagesLst = [] #Contains all the created pages
        self.activePage = None #The currently displayed page

        #Creates the pages (customtkinter frames) based on numCoursePages
        for page in range(1, numCoursePages+1):
            page = customtkinter.CTkFrame(master=self.container)
            self.pagesLst.append(page)

        self.pagesLst[0].place(relwidth=1, relheight=0.9, rely=0.1) #places the first course page
        self.activePage = self.pagesLst[0] #updates activePage to be the first page

        #Creates next/prev buttons based on the app's appearance mode if >1 pages
        if(numCoursePages > 1):
            if(customtkinter.get_appearance_mode() == "Dark"):
                self.nextPageBtn = customtkinter.CTkButton(self.container, image=right_arrow_img, fg_color="gray17", hover=False, text=None, command=lambda:self.changeCoursePage("next"))
                self.previousPageBtn = customtkinter.CTkButton(self.container, image=left_arrow_img, fg_color="gray17", hover=False, text=None, command=lambda:self.changeCoursePage("prev"))
            else:
                self.nextPageBtn = customtkinter.CTkButton(self.container, image=right_arrow_img, fg_color="gray86", hover=False, text=None, command=lambda:self.changeCoursePage("next"))
                self.previousPageBtn = customtkinter.CTkButton(self.container, image=left_arrow_img, fg_color="gray86", hover=False, text=None, command=lambda:self.changeCoursePage("prev"))
            
            self.nextPageBtn.place(relx=0.9, rely=0.5) 

        #Places all course frames w/ proper placement and attrs
        for iter, course in enumerate(userCourses):
            courseNum = iter + 1
            iter = UserCourseFrame(container=self.pagesLst[math.ceil(courseNum/6)-1], frameHeight=courseFrameHeight, frameWidth=courseFrameWidth, courseName=course, relx=relx, rely=rely, border_color="blue", border_width=1)
            courseFrameLst.append(iter)
            relx += (courseFrameWidth/frameWidth + 0.1) #spreads frames horizontally
            
            if(courseNum % 6 == 3):
                #resets relx and moves rely down to start 2nd row on same page
                relx = 0.1
                rely += (courseFrameHeight/frameHeight + 0.15)
            
            if((courseNum/6).is_integer()):
                #reset relx and rely to start new page
                relx = 0.1
                rely = 0.1

        #Creates and links a customtkinter label object to a courseFrame, accessing the frame's courseName attr as the text attr
        for iter, frame in enumerate(courseFrameLst):
            iter = customtkinter.CTkLabel(frame, text=frame.courseName, font=generateFont("Roboto", 18, weight='bold'))
            courseTextLst.append(iter)

        #Places the course frames and associated text. Frame is configured with the attrs from the frame class. 
        for index, frame in enumerate(courseFrameLst):
            frame.configure(height=frame.frameHeight, width=frame.frameWidth, border_color=frame.border_color, border_width=frame.border_width)
            frame.place(relx=frame.relx, rely=frame.rely)
            courseTextLst[index].place(relx=0.5, rely=0.5, anchor="center")
            
    def changeCoursePage(self, changeDirection:str):                
        currentPageIdx = None
        newPageIdx = None

        #Sets currentPageIdx with the idx of self.active page
        for idx, page in enumerate(self.pagesLst):
            if(self.activePage == page):
                currentPageIdx = idx

        #finds the page that is one after/before (since changeDirection is next/prev) the current page and updates the app so that page displays. 
        for idx, page in enumerate(self.pagesLst):
            
            if(((currentPageIdx + 1) == idx) and changeDirection == "next"):
                newPageIdx = idx
                self.activePage.place_forget()
                page.place(relwidth=1, relheight=0.9, rely=0.1)
                self.activePage = page
            elif(((currentPageIdx - 1) == idx) and changeDirection == "prev"):
                newPageIdx = idx
                self.activePage.place_forget()
                page.place(relwidth=1, relheight=0.9, rely=0.1)
                self.activePage = page

        #Places the previousPageBtn if not first page is placed
        for page in [page for idx, page in enumerate(self.pagesLst) if idx > 0]:
            if(self.activePage == page):
                self.previousPageBtn.place(relx=0, rely=0.5)
        
        #Places the nextPageBtn if not last page is placed
        for page in [page for idx, page in enumerate(self.pagesLst) if idx < len(self.pagesLst)-1]:
            if(self.activePage == page):
                self.nextPageBtn.place(relx=0.9, rely=0.5)

        #Hides previousPageBtn if the first page is placed
        if(newPageIdx == 0):
            self.previousPageBtn.place_forget()
            
        #Hides nextPageBtn if the last page is placed or if newPageIdx == None (Error Catching)
        if((newPageIdx == (len(self.pagesLst)-1)) or newPageIdx == None):
            self.nextPageBtn.place_forget()   

class NewUserCourseSelection(customtkinter.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.place(relwidth=1, relheight=1)

        activeFrameLst.append(self)
        self.container = container
        if(activeUser != None):
            self.userRecommendedCourses = self.generateClasses(activeUser.grade)
        else:
            loadFrame(UserLogin, container)


        self.userChosenCourses = []

        self.courseEntry = customtkinter.CTkEntry(self, placeholder_text="Enter a course:", justify='center', font=generateFont("Roboto", 25))
        self.courseEntry.place(relwidth=0.4, relheight=0.1, relx=0.05, rely=0.1)

        self.submit_course_button = customtkinter.CTkButton(self, text="Register Course", command=lambda:self.chooseClass())
        self.submit_course_button.place(relwidth=0.2, relheight=0.05, relx=0.5, rely=0.125)

        self.confirm_courses_button = customtkinter.CTkButton(self, text="Confirm All Courses", command=lambda:self.initUserCoursesDB())
        self.confirm_courses_button.place(relwidth=0.2, relheight=0.05, relx=0.75, rely=0.125)
        self.scrollableFrame = customtkinter.CTkScrollableFrame(self)
        self.scrollableFrame.place(relwidth = 0.9, relheight=0.65, relx=0.05, rely=0.25)

        self.pickClasses()

    def initUserCoursesDB(self):
        conn = sqlite3.connect("main.db")
        cur =  conn.cursor()

        finalUserChosenCourses = []
        for course in self.userChosenCourses:
            course = course.replace(" ", "_")
            course = course.replace(":", "")
            course = course.replace("-", "_")
            course = course.lower()
            finalUserChosenCourses.append(course)
        
        for course in finalUserChosenCourses:
            cur.execute("""
            INSERT INTO courses (name, student_id) VALUES (?, ?)
            """,(course, activeUser.id) 
            )
        conn.commit()
        conn.close()
        loadFrame(UserCourseDashboard, self.container)
    def chooseClass(self):
        if(not self.courseEntry.get().isspace() and len(self.courseEntry.get()) > 0):
            self.userChosenCourses.append(self.courseEntry.get())
            self.courseEntry.delete(0, 'end')

    
    def pickClasses(self):
        self.searchingCourses = []
        self.courseLabels = []
        self.courseEntryFocused = False
        for course in self.userRecommendedCourses:
            label = customtkinter.CTkLabel(self.scrollableFrame, text=course)
            label.pack()
            self.courseLabels.append(label)
            # label.winfo_

        # self.courseEntry.bind("<FocusIn>", lambda event:toggleCourseEntryFocus(event))
        # self.courseEntry.bind("<FocusOut>", lambda event:toggleCourseEntryFocus(event))
        
        # self.courseEntry.bind("<Any-KeyPress>", lambda event:self.update_label(event))
        self.update_label()  # Initial GUI update
        

        # def toggleCourseEntryFocus(event):
        #     print("toggleCourseEntryFocus() pretoggle:", self.courseEntryFocused)
        #     self.courseEntryFocused = not self.courseEntryFocused
        #     print("toggleCourseEntryFocus() posttoggle:", self.courseEntryFocused)
    def update_label(self):
        # print("self.update_label")
        for label in self.courseLabels:
            label.bind("<Button-1>", lambda event:self.label_clicked(event))
            if(label.cget("text").lower().count(self.courseEntry.get().lower()) <= 0 and len(self.courseEntry.get()) >0 ):
                label.pack_forget()
                self.courseLabels.remove(label)
            

        for course in self.userRecommendedCourses:
            if(course.count(self.courseEntry.get()) > 0 and course not in [label.cget("text") for label in self.courseLabels]):
                label = customtkinter.CTkLabel(self.scrollableFrame, text=course)
                label.pack()
                self.courseLabels.append(label)  
        
        self.after(100, self.update_label)  # Schedule the next update


    def label_clicked(self, event):
        clicked_label = event.widget
        self.courseEntry.delete(0, 'end')
        self.courseEntry.insert(0, clicked_label.cget("text"))
   
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
                     
class UserRegistration(customtkinter.CTkFrame):
    """ 
    
    class UserRegistration() - customTkinter Frame that serves as the registration window to the app

        def __init__() - Adds the Frame to the activeFrameLst and configures the frame and login UI.  

        def login() - Handles registering a new user by inserting the inputted user data into main.db, creating a new User instance,
        and loading the Course Selection dashboard. Displays an error message if process fails.

    """
    def __init__(self, container):
        super().__init__(container)
        self.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)
        self.container = container
        activeFrameLst.append(self)
        
        # Sign Up UI - .setvar() is being used to correlate the entry response with the name of input. This is used in def login()
        self.close_button = customtkinter.CTkButton(self, image = close_btn_img, fg_color="transparent", text=None, command=lambda:[forgetAllFrames()])
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
        conn = sqlite3.connect('main.db')
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
        res = cur.execute("SELECT username FROM students")
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
            
        #Checks if self.grade is an int, if it is, saves values for entry into main.db
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
        
        #Inserts new user data into database and closes it
        cur.execute("INSERT INTO students (first_name, last_name, username, grade, password) VALUES (?, ?, ?, ?, ?)", form_entries)
        conn.commit()
        conn.close()

        #Populates activeUser with a new instance of the User class and loads the Course Selection frame
        activeUser = User(*form_entries)
        loadFrame(NewUserCourseSelection, self.container)

class UserLogin(customtkinter.CTkFrame):

    """ 

    class UserLogin() - customTkinter Frame that serves as the login window to the app

        def __init__() - Adds the Frame to the activeFrameLst and configures the frame and login UI

        def login() - Handles logging in the user by checking the inputted credentials with the stored credentials in the database.
        Displays an error message if process fails, populates the activeUser variable and loads the user's course dashboard on success.

    """
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

        self.log_in_button = customtkinter.CTkButton(self, border_width=2, text="Log In", font=generateFont('Roboto', 20), text_color=("gray10", "#DCE4EE"), command=lambda:self.login())
        self.log_in_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.6)

        self.form_options = [self.inputted_username, self.inputted_password]

    def login(self):
        global activeUser

        #Opens database and retrieves stores hashed password based on the inputted username
        conn = sqlite3.connect('main.db')
        cur = conn.cursor()
        res = cur.execute("SELECT password FROM students WHERE username=?",(self.inputted_username.get(),))
        
        # raw_password will be None if the inputted username is not in the database
        raw_password = res.fetchone()
        
        # Error Catching w/ User Submitted Data

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
            #Retrieves Matching User's Data
            res = cur.execute("SELECT  first_name, last_name, username, grade, password FROM students WHERE username=?", (self.inputted_username.get(),))
            userDetails = res.fetchall()
            #Creates a User instance with fetched data
            activeUser = User(*userDetails[0])
            #Closes database connection and changes UI popup to confirm successful login
            conn.close()
            self.log_in_confirmation_txt = customtkinter.CTkLabel(self, text = "Log In Successful! Welcome, " + activeUser.username + ".", font=generateFont('Roboto', 20))
            self.log_in_confirmation_txt.place(relheight=1, relwidth=1)
            self.close_button.lift()
            #Changes close_button action to loading the dashboard frame
            self.close_button.configure(command=lambda:loadFrame(UserCourseDashboard, self.container)) 

class Main(customtkinter.CTk):
    """  
    
    class Main() - customTkinter Master Window serves as home page that opens upon program start

        def __init__() - Configures the Master Window as well as the UI for the home menu
    
        def initDb() - Ensures the main.db database and "students", "courses", and "assignments" tables have been created

    """

    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("GradeSaver - Main")
        self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
        self.initDb()

        #Home UI
        self.titleUI = customtkinter.CTkLabel(self, text="GradeSaver vDEV", font=generateFont('Roboto', 64))
        self.titleUI.place(relx=0, rely=0.1, relwidth=1)

        self.sign_up_button = customtkinter.CTkButton(self, text='Sign Up', font=generateFont('Roboto', 20), command=lambda:[loadFrame(UserRegistration, self)])
        self.sign_up_button.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.05)

        self.log_in_button = customtkinter.CTkButton(self, text='Log In', font=generateFont('Roboto', 20), command=lambda:[loadFrame(UserLogin, self)])
        self.log_in_button.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.05)

    def initDb(self):
        # Connect to the database if not exists
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()

        # Create the students table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                grade INTEGER,
                password TEXT NOT NULL
            )
        ''')

        # Create the courses table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
 
        # Create the assignments table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                student_id INTEGER,
                grade INTEGER,
                FOREIGN KEY (course_id) REFERENCES courses (id),
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

""" 
Helper Functions and Classes:

    def generateFont() - Returns a CTKFont object using the given fontName and fontSize

    def togglePasswordVisibility() - Toggles the visibilities of the given entry from showing raw text to showing **** and toggles 
    the image displaying for the toggle button

    def forgetAllFrames() - Forgets all active frames and removes them from activeFrameLst

    def loadFrame() - Forgets all current frames and loads the given frame in the given container
    
    class User() - the activeUser variable will either equal None or be an instance of User(). Serves to access the attributes of the 
    current user without opening main.db

    class UserCourseFrame() - A structure for a course frame in the UserCourseDashboard. Used to generate individual frames per user's
    course

 """

def generateFont(fontName:str, fontSize:int, weight:str = 'normal', slant:str = 'roman', underline:bool = False, overstrike:bool = False):
    return customtkinter.CTkFont(family = fontName, size = fontSize, weight=weight, slant=slant, underline=underline, overstrike=overstrike)

def togglePasswordVisiblity(entry:customtkinter.CTkEntry, btn:customtkinter.CTkButton):
    if entry._entry.cget('show') == '':
        entry.configure(show='*')
        btn.configure(image=closed_eye_img)
    else:
        entry.configure(show='')
        btn.configure(image=open_eye_img)

def forgetAllFrames():
    for frame in activeFrameLst:
        frame.place_forget()
        activeFrameLst.remove(frame)

def loadFrame(frame, container):
        forgetAllFrames()
        frame(container)

class User():
    def __init__(self, first_name:str, last_name:str, username:str, grade:int, password:str):
        conn = sqlite3.connect("main.db")
        cur = conn.cursor() 
        res = cur.execute("SELECT id FROM students WHERE username=?",(username,))
        self.id = res.fetchone()[0]
        conn.close()

        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.grade = grade
        self.password = password

    def returnAllAttrs(self):
        return {"Id" : self.id, "First Name" : self.first_name, "Last Name" : self.last_name, "Username" : self.username, "Grade" : self.grade, "Hashed Password" : self.password}

class UserCourseFrame(customtkinter.CTkFrame):
    def __init__(self, container, frameHeight, frameWidth, courseName, relx, rely, border_color, border_width):
        super().__init__(container)

        self.container = container
        self.frameHeight = frameHeight
        self.frameWidth = frameWidth
        self.courseName = courseName
        self.relx = relx
        self.rely = rely
        self.border_color = border_color
        self.border_width = border_width

#Launches Application
if __name__ == "__main__":
    app = Main()
    app.mainloop()