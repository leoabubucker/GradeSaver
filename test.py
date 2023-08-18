# import sqlite3

# # print(type(b"hi"))
# # print(type("hi"))

# # password = "hi"

# # print(type(password.encode("utf-8")))

# # int("1")
# # int("hello")

# conn = sqlite3.connect('users.db')
# cur = conn.cursor()
# #Checks if username is already in database
# res = cur.execute("SELECT last_name FROM users")
# usernames = res.fetchall()
# print(usernames)

# for username in usernames:
#     print(str(username)[2:-3])
#     if(str(username)[2:-3] == "bob5802"):
#         print("ERROR3")

#     print(username[0])
#     if(username[0] == "bob5802"):
#         print("ERROR4")
# from tkinter import *

# root = Tk()

# # create an Entry widget with a "show" option set to "*"
# entry = Entry(root, show="*")
# entry.pack()

# # get the current value of the "show" option using cget()
# show_value = entry.cget('show')

# print("The current value of the 'show' attribute is:", show_value)

# root.mainloop()
# import customtkinter as tk

# root = tk.CTk()

# # create a customtkinter Entry widget with a "show" option set to "*"
# entry = tk.CTkEntry(root, show="*")
# entry.pack()

# # get the current value of the "show" option using configure()
# # show_value = entry.configure('show')[-1]
# # show_value = entry.show
# show_value = entry.__getattribute__('show')

# print("The current value of the 'show' attribute is:", show_value)

# root.mainloop()

# import time
# from time import sleep

# sleep()
# self.form_options = [self.first_name, self.last_name, self.username, self.grade, self.password]
# for option in self.form_options:
#             if(option.get() == ''):
#                 print("ERROR_emptyFormEntry")
#                 optionStr = str(option)
#                 optionStr = optionStr.removeprefix('self.')
#                 # if(optionStr.find('_') != -1):
#                 optionStr.replace('_', ' ')
#                 optionStr = optionStr.title()


# numsLst = [23, 55, 212, 84, 234, 3]
# target1 = 26

# target2 = 267

# target3 = 107

# target4 = 296

# def Solution(nums, target):
#     for num in range(len(nums)):
#         print("----------------------------------\n")
#         rm_num = nums.pop(len(nums) - 1)
#         print(rm_num)

#         for num1 in nums:
#             if(rm_num + num1 == target):
#                 print(1, rm_num, num1)
#                 return f"{rm_num} + {num1} = {target}"
#             else:
#                 print(0)

# print(Solution(numsLst, target1))
# print(Solution(numsLst, target2))
# print(Solution(numsLst, target3))
# print(Solution(numsLst, target4))
#     solution = [i for i in nums if i + num == target]

# print(solution)

# import customtkinter
# import tkinter
# root = customtkinter.CTk()

# label = customtkinter.CTkLabel(root, text="Start Typing...")

# label.pack(pady=20)

# entry = customtkinter.CTkEntry(root)
# entry.pack()
# # lst = ["Language Arts", "Mathematics", "Science", "Social Studies", "Physical Education", "Art"]
# raw_recommendedClasses = ["Art", "Music", "Health", "French", "Spanish", "Latin", "Physical Education", "English", "Algebra 1", "Geometry", "Algebra 2", "Precalculus", "Trignometry"]
# apClasses = ["AP Research", "AP Seminar", "AP Art History", "AP Music Theory", "AP English Language and Composition", "AP English Literature and Composition", "AP Comparative Government and Politics", "AP European History", "AP Human Geography", "AP Macroeconomics", "AP Microeconomics", "AP Psychology", "AP United States Government and Politics", "AP United States History", "AP World History: Modern", "AP Calculus AB", "AP Calculus BC", "AP Computer Science A", "AP Computer Science Principles", "AP Precalculus", "AP Statistics", "AP Biology", "AP Chemistry", "AP Environmental Science", "AP Physics 1: Algebra-Based", "AP Physics 2: Algebra-Based", "AP Physics C Electricity and Magnetism", "AP Physics C: Mechanics", "AP Chinese Language and Culture", "AP French Language and Culture", "AP French Language and Culture", "AP German Language and Culture", "AP Italian Language and Culture", "AP Japanese Language and Culture", "AP Latin", "AP Spanish Language and Culture", "AP Spanish Literature and Culture"]
# raw_recommendedClasses.extend(apClasses)
# # list = customtkinter.CTkComboBox(root, values=raw_recommendedClasses)
# # lst2 = customtkinter.CTkOptionMenu(root, values=raw_recommendedClasses)
# # list.place(relwidth=0.8, relx=0.1, rely=0.5)
# # lst2.pack()


# def getText():
#     entry = customtkinter.CTkEntry(root)
#     entry.pack()
#     root.mainloop()
#     searching=True
#     inBar = []
#     print(1)
#     while searching:
#         for course in raw_recommendedClasses:
#             if(course.startswith("AP")):
#                 if(course not in inBar):
#                     inBar.append(course)
        

#         # print(raw_recommendedClasses)
#         print(inBar)
#         if(entry.get().find("done") != -1):
#             searching=False



# getText()

# import math

# print(math.ceil(7.2))

num = 1.1
print(num.is_integer())