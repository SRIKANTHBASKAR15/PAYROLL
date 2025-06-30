from tkinter import*
from tkinter import messagebox,ttk,filedialog
import tkinter as tk
import pymysql
import time
import os
import pandas as pd
import sqlite3
from datetime import datetime
import pymysql.cursors
import tkinter as tk
from tkcalendar import DateEntry
import calendar
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from xlsxwriter.utility import xl_rowcol_to_cell
from openpyxl.styles import NamedStyle
        
class EmployeeSystem:

    def __init__(self, root):
        # Add a login window
        self.login_window = tk.Toplevel(root)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        self.login_window.resizable(False, False)

        tk.Label(self.login_window, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.login_window, show="*")
        self.username_entry.pack(pady=5)

        tk.Label(self.login_window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.login_window, text="Login", command=self.check_login).pack(pady=10)
        self.users = {
            "admin": "vmsulo@3",
            "guest": "guest123",
        }


    def check_login(self):
        # Check if the entered username and password are correct
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Replace the following condition with your actual authentication logic
        if username == "admin" and password == "vmsulo@3":
            # Destroy the login window and continue with the main application
            self.login_window.destroy()
            self.initialize_main_application()
        elif username == "guest" and password == "guest123":
            # Limit access for the guest user
            self.login_window.destroy()
            self.initialize_main_application(guest_mode=True)
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password")


    def initialize_main_application(self, guest_mode=False):
        self.script_directory = os.path.dirname(os.path.realpath(__file__))
        self.root=root
        self.root.title("Employee Payroll Management System | Developed By SRIKANTH BASKAR")
        self.root.geometry("1365x700+0+0")
        self.root.config(bg="White")
        title=Label(self.root,text="VMS Payroll Management System",font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).place(x=0,y=0,relwidth=1)
        btn_emp = Button(self.root,text="All Employee's",command=self.employee_frame,font=("times new roman", 13), bg="lightgray", fg="black").place(x=1100, y=15, height=30, width=120)
        btn_exc = Button(self.root,text="Excel",command=self.salary_frame,font=("times new roman", 13), bg="green", fg="white")
        btn_exc.place(x=1230, y=15, height=30, width=120)
        btn_des = Button(self.root,text="Designation",command=self.desgination_frame,font=("times new roman", 13), bg="lightgray", fg="black")
        btn_des.place(x=970, y=15, height=30, width=120)
        btn_bank = Button(self.root,text="Bank details",command=self.bankdetails_frame,font=("times new roman", 13), bg="lightgray", fg="black").place(x=840, y=15, height=30, width=120)
        btn_attendance = Button(self.root,text="Attendance",command=self.attendancedetails_frame,font=("times new roman", 13), bg="lightgray", fg="black")
        btn_attendance.place(x=710, y=15, height=30, width=120)
        btn_auto = Button(self.root,text="Auto",command=self.update_attendance_and_calculate,font=("times new roman", 13), bg="red", fg="white")
        btn_auto.place(x=620, y=15, height=30, width=80)
        #=======Frame1==============
        #=======Variables===========
        self.var_emp_code=StringVar()
        self.var_designation=StringVar()
        self.var_name=StringVar()
        self.var_age=StringVar()
        self.var_gender=StringVar()
        self.var_email=StringVar()
        self.var_hired_location=StringVar()
        self.var_doj=StringVar()
        self.var_dob=StringVar()
        self.var_experience=StringVar()
        self.var_proof_id=StringVar()
        self.var_contactno=StringVar()
        self.var_status=StringVar()
        self.var_intime = StringVar()
        self.var_outime = StringVar()
        self.var_lunchout = StringVar()
        self.var_lunchin = StringVar()




        Frame1=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Frame1.place(x=10,y=70,width=750,height=620)
        title2=Label(Frame1,text="Empolyee Details",font=("times new roman",20),bg="lightgray",fg="black",anchor="w",padx=10).place(x=0,y=0,relwidth=1)
        btn_adddetails=Button(Frame1,text="Load File",command=self.add_details_from_excel,font=("times new roman",14)).place(x=650,y=5,height=25)

        lbl_code=Label(Frame1,text="Empolyee Code",font=("times new roman",20),bg="white",fg="black").place(x=10,y=70)
        self.txt_code=Entry(Frame1,font=("times new roman",15),textvariable=self.var_emp_code,bg="lightyellow",fg="black")
        self.txt_code.place(x=220,y=74,width=200)
        btn_search=Button(Frame1,text="Search",command=self.search,font=("times new roman",20),bg="gold",fg="black").place(x=430,y=70,height=30)
        self.btn_atten=Button(Frame1,text="Attendance",command=self.search2,font=("times new roman",20),bg="darkorange",fg="white")
        self.btn_atten.place(x=540,y=70,height=30)

        #====ROW1=============
        lbl_designation=Label(Frame1,text="Designation",font=("times new roman",20),bg="white",fg="black").place(x=10,y=120)
        txt_designation=Entry(Frame1,font=("times new roman",15),textvariable=self.var_designation,bg="lightyellow",fg="black").place(x=170,y=125,width=200)
        btn_designation=Button(Frame1,font=("times new roman",20),command=self.search1,bg="lightgray",fg="black").place(x=346,y=125,height=26)
        lbl_doj=Label(Frame1,text="D.O.J",font=("times new roman",20),bg="white",fg="black").place(x=390,y=120)
        txt_doj=DateEntry(root, font=("times new roman", 15), date_pattern='yyyy-mm-dd',textvariable=self.var_doj, bg="lightyellow", fg="black").place(x=535,y=200,width=200)
        #====ROW2=============
        lbl_name=Label(Frame1,text="Name",font=("times new roman",20),bg="white",fg="black").place(x=10,y=170)
        txt_name=Entry(Frame1,font=("times new roman",15),textvariable=self.var_name,bg="lightyellow",fg="black").place(x=170,y=175,width=200)
        lbl_dob=Label(Frame1,text="D.O.B",font=("times new roman",20),bg="white",fg="black").place(x=390,y=170)
        txt_dob=DateEntry(root, font=("times new roman", 15), date_pattern='yyyy-mm-dd',textvariable=self.var_dob, bg="lightyellow", fg="black").place(x=535,y=250,width=200)
        #====ROW3=============
        lbl_age=Label(Frame1, text="Age", font=("times new roman", 20), bg="white", fg="black").place(x=10, y=220)
        txt_age=Entry(Frame1, font=("times new roman", 15),textvariable=self.var_age, bg="lightyellow", fg="black").place(x=170, y=225, width=200)
        btn_calculate_age=Button(Frame1, command=self.calculate_age, font=("times new roman", 15), bg="gray", fg="black")
        btn_calculate_age.place(x=345, y=225, height=25, width=25)
        lbl_experience=Label(Frame1, text="Experience", font=("times new roman", 20), bg="white", fg="black").place(x=390, y=220)
        txt_experience=Entry(Frame1, font=("times new roman", 15), textvariable=self.var_experience, bg="lightyellow", fg="black").place(x=520, y=225, width=200)
        btn_calculate_exp=Button(Frame1, command=self.calculate_experience, font=("times new roman", 15), bg="gray", fg="black").place(x=700, y=225, height=25, width=25)
        #====ROW4=============
        lbl_gender=Label(Frame1,text="Gender",font=("times new roman",20),bg="white",fg="black").place(x=10,y=270)
        genders = ["Male", "Female", "Other"]
        self.var_gender = StringVar()
        txt_gender = ttk.Combobox(Frame1, font=("times new roman", 15), textvariable=self.var_gender, values=genders)
        txt_gender.place(x=170, y=270, width=200)
        txt_gender.set("Select Gender")
        lbl_proofid=Label(Frame1,text="Proof ID",font=("times new roman",20),bg="white",fg="black").place(x=390,y=270)
        txt_proofid=Entry(Frame1,font=("times new roman",15),textvariable=self.var_proof_id,bg="lightyellow",fg="black").place(x=520,y=275,width=200)
        #====ROW4=============
        lbl_email=Label(Frame1,text="Email",font=("times new roman",20),bg="white",fg="black").place(x=10,y=320)
        txt_email=Entry(Frame1,font=("times new roman",15),textvariable=self.var_email,bg="lightyellow",fg="black").place(x=170,y=325,width=200)
        lbl_contactno=Label(Frame1,text="Contact No",font=("times new roman",20),bg="white",fg="black").place(x=390,y=320)
        txt_contactno=Entry(Frame1,font=("times new roman",15),textvariable=self.var_contactno,bg="lightyellow",fg="black").place(x=520,y=325,width=200)
        #====ROW5=============
        lbl_hired=Label(Frame1,text="Hired Location",font=("times new roman",18),bg="white",fg="black").place(x=10,y=372)
        txt_hired=Entry(Frame1,font=("times new roman",15),textvariable=self.var_hired_location,bg="lightyellow",fg="black").place(x=170,y=375,width=200)
        lbl_status=Label(Frame1,text="Status",font=("times new roman",20),bg="white",fg="black").place(x=390,y=370)
        status = ["Primary", "Secondary", "Part Time"]
        txt_status = ttk.Combobox(Frame1, font=("times new roman", 15), textvariable=self.var_status, values=status)
        txt_status.place(x=520, y=370, width=200)
        txt_status.set("Select Status")
        #====ROW6=============
        # In Time Label and Combobox
        lbl_intime = Label(Frame1, text="In Time", font=("times new roman", 20), bg="white", fg="black")
        lbl_intime.place(x=10, y=420)
        self.hour_intime = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(24)], state="readonly")
        self.hour_intime.place(x=170, y=420)
        self.hour_intime.set("00")
        self.minute_intime = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(60)], state="readonly")
        self.minute_intime.place(x=220, y=420)
        self.minute_intime.set("00")

        # Out Time Label and Combobox
        lbl_outime = Label(Frame1, text="Out Time", font=("times new roman", 20), bg="white", fg="black")
        lbl_outime.place(x=390, y=420)
        self.hour_outime = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(24)], state="readonly")
        self.hour_outime.place(x=520, y=420)
        self.hour_outime.set("00")
        self.minute_outime = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(60)], state="readonly")
        self.minute_outime.place(x=570, y=420)
        self.minute_outime.set("00")
        #====ROW7=============
        # Lunch Out Label and Combobox
        lbl_lunchout = Label(Frame1, text="Lunch Out", font=("times new roman", 20), bg="white", fg="black")
        lbl_lunchout.place(x=10, y=465)
        self.hour_lunchout = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(24)], state="readonly")
        self.hour_lunchout.place(x=170, y=465)
        self.hour_lunchout.set("00")
        self.minute_lunchout = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(60)], state="readonly")
        self.minute_lunchout.place(x=220, y=465)
        self.minute_lunchout.set("00")
        # Lunch In Label and Combobox
        lbl_lunchin = Label(Frame1, text="Lunch In", font=("times new roman", 20), bg="white", fg="black")
        lbl_lunchin.place(x=390, y=465)
        self.hour_lunchin = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(24)], state="readonly")
        self.hour_lunchin.place(x=520, y=465)
        self.hour_lunchin.set("00")
        self.minute_lunchin = ttk.Combobox(Frame1, width=3, font=("times new roman", 15), values=[f"{i:02}" for i in range(60)], state="readonly")
        self.minute_lunchin.place(x=570, y=465)
        self.minute_lunchin.set("00")
        #====ROW8=============
        lbl_address=Label(Frame1,text="Address",font=("times new roman",20),bg="white",fg="black").place(x=10,y=505)
        self.txt_address=Text(Frame1,font=("times new roman",15),bg="lightyellow",fg="black")
        self.txt_address.place(x=170,y=505,width=550,height=70)
        #====Row9=============
        self.btn_save=Button(Frame1,text="Save",command=self.add,font=("times new roman",20),bg="green",fg="white")
        self.btn_save.place(x=300,y=580,height=30,width=100)
        btn_clear=Button(Frame1,text="Clear",command=self.clear,font=("times new roman",20),bg="gray",fg="black").place(x=410,y=580,height=30,width=100)
        self.btn_delete=Button(Frame1,text="Delete",command=self.delete,font=("times new roman",20),bg="red",fg="white")
        self.btn_delete.place(x=520,y=580,height=30,width=100)
        self.btn_update=Button(Frame1,text="Update",command=self.update,font=("times new roman",20),bg="lightblue",fg="black")
        self.btn_update.place(x=630,y=580,height=30,width=100)   
        #=======FRAME2==============
        #=======Variables===========
        self.var_month=StringVar()
        self.var_year=StringVar()
        self.var_bsalary=StringVar()
        self.var_ftsalary=StringVar()
        self.var_totaldays=StringVar()
        self.var_absents=StringVar()
        self.var_convence=StringVar()
        self.var_da=StringVar()
        self.var_spl=StringVar()
        self.var_nh=StringVar()
        self.var_incentive=StringVar()
        self.var_ph=StringVar()
        self.var_advance=StringVar()

        Frame2=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Frame2.place(x=770,y=70,width=580,height=300)
        title3=Label(Frame2,text="Empolyee Salary Details",font=("times new roman",20),bg="lightgray",fg="black",anchor="w",padx=10).place(x=0,y=0,relwidth=1)
        lbl_ph=Label(Frame2,text="N H",font=("times new roman",20),bg="lightgray",fg="black").place(x=400,y=0)
        txt_ph=Entry(Frame2,font=("times new roman",15),textvariable=self.var_ph,bg="lightyellow",fg="black").place(x=460,y=5,width=100)


        #====ROW1=============
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        lbl_month = tk.Label(Frame2, text="Month", font=("times new roman", 20), bg="white", fg="black").place(x=10, y=60)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.var_month = tk.StringVar()
        txt_month = ttk.Combobox(Frame2, font=("times new roman", 15), textvariable=self.var_month, values=months)
        txt_month.place(x=90, y=66, width=110)
        txt_month.set(months[current_month - 1])
        self.var_year = tk.StringVar()
        lbl_month = tk.Label(Frame2, text="Month", font=("times new roman", 20), bg="white", fg="black").place(x=10, y=60)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.var_month = tk.StringVar()
        txt_month = ttk.Combobox(Frame2, font=("times new roman", 15), textvariable=self.var_month, values=months)
        txt_month.place(x=90, y=66, width=110)
        txt_month.set(months[current_month - 1])
        self.var_year = tk.StringVar()
        lbl_year = tk.Label(Frame2, text="Year", font=("times new roman", 20), bg="white", fg="black").place(x=210, y=60)
        txt_year = tk.Entry(Frame2, font=("times new roman", 15), textvariable=self.var_year, bg="lightyellow", fg="black")
        txt_year.place(x=270, y=62, width=100)
        txt_year.insert(0, current_year) 
        lbl_ftsalary = Label(Frame2, text="Salary", font=("times new roman", 20), bg="white", fg="black").place(x=380, y=60)
        txt_ftbasicsalary = Entry(Frame2, font=("times new roman", 15), textvariable=self.var_ftsalary, bg="lightyellow", fg="black").place(x=460, y=62, width=100)

        # ==== ROW2 =============
        lbl_totaldays = Label(Frame2, text="Total Days", font=("times new roman", 20), bg="white", fg="black").place(x=10, y=120)
        txt_totaldays = Entry(Frame2, font=("times new roman", 15), textvariable=self.var_totaldays, bg="lightyellow", fg="black").place(x=170, y=125, width=100)
        btn_totaldays = Button(Frame2, command=self.calculate_total_days, font=("times new roman", 15), bg="gray", fg="black")
        btn_totaldays.place(x=245, y=125, height=25, width=25)
        lbl_ftsalary=Label(Frame2,text="Salary",font=("times new roman",20),bg="white",fg="black").place(x=380,y=60)
        txt_ftbasicsalary=Entry(Frame2,font=("times new roman",15),textvariable=self.var_ftsalary,bg="lightyellow",fg="black").place(x=460,y=62,width=100)

        #====ROW2=============
        lbl_absents=Label(Frame2,text="Absents",font=("times new roman",20),bg="white",fg="black").place(x=300,y=120)
        txt_absents=Entry(Frame2,font=("times new roman",15),textvariable=self.var_absents,bg="lightyellow",fg="black").place(x=425,y=125,width=120)
        #====ROW3=============
        lbl_basic=Label(Frame2,text="Basic",font=("times new roman",20),bg="white",fg="black").place(x=10,y=150)
        txt_basic=Entry(Frame2,font=("times new roman",15),textvariable=self.var_bsalary,bg="lightyellow",fg="black").place(x=170,y=155,width=100)
        lbl_da=Label(Frame2,text="DA",font=("times new roman",20),bg="white",fg="black").place(x=300,y=150)
        txt_da=Entry(Frame2,font=("times new roman",15),textvariable=self.var_da,bg="lightyellow",fg="black").place(x=425,y=155,width=120)
        #====ROW4=============
        lbl_convence=Label(Frame2,text="Convence",font=("times new roman",20),bg="white",fg="black").place(x=10,y=180)
        txt_convence=Entry(Frame2,font=("times new roman",15),textvariable=self.var_convence,bg="lightyellow",fg="black").place(x=170,y=185,width=100)
        lbl_spl=Label(Frame2,text="Allowance",font=("times new roman",20),bg="white",fg="black").place(x=300,y=180)
        txt_spl=Entry(Frame2,font=("times new roman",15),textvariable=self.var_spl,bg="lightyellow",fg="black").place(x=425,y=185,width=120) 
        #====ROW5=============
        lbl_advance=Label(Frame2,text="Advance",font=("times new roman",20),bg="white",fg="black").place(x=10,y=210)
        txt_advance=Entry(Frame2,font=("times new roman",15),textvariable=self.var_advance,bg="lightyellow",fg="black").place(x=170,y=215,width=100)
        lbl_incentive=Label(Frame2,text="Incentive",font=("times new roman",20),bg="white",fg="black").place(x=300,y=210)
        txt_incentive=Entry(Frame2,font=("times new roman",15),textvariable=self.var_incentive,bg="lightyellow",fg="black").place(x=425,y=215,width=120) 
        #====ROW6=============
        self.btn_update=Button(Frame2,text="Update",command=self.update1,font=("times new roman",20),bg="lightblue",fg="black")
        self.btn_update.place(x=20,y=255,height=30,width=100) 
        self.btn_calculate = Button(Frame2, text="Calculate",command=self.calculate,font=("times new roman", 20), bg="orange", fg="black")
        self.btn_calculate.place(x=237, y=255, height=30, width=120)
        self.btn_save=Button(Frame2,text="Save",command=self.add2,font=("times new roman",20),bg="green",fg="white")
        self.btn_save.place(x=365,y=255,height=30,width=100)
        btn_clear=Button(Frame2,text="Clear",command=self.clear1,font=("times new roman",20),bg="gray",fg="black")
        btn_clear.place(x=470,y=255,height=30,width=100)
        self.btn_delete=Button(Frame2,text="Delete",command=self.delete2,font=("times new roman",20),bg="red",fg="white")
        self.btn_delete.place(x=130,y=255,height=30,width=100)       
        #=======FRAME3==============
        Frame3=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Frame3.place(x=770,y=380,width=580,height=310)

        #===EARN SALARY Frame==========
        #=======Variables===========
        self.var_earned_bsalary=StringVar()
        self.var_gtsalary=StringVar()
        self.var_ntsalary=StringVar()
        self.var_earned_convence=StringVar()
        self.var_earned_da=StringVar()
        self.var_earned_spl=StringVar()
        self.var_esi=StringVar()
        self.var_pf=StringVar()
        earn_Frame=Frame(Frame3,bg="white",bd=2,relief=RIDGE)
        earn_Frame.place(x=2,y=2,width=247,height=300)
        title_ear=Label(earn_Frame,text="EARNED SALARY",font=("times new roman",18),bg="lightgray",fg="black",anchor="w",padx=10).place(x=0,y=0,relwidth=1)
        #====earned salary===========
        lbl_basic=Label(earn_Frame,text="Basic",font=("times new roman",17),bg="white",fg="black").place(x=10,y=35)
        txt_basic=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_earned_bsalary,bg="lightyellow",fg="black").place(x=125,y=40,width=100)
        lbl_da=Label(earn_Frame,text="DA",font=("times new roman",17),bg="white",fg="black").place(x=10,y=65)
        txt_da=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_earned_da,bg="lightyellow",fg="black").place(x=125,y=70,width=100)
        lbl_convence=Label(earn_Frame,text="Convence",font=("times new roman",17),bg="white",fg="black").place(x=10,y=95)
        txt_convence=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_earned_convence,bg="lightyellow",fg="black").place(x=125,y=100,width=100)
        lbl_spl=Label(earn_Frame,text="Allowance",font=("times new roman",17),bg="white",fg="black").place(x=10,y=125)
        txt_spl=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_earned_spl,bg="lightyellow",fg="black").place(x=125,y=130,width=100) 
        lbl_gtsalary=Label(earn_Frame,text="Salary",font=("times new roman",17),bg="white",fg="black").place(x=10,y=155)
        txt_gtbasicsalary=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_gtsalary,bg="lightyellow",fg="black").place(x=125,y=160,width=100)

        title_dt=Label(earn_Frame,text="DEDUCTION",font=("times new roman",18),bg="lightgray",fg="black",anchor="w",padx=10).place(x=0,y=190,relwidth=1)

        lbl_pf=Label(earn_Frame,text="PF",font=("times new roman",17),bg="white",fg="black").place(x=10,y=230)
        txt_pf=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_pf,bg="lightyellow",fg="black").place(x=125,y=235,width=100) 
        lbl_esi=Label(earn_Frame,text="ESI",font=("times new roman",17),bg="white",fg="black").place(x=10,y=260)
        txt_esi=Entry(earn_Frame,font=("times new roman",15),textvariable=self.var_esi,bg="lightyellow",fg="black").place(x=125,y=265,width=100)


       
        #======Bank Frame========
        self.var_bank=StringVar()
        self.var_acctno=StringVar()
        self.var_ifscode=StringVar()
        self.var_ntsalary=StringVar()
        sal_Frame = Frame(Frame3, bg="white", bd=2, relief=RIDGE)
        sal_Frame.place(x=251, y=2, width=320, height=170)
        title_sal=Label(sal_Frame,text="Bank Details",font=("times new roman",18),bg="lightgray",fg="black",anchor="w",padx=10).place(x=0,y=0,relwidth=1)
        lbl_bank=Label(sal_Frame,text="Bank",font=("times new roman",17),bg="white",fg="black").place(x=10,y=40)
        txt_bank=Entry(sal_Frame,font=("times new roman",15),textvariable=self.var_bank,bg="lightyellow",fg="black").place(x=125,y=40,width=180)
        lbl_acctno=Label(sal_Frame,text="Accnt No",font=("times new roman",17),bg="white",fg="black").place(x=10,y=70)
        txt_acctno=Entry(sal_Frame,font=("times new roman",15),textvariable=self.var_acctno,bg="lightyellow",fg="black").place(x=125,y=70,width=180)
        lbl_ifscode=Label(sal_Frame,text="IFS Code",font=("times new roman",17),bg="white",fg="black").place(x=10,y=100)
        txt_ifscode=Entry(sal_Frame,font=("times new roman",15),textvariable=self.var_ifscode,bg="lightyellow",fg="black").place(x=125,y=100,width=180)
        lbl_ntsalary=Label(sal_Frame,text="Net Salary",font=("times new roman",15),bg="white",fg="black").place(x=10,y=130)
        txt_ntbasicsalary=Entry(sal_Frame,font=("times new roman",15),textvariable=self.var_ntsalary,bg="lightyellow",fg="black").place(x=125,y=130,width=180)

        #======Attendance Frame========
        attendance_Frame=Frame(Frame3,bg="white",bd=2,relief=RIDGE)
        attendance_Frame.place(x=251,y=172,width=320,height=130)
        title_sal=Label(attendance_Frame,text="Attendance",font=("times new roman",18),bg="lightgray",fg="black",anchor="w",padx=10).place(x=0,y=0,relwidth=1)

        button1 = tk.Button(attendance_Frame, text="Browse A File", command=lambda: self.File_dialog())
        button1.place(rely=0.70, relx=0.50)

        button2 = tk.Button(attendance_Frame, text="Load File", command=lambda: self.Load_excel_data())
        button2.place(rely=0.70, relx=0.30)

        self.label_file = ttk.Label(attendance_Frame, text="No File Selected")
        self.label_file.place(rely=0.3, relx=0)

        self.tv1 = ttk.Treeview()
        self.treescrolly = None
        self.treescrollx = None


        self.create_database_and_tables()
        self.check_connection()
        self.calculate_total_days()
        if guest_mode:
            btn_exc.config(state="disabled")
            button2.config(state="disabled")
            button1.config(state="disabled")
            btn_clear.config(state="disabled")
            self.btn_update.config(state="disabled")
            self.btn_calculate.config(state="disabled")
            self.btn_save.config(state="disabled")
            self.btn_atten.config(state="disabled")
            self.btn_delete.config(state="disabled")  # Disable the Excel button for the guest user
            btn_exc.config(state="disabled")
            btn_des.config(state="disabled")
            btn_attendance.config(state="disabled")
            btn_auto.config(state="disabled")
#=========================ALL FUNCTION START HERE======================

                    
    def calculate_total_days(self):
        selected_month = self.var_month.get()
        selected_year = int(self.var_year.get())

        # Map the month abbreviation to its numeric value
        month_number = {month: index + 1 for index, month in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}

        if selected_month in month_number:
            month = month_number[selected_month]
            total_days = calendar.monthrange(selected_year, month)[1]
            self.var_totaldays.set(total_days)
        else:
            print("Invalid month selected")

    def some_function_that_uses_dob(self):
        # You can access the selected DOB using self.var_dob.get()
        dob = self.var_dob.get()
        print("Selected DOB:", dob)
        
    def File_dialog(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                            title="Select A File",
                                            filetypes=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))

        self.label_file["text"] = filename  # Use self.label_file instead of label_file
        return None
    
    def calculate_age(self):
        dob_str = self.var_dob.get()
        if dob_str:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            self.var_age.set(age)

    def calculate_experience(self):
        doj_str = self.var_doj.get()
        if doj_str:
            doj = datetime.strptime(doj_str, "%Y-%m-%d")
            today = datetime.now()
            experience = today.year - doj.year - ((today.month, today.day) < (doj.month, doj.day))
            self.var_experience.set(experience)




    def Load_excel_data(self):
        file_path = self.label_file["text"]
        if file_path == "No File Selected":
            messagebox.showinfo("Information", "Please select a file first.")
            return None

        try:
            df = pd.read_excel(file_path)
        except ValueError:
            messagebox.showerror("Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            messagebox.showerror("Information", f"No such file as {file_path}")
            return None

        # Now, you can load the DataFrame into the SQL table
        self.load_data_to_sql(df)



    def load_data_to_sql(self, df):

        # Calculate the total number of absent days for each employee
        absent_count = df[df['Absent'] == 1].groupby(['EmployeeCode', 'EmployeeName'])['Absent'].count().reset_index()
        absent_count.columns = ['EmployeeCode', 'EmployeeName', 'Absent']

        # Create a named style to suppress the warning
        style = NamedStyle(name="custom_style")

        # Create a new workbook and add a sheet
        wb = Workbook()
        wb.add_named_style(style)

        # Write the DataFrame to the sheet using the named style
        ws = wb.active
        for row in dataframe_to_rows(absent_count, index=False, header=True):
            ws.append(row)

        try:
            # Establish a connection to your MySQL database
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='vms',
                cursorclass=pymysql.cursors.DictCursor
            )

            with connection.cursor() as cursor:
                # Create the table if it doesn't exist
                create_table_query = '''
                CREATE TABLE IF NOT EXISTS summaryatten (
                    emp_code VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(20),
                    absent TEXT
                )
                '''
                cursor.execute(create_table_query)

                delete_data_query = '''DELETE FROM summaryatten'''
                cursor.execute(delete_data_query)

                # Insert or update the data into the table
                for index, row in absent_count.iterrows():
                    # Skip rows where emp_code is 0
                    if row['EmployeeCode'] == 0:
                        continue

                    # Add 'EMP' in front of the EmployeeCode
                    emp_code = 'EMP' + str(row['EmployeeCode'])

                    insert_query = '''
                    INSERT INTO summaryatten (emp_code, name, absent)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        emp_code = VALUES(emp_code),
                        name = VALUES(name),
                        absent = VALUES(absent)
                    '''
                    cursor.execute(insert_query, (
                        emp_code,
                        str(row['EmployeeName']),
                        str(row['Absent'])
                    ))

            # Commit the changes
            connection.commit()

            messagebox.showinfo("Information", "Data loaded into SQL table successfully.")

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            # Close the connection outside the try block
            if connection:
                connection.close()






    def clear_data(self):
        self.tv1.delete(*self.tv1.get_children())

    def search(self):
        if self.var_emp_code.get()=='' or self.var_totaldays.get()=='':
            messagebox.showerror("Error","Employee ID, Total days, basic are  must be required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from employeepayroll where emp_code=%s",(self.var_emp_code.get()))
                row=cur.fetchone()
                cur1=con.cursor()
                cur1.execute("select * from bank_details where emp_code=%s",(self.var_emp_code.get()))
                row1=cur1.fetchone()
                cur2=con.cursor()
                cur2.execute("select * from salary_details where emp_code=%s",(self.var_emp_code.get()))
                row2=cur2.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Employee ID, please try with another employee ID")
                else:
                    self.var_emp_code.set(row[0])
                    self.var_designation.set(row[1])
                    self.var_name.set(row[2])
                    self.var_age.set(row[3])
                    self.var_gender.set(row[4])
                    self.var_email.set(row[5])
                    self.var_hired_location.set(row[6])
                    self.var_doj.set(row[7])
                    self.var_dob.set(row[8])
                    self.var_experience.set(row[9])
                    self.var_proof_id.set(row[10])
                    self.var_contactno.set(row[11])
                    self.var_status.set(row[12])
                    self.txt_address.delete('1.0',END)
                    self.txt_address.insert(END,row[13])
                    self.var_name.set(row1[1])
                    self.var_bank.set(row1[2])
                    self.var_acctno.set(row1[3])
                    self.var_ifscode.set(row1[4])
                    self.var_ntsalary.set(row1[5])
                    self.var_totaldays.set(row2[5]),
                    self.var_nh.set(row2[6]),
                    self.var_bsalary.set(row2[8]),
                    self.var_da.set(row2[9]),
                    self.var_spl.set(row2[10]),
                    self.var_convence.set(row2[11]),
                    self.var_earned_bsalary.set(row2[13]),
                    self.var_earned_da.set(row2[14]),
                    self.var_earned_spl.set(row2[15]),
                    self.var_earned_convence.set(row2[16]),
                    self.var_gtsalary.set(row2[17]),
                    self.var_pf.set(row2[18]),
                    self.var_esi.set(row2[19]),
                    self.var_advance.set(row2[20]),     
                    self.var_incentive.set(row2[22]),    
                    self.var_ntsalary.set(row2[23]), 

                    
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def search1(self):
        if self.var_designation.get()=='':
            messagebox.showerror("Error","Desgination name must be required")
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', db='vms')
                cur = con.cursor()
                cur.execute("select * from Designation where designation=%s", (self.var_designation.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid designation, please try with another designation")
                else:
                    self.var_designation.set(row[0])
                    self.var_bsalary.set(row[1])
                    self.var_ftsalary.set(row[5])
                    self.var_spl.set(row[4])
                    self.var_convence.set(row[3])
                    self.var_da.set(row[2])
                    self.txt_code.config(state='readonly')

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")
                self.btn_delete.config(state=NORMAL)  # Enable delete button

    def search2(self):
        if self.var_emp_code.get()=='':
            messagebox.showerror("Error","Employee ID must be required")
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', db='vms')
                cur = con.cursor()
                cur.execute("select * from summaryatten where emp_code=%s", (self.var_emp_code.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid emp_code, please try with another emp_code")
                else:
                    self.var_absents.set(row[2])
                    self.txt_code.config(state='readonly')

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")
                self.btn_delete.config(state=NORMAL)  # Enable delete button


    def clear(self):
        self.btn_save.config(state=NORMAL)
        self.txt_code.config(state=NORMAL)
        self.var_emp_code.set('')
        self.var_designation.set('')
        self.var_name.set('')
        self.var_age.set('')
        self.var_gender.set('')
        self.var_email.set('')
        self.var_hired_location.set('')
        self.var_doj.set('')
        self.var_dob.set('')
        self.var_experience.set('')
        self.var_proof_id.set('')
        self.var_contactno.set('')
        self.var_status.set('')
        self.txt_address.delete('1.0',END)
        self.var_bank.set('')
        self.var_acctno.set('')
        self.var_ifscode.set('')
        self.var_ntsalary.set('')

    def clear1(self):
        self.var_month.set('')
        self.var_year.set('')
        self.var_bsalary.set('')
        self.var_ftsalary.set('')
        self.var_totaldays.set('')
        self.var_absents.set('')
        self.var_convence.set('')
        self.var_da.set('')
        self.var_spl.set('')
        self.var_nh.set('')
        self.var_incentive.set('')
        self.var_earned_bsalary.set('')
        self.var_earned_da.set('')
        self.var_earned_convence.set('')
        self.var_earned_spl.set('')
        self.var_gtsalary.set('')
        self.var_pf.set('')
        self.var_esi.set('')
        self.var_advance.set('')


    def delete(self):
        if self.var_emp_code.get()=='':
            messagebox.showerror("Error","Employee ID must be required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from employeepayroll where emp_code=%s",(self.var_emp_code.get()))
                row=cur.fetchone()
                cur1=con.cursor()
                cur1.execute("select * from bank_details where emp_code=%s",(self.var_emp_code.get()))
                row1=cur1.fetchone()
                if row == None and row1 == None:
                    messagebox.showerror("Error","Invalid Employee ID, please try with another employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?")
                    if op==True:
                        cur.execute("delete from employeepayroll where emp_code=%s",(self.var_emp_code.get()))
                        cur1.execute("delete from bank_details where emp_code=%s",(self.var_emp_code.get()))
                        con.commit()
                        con.close()
                        messagebox.showerror("Delete","Employee Record Deleted Successfully",parent=self.root)
                        self.clear()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def delete1(self):
        if self.var_designation_1.get()=='':
            messagebox.showerror("Error","Designation must be required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from designation where designation=%s",(self.var_designation_1.get()))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Designation, please try with another Designation",parent=self.root3)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?")
                    if op==True:
                        cur.execute("delete from designation where designation=%s",(self.var_designation_1.get()))
                        con.commit()
                        con.close()
                        messagebox.showerror("Delete","Designation Record Deleted Successfully",parent=self.root3)
                        self.clear()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def delete2(self):
        if self.var_emp_code.get()=='':
            messagebox.showerror("Error","Empolyee Code must be required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from salary_details where emp_code=%s",(self.var_emp_code.get()))
                row=cur.fetchone()
                cur1=con.cursor()
                cur1.execute("select * from attendance where emp_code=%s",(self.var_emp_code.get()))
                row1=cur1.fetchone()
                if row == None and row1 == None:
                    messagebox.showerror("Error","Invalid salary_details, please try with another salary_details",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?")
                    if op==True:
                        cur.execute("delete from salary_details where emp_code=%s",(self.var_emp_code.get()))
                        cur1.execute("delete from attendance where emp_code=%s",(self.var_emp_code.get()))
                        con.commit()
                        con.close()
                        messagebox.showerror("Delete","salary_details Record Deleted Successfully",parent=self.root)
                        self.clear1()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")


    def add_details_from_excel(self):
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=(("Excel files", "*.xlsx;*.xls"), ("all files", "*.*")))
        
        if file_path:
            try:
                # Load data from Excel file using pandas
                df_employee = pd.read_excel(file_path, sheet_name='Sheet1')
                df_bank = pd.read_excel(file_path, sheet_name='Sheet2')

                # Assuming the DataFrames have columns similar to your employee details
                for index, row_employee in df_employee.iterrows():
                    # Extract data from employee DataFrame and insert into SQL tables
                    self.add_employee_to_database(row_employee)

                # Assuming the DataFrames have columns similar to your bank details
                for index, row_bank in df_bank.iterrows():
                    # Extract data from bank DataFrame and insert into SQL tables
                    self.add_bank_details_to_database(row_bank)

                messagebox.showinfo("Success", "Data loaded from Excel file and added to the database")

            except Exception as ex:
                messagebox.showerror("Error", f"Error loading data from Excel: {str(ex)}")

    def add_employee_to_database(self, data_row):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', db='vms')
            cur = con.cursor()

            # Check if employee ID already exists in employeepayroll table
            cur.execute("SELECT * FROM employeepayroll WHERE emp_code=%s", (data_row['emp_code'],))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror("Error", "Employee with this ID already exists in the record")
            else:
                # Convert all values to strings
                values = tuple(str(value) for value in [
                    data_row['emp_code'], data_row['designation'], data_row['name'], data_row['age'],
                    data_row['gender'], data_row['email'], data_row['hired_location'], data_row['doj'], data_row['dob'],
                    data_row['experience'], data_row['proof_id'], data_row['contactno'], data_row['status'],
                    data_row['address']
                ])

                # Insert into employeepayroll table
                query = "INSERT INTO employeepayroll VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query, values)

                con.commit()
                con.close()


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")


    def add_bank_details_to_database(self, data_row):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', db='vms')
            cur = con.cursor()

            # Check if employee ID already exists in bank_details table
            cur.execute("SELECT * FROM bank_details WHERE emp_code=%s", (data_row['emp_code'],))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror("Error", "Bank details for this employee ID already exist in the record")
            else:

                # Convert all values to strings
                values = tuple(str(value) for value in [
                    data_row['emp_code'], data_row['name'], data_row['bank'], data_row['acctno'],
                    data_row['ifscode'], data_row['ntsalary']
                ])

                # Insert into bank_details table
                query = "INSERT INTO bank_details VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute(query, values)

                con.commit()
                con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def calculate_working_hours(self, intime, lunchout, lunchin, outime):
        # Convert the time strings to datetime objects
        time_format = "%H:%M"
        intime_dt = datetime.strptime(intime, time_format)
        lunchout_dt = datetime.strptime(lunchout, time_format)
        lunchin_dt = datetime.strptime(lunchin, time_format)
        outime_dt = datetime.strptime(outime, time_format)

        # Calculate the time differences
        morning_work_duration = lunchout_dt - intime_dt
        afternoon_work_duration = outime_dt - lunchin_dt

        # Calculate total working hours
        total_work_duration = morning_work_duration + afternoon_work_duration

        # Return the total working hours as hours and minutes
        return total_work_duration


    def add(self):
        if self.var_emp_code.get()=='' or self.var_name.get()=='':
            messagebox.showerror("Error","Employee details are required")
        else:
            # Set the time values in the StringVar variables
            self.var_intime.set(f"{self.hour_intime.get()}:{self.minute_intime.get()}")
            self.var_outime.set(f"{self.hour_outime.get()}:{self.minute_outime.get()}")
            self.var_lunchout.set(f"{self.hour_lunchout.get()}:{self.minute_lunchout.get()}")
            self.var_lunchin.set(f"{self.hour_lunchin.get()}:{self.minute_lunchin.get()}")

            total_working_hours = self.calculate_working_hours(
            self.var_intime.get(),
            self.var_lunchout.get(),
            self.var_lunchin.get(),
            self.var_outime.get()
            )
            
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur1=con.cursor()
                cur.execute("select * from employeepayroll where emp_code=%s",(self.var_emp_code.get()))
                cur1.execute("select * from bank_details where emp_code=%s",(self.var_emp_code.get()))
                row=cur.fetchone()
                row1=cur1.fetchone()
                if row!=None:
                    messagebox.showerror("Error","this employee ID has already available in our record, try will some other employee id")
                else:
                    cur.execute("INSERT INTO employeepayroll VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s,%s,%s,%s,%s %s)",
                                (
                                    self.var_emp_code.get(),
                                    self.var_designation.get(),
                                    self.var_name.get(),
                                    self.var_age.get(),
                                    self.var_gender.get(),
                                    self.var_email.get(),
                                    self.var_hired_location.get(),
                                    self.var_doj.get(),
                                    self.var_dob.get(),
                                    self.var_experience.get(),
                                    self.var_proof_id.get(),
                                    self.var_contactno.get(),
                                    self.var_status.get(),
                                    self.var_intime.get(),
                                    self.var_outime.get(),
                                    self.var_lunchout.get(),
                                    self.var_lunchin.get(),
                                    total_working_hours,
                                    self.txt_address.get('1.0', END),
                                )
                                )
                    cur1.execute("INSERT INTO bank_details VALUES (%s, %s, %s,%s, %s, %s)",
                                (
                                    self.var_emp_code.get(),
                                    self.var_name.get(),
                                    self.var_bank.get(),
                                    self.var_acctno.get(),
                                    self.var_ifscode.get(),
                                    self.var_ntsalary.get(),
                                )
                                )                   
                    con.commit() 
                    con.close()


                    messagebox.showinfo("Success","Record Added Successfully")

                
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")

            
    def search3(self,emp_code):
        if emp_code=='':
            messagebox.showerror("Error","Employee ID are must required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from employeepayroll where emp_code=%s",(emp_code))
                row=cur.fetchone()
                cur1=con.cursor()
                cur1.execute("select * from bank_details where emp_code=%s",(emp_code))
                row1=cur1.fetchone()
                cur2=con.cursor()
                cur2.execute("select * from salary_details where emp_code=%s",(emp_code))
                row2=cur2.fetchone()
                cur3=con.cursor()
                cur3.execute("select * from attendance where emp_code=%s",(emp_code))
                row3=cur3.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Employee ID, please try with another employee ID")
                else:
                    self.var_emp_code.set(row[0])
                    self.var_designation.set(row[1])
                    self.var_name.set(row[2])
                    self.var_age.set(row[3])
                    self.var_gender.set(row[4])
                    self.var_email.set(row[5])
                    self.var_hired_location.set(row[6])
                    self.var_doj.set(row[7])
                    self.var_dob.set(row[8])
                    self.var_experience.set(row[9])
                    self.var_proof_id.set(row[10])
                    self.var_contactno.set(row[11])
                    self.var_status.set(row[12])
                    self.txt_address.delete('1.0',END)
                    self.txt_address.insert(END,row[13])
                    self.var_name.set(row1[1])
                    self.var_bank.set(row1[2])
                    self.var_acctno.set(row1[3])
                    self.var_ifscode.set(row1[4])
                    self.var_ntsalary.set(row1[5])
                    self.var_absents.set(str(int(row3[2])-int(row3[3]))),
                    self.var_bsalary.set(row2[8]),
                    self.var_da.set(row2[9]),
                    self.var_spl.set(row2[10]),
                    self.var_convence.set(row2[11]),
                    self.var_earned_bsalary.set(row2[13]),
                    self.var_earned_da.set(row2[14]),
                    self.var_earned_spl.set(row2[15]),
                    self.var_earned_convence.set(row2[16]),
                    self.var_gtsalary.set(row2[17]),
                    self.var_pf.set(row2[18]),
                    self.var_esi.set(row2[19]),     
                    self.var_incentive.set(row2[20]),    
                    self.var_ntsalary.set(row2[21]), 

                    
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")      

    def add2(self):
        if self.var_designation.get()=='' or self.var_bsalary.get()=='':
            messagebox.showerror("Error","Salary Details details are required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from salary_details where emp_code=%s",(self.var_emp_code.get()))
                row=cur.fetchone()
                cur1=con.cursor()
                cur1.execute("select * from attendance where emp_code=%s",(self.var_emp_code.get()))
                row1=cur1.fetchone()
                if row!=None and row1!=None:
                    messagebox.showerror("Error","this salary_details has already available in our record, try will some other Employee code")
                else:
                    cur.execute("INSERT INTO salary_details VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s,%s)",
                                (
                                    self.var_emp_code.get(),
                                    self.var_name.get(),
                                    self.var_designation.get(),
                                    self.var_ftsalary.get(),
                                    self.var_totaldays.get(),
                                    str(int(self.var_totaldays.get())-int(self.var_absents.get())), 
                                    self.var_nh.get(),
                                    str(int(self.var_totaldays.get())-int(self.var_absents.get())+int(self.var_nh.get())+int(self.var_ph.get())),
                                    self.var_bsalary.get(),
                                    self.var_da.get(),
                                    self.var_spl.get(),
                                    self.var_convence.get(),
                                    self.var_ftsalary.get(),
                                    self.var_earned_bsalary.get(),
                                    self.var_earned_da.get(),
                                    self.var_earned_spl.get(),
                                    self.var_earned_convence.get(),
                                    self.var_gtsalary.get(),
                                    self.var_pf.get(),
                                    self.var_esi.get(),
                                    self.var_advance.get(),
                                    str(int(self.var_pf.get()) + int(self.var_esi.get()) + int(self.var_advance.get())), 
                                    self.var_incentive.get(),    
                                    self.var_ntsalary.get(), 
                                )
                                )
                    cur.execute("INSERT INTO attendance VALUES (%s, %s, %s,%s, %s, %s)",
                                (
                                    self.var_emp_code.get(),
                                    self.var_name.get(),
                                    self.var_totaldays.get(),
                                    str(int(self.var_totaldays.get())-int(self.var_absents.get())), 
                                    self.var_nh.get(),
                                    self.var_totaldays.get(),
                                )
                                )
                    con.commit() 
                    con.close()


                    messagebox.showinfo("Success","Record Added Successfully")

                
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")  

 
    def add1(self):
        if self.var_designation_1.get()=='' or self.var_bsalary_1.get()=='':
            messagebox.showerror("Error","Employee details are required")
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='',db='vms')
                cur=con.cursor()
                cur.execute("select * from designation where designation=%s",(self.var_designation_1.get()))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","this Designation has already available in our record, try will some other Designation code")
                else:
                    cur.execute("INSERT INTO designation VALUES (%s, %s, %s,%s, %s, %s)",
                                (
                                    self.var_designation_1.get(),
                                    self.var_bsalary_1.get(),
                                    self.var_da_1.get(),
                                    self.var_convence_1.get(),
                                    self.var_spl_1.get(),
                                    self.var_ftsalary_1.get(),
                                    
                                )
                                )
                    con.commit() 
                    con.close()


                    messagebox.showinfo("Success","Record Added Successfully")

                
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}")   

    def update(self):
        if self.var_emp_code.get() == '':
            messagebox.showerror("Error", "Employee details are required")
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', db='vms')
                cur = con.cursor()
                cur.execute("SELECT * FROM employeepayroll WHERE emp_code=%s", (self.var_emp_code.get()))
                row = cur.fetchone()
                cur1 = con.cursor()
                cur1.execute("SELECT * FROM bank_details WHERE emp_code=%s", (self.var_emp_code.get()))
                row1 = cur1.fetchone()
                if row is None and row1 is None:
                    messagebox.showerror("Error", "This employee ID is invalid. Try again with a valid Employee ID", parent=self.root)
                else:
                    cur.execute("""
                        UPDATE `employeepayroll` SET `Desgination`= %s ,`name`=%s,`age`=%s,`gender`=%s,`email`=%s,`hired_location`=%s,`doj`=%s,`dob`=%s,`experience`=%s,`proof_id`=%s,`contactno`=%s,`status`=%s,`address`=%s WHERE `emp_code`=%s
                        """,
                        (
                            self.var_designation.get(),
                            self.var_name.get(),
                            self.var_age.get(),
                            self.var_gender.get(),
                            self.var_email.get(),
                            self.var_hired_location.get(),
                            self.var_doj.get(),
                            self.var_dob.get(),
                            self.var_experience.get(),
                            self.var_proof_id.get(),
                            self.var_contactno.get(),
                            self.var_status.get(),
                            self.txt_address.get('1.0', END),
                            self.var_emp_code.get()
                            
                        )
                    )
                    cur1.execute("""
                        UPDATE `bank_details` SET `name`=%s,`bank`=%s,`acctno`=%s,`ifscode`=%s,`ntsalary`=%s WHERE `emp_code`=%s
                        """,
                        (
                            self.var_name.get(),
                            self.var_bank.get(),
                            self.var_acctno.get(),
                            self.var_ifscode.get(),
                            self.var_ntsalary.get(),
                            self.var_emp_code.get()
                        )
                    )  
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Record Updated Successfully")
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def update1(self):
        if self.var_emp_code.get() == '':
            messagebox.showerror("Error", "Employee details are required")
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', db='vms')
                cur = con.cursor()
                cur.execute("SELECT * FROM salary_details WHERE emp_code=%s", (self.var_emp_code.get()))
                row = cur.fetchone()
                cur1 = con.cursor()
                cur1.execute("SELECT * FROM attendance WHERE emp_code=%s", (self.var_emp_code.get()))
                row1 = cur1.fetchone()
                if row is None and row1 is None:
                    messagebox.showerror("Error", "This employee ID is invalid. Try again with a valid Employee ID", parent=self.root)
                else:
                    cur.execute("""
                       UPDATE `salary_details` SET `name`=%s,`designation`=%s,`fixed_salary`=%s,`no_of_payable`=%s,`no_of_days_present`=%s,`nh_fh_ot_days`=%s,`total_days_present`=%s,`fbasic`=%s,`fda`=%s,`fallowance`=%s,`fconveyance`=%s,`fixed_salary_1`=%s,`ebasic`=%s,`eda`=%s,`eallowance`=%s,`econveyance`=%s,`gross_salary`=%s,`pf`=%s,`esi`=%s,`advance`=%s,`total_deduction`=%s,`other`=%s,`ntsalary`=%s WHERE `emp_code`=%s
                        """,
                        (
                            self.var_name.get(),
                            self.var_designation.get(),
                            self.var_ftsalary.get(),
                            self.var_totaldays.get(),
                            str(int(self.var_totaldays.get())-int(self.var_absents.get())), 
                            self.var_nh.get(),
                            str(int(self.var_totaldays.get())-int(self.var_absents.get())+int(self.var_nh.get())+int(self.var_ph.get())),
                            self.var_bsalary.get(),
                            self.var_da.get(),
                            self.var_spl.get(),
                            self.var_convence.get(),
                            self.var_ftsalary.get(),
                            self.var_earned_bsalary.get(),
                            self.var_earned_da.get(),
                            self.var_earned_spl.get(),
                            self.var_earned_convence.get(),
                            self.var_gtsalary.get(),
                            self.var_pf.get(),
                            self.var_esi.get(),
                            self.var_advance.get(),
                            str(int(self.var_pf.get()) + int(self.var_esi.get()) + int(self.var_advance.get())),    
                            self.var_incentive.get(),    
                            self.var_ntsalary.get(), 
                            self.var_emp_code.get(),
                            
                        )
                    )
                    cur1.execute("""
                        UPDATE `attendance` SET `name`=%s,`no_of_payable`=%s,`no_of_days_present`=%s,`nh_fh_ot_days`=%s,`total_days_present`=%s WHERE `emp_code`=%s
                        """,
                        (
                            self.var_name.get(),
                            self.var_totaldays.get(),
                            str(int(self.var_totaldays.get())-int(self.var_absents.get())), 
                            self.var_nh.get(),
                            str(int(self.var_totaldays.get())-int(self.var_absents.get())+int(self.var_nh.get())),
                            self.var_emp_code.get(),
                        )
                    )  
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Record Updated Successfully")
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")



    def calculate(self):
        # Check if any required fields are empty
        if (
            self.var_month.get() == ''
            or self.var_year.get() == ''
            or self.var_bsalary.get() == ''
            or self.var_totaldays.get() == ''
            or self.var_absents.get() == ''
            or self.var_convence.get() == ''
            or self.var_da.get() == ''
            or self.var_spl.get() == ''
        ):
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                # Set default values to 0 if not entered
                self.var_advance.set(0 if self.var_advance.get() == '' else int(self.var_advance.get()))
                self.var_incentive.set(0 if self.var_incentive.get() == '' else int(self.var_incentive.get()))

                # Additional checks for empty strings before conversion
                if int(self.var_absents.get()) == 0:
                    self.var_nh.set('1')
                else:
                    self.var_nh.set('0')

                per_basic = int(self.var_bsalary.get()) / int(self.var_totaldays.get())
                month_basic = per_basic * (
                    int(self.var_totaldays.get())
                    - int(self.var_absents.get())
                    + int(self.var_nh.get())
                    + int(self.var_ph.get())
                )
                self.var_earned_bsalary.set(round(month_basic))

                per_da = int(self.var_da.get()) / int(self.var_totaldays.get())
                month_da = per_da * (
                    int(self.var_totaldays.get())
                    - int(self.var_absents.get())
                    + int(self.var_nh.get())
                    + int(self.var_ph.get())
                )
                self.var_earned_da.set(round(month_da))

                per_allowance = int(self.var_spl.get()) / int(self.var_totaldays.get())
                month_allowance = per_allowance * (
                    int(self.var_totaldays.get())
                    - int(self.var_absents.get())
                    + int(self.var_nh.get())
                    + int(self.var_ph.get())
                )
                self.var_earned_spl.set(round(month_allowance))

                per_conveyance = int(self.var_convence.get()) / int(self.var_totaldays.get())
                month_conveyance = per_conveyance * (
                    int(self.var_totaldays.get())
                    - int(self.var_absents.get())
                    + int(self.var_nh.get())
                    + int(self.var_ph.get())
                )
                self.var_earned_convence.set(round(month_conveyance))

                fixed_salary = (
                    int(self.var_bsalary.get())
                    + int(self.var_da.get())
                    + int(self.var_spl.get())
                    + int(self.var_convence.get())
                )
                self.var_ftsalary.set(round(fixed_salary))

                gross_total = month_basic + month_da + month_allowance + month_conveyance
                self.var_gtsalary.set(round(gross_total))

                pf = gross_total * 0.06
                self.var_pf.set(round(pf))

                esi = gross_total * 0.0075
                self.var_esi.set(round(esi))

                net_salary = gross_total - pf - esi + int(self.var_incentive.get()) - int(self.var_advance.get())
                self.var_ntsalary.set(round(net_salary))

            except ValueError as ve:
                messagebox.showerror('Error', f"Error in calculations: {str(ve)}")


    def update_attendance_and_calculate(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', db='vms')
            cur = con.cursor()

            # Fetch all records from the summaryatten table
            cur.execute("SELECT * FROM summaryatten")
            rows = cur.fetchall()
            self.var_ph.set(0 if self.var_ph.get() == '' else int(self.var_ph.get()))

            for row in rows:
                emp_code = row[0]
                absent = row[2]

                # Update the attendance table
                cur.execute("""
                    UPDATE `attendance` SET 
                    `name`=%s, 
                    `no_of_payable`=%s, 
                    `no_of_days_present`=%s,
                    `nh_fh_ot_days`=%s,
                    `total_days_present`=%s 
                    WHERE `emp_code`=%s
                    """,
                    (
                        row[1],  # Assuming `name` is in the 2nd position in summaryatten
                        self.var_totaldays.get(),
                        str(int(self.var_totaldays.get())-int(absent)),
                        str(int(self.var_ph.get())),
                        str(int(self.var_totaldays.get())-int(absent)+int(self.var_ph.get())),
                        emp_code
                    )
                )
                self.search3(emp_code)
                self.calculate()
                self.update2(emp_code)

            self.primary()
            self.secondary()

            con.commit()
            con.close()

            messagebox.showinfo("Success", "Attendance and Salary Details Updated Successfully")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")


    def update2(self, emp_code):
        if self.var_emp_code.get() == '':
            messagebox.showerror("Error", "Employee details are required")
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', db='vms')
                cur = con.cursor()
                cur.execute("SELECT * FROM salary_details WHERE emp_code=%s", (self.var_emp_code.get()))
                row = cur.fetchone()
                cur1 = con.cursor()
                cur1.execute("SELECT * FROM bank_details WHERE emp_code=%s", (self.var_emp_code.get()))
                row1 = cur1.fetchone()
                if row is None and row1 is None:
                    messagebox.showerror("Error", "This employee ID is invalid. Try again with a valid Employee ID", parent=self.root)
                else:
                    cur.execute("""
                       UPDATE `salary_details` SET `name`=%s,`designation`=%s,`fixed_salary`=%s,`no_of_payable`=%s,`no_of_days_present`=%s,`nh_fh_ot_days`=%s,`total_days_present`=%s,`fbasic`=%s,`fda`=%s,`fallowance`=%s,`fconveyance`=%s,`fixed_salary_1`=%s,`ebasic`=%s,`eda`=%s,`eallowance`=%s,`econveyance`=%s,`gross_salary`=%s,`pf`=%s,`esi`=%s,`other`=%s,`ntsalary`=%s WHERE `emp_code`=%s
                        """,
                        (
                            self.var_name.get(),
                            self.var_designation.get(),
                            self.var_ftsalary.get(),
                            self.var_totaldays.get(),
                            str(int(self.var_totaldays.get())-int(self.var_absents.get())), 
                            self.var_nh.get(),
                            str(int(self.var_totaldays.get())-int(self.var_absents.get())+int(self.var_nh.get())+int(self.var_ph.get())),
                            self.var_bsalary.get(),
                            self.var_da.get(),
                            self.var_spl.get(),
                            self.var_convence.get(),
                            self.var_ftsalary.get(),
                            self.var_earned_bsalary.get(),
                            self.var_earned_da.get(),
                            self.var_earned_spl.get(),
                            self.var_earned_convence.get(),
                            self.var_gtsalary.get(),
                            self.var_pf.get(),
                            self.var_esi.get(),     
                            self.var_incentive.get(),    
                            self.var_ntsalary.get(), 
                            self.var_emp_code.get(),
                            
                        )
                    )
                    cur1.execute("""
                        UPDATE `bank_details` SET `name`=%s,`bank`=%s,`acctno`=%s,`ifscode`=%s,`ntsalary`=%s WHERE `emp_code`=%s
                        """,
                        (
                            self.var_name.get(),
                            self.var_bank.get(),
                            self.var_acctno.get(),
                            self.var_ifscode.get(),
                            self.var_ntsalary.get(),
                            self.var_emp_code.get()
                        )
                    )
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Record Updated Successfully")
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")



    def check_connection(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',db='vms')
            cur=con.cursor()
            cur2=con.cursor()
            cur3=con.cursor()
            cur4=con.cursor()
            cur5=con.cursor()
            cur.execute("select * from employeepayroll")
            cur2.execute("select * from designation")
            cur3.execute("select * from bank_details")
            cur4.execute("select * from attendance")
            cur4.execute("select * from summaryatten")
            cur5.execute("select * from attendance")
            rows=cur.fetchall()
            rows2=cur2.fetchall()
            rows3=cur3.fetchall()
            rows4=cur4.fetchall()
            rows5=cur5.fetchall()
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def create_database_and_tables(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='')
            cur = con.cursor()

            # Create the database if it doesn't exist
            cur.execute("CREATE DATABASE IF NOT EXISTS vms")

            # Switch to the vms database
            cur.execute("USE vms")

            # Create employeepayroll table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employeepayroll (
                    emp_code VARCHAR(20) PRIMARY KEY,
                    Desgination VARCHAR(20),
                    name TEXT,
                    age TEXT,
                    gender TEXT,
                    email TEXT,
                    hired_location TEXT,
                    doj TEXT,
                    dob TEXT,
                    experience TEXT,
                    proof_id TEXT,
                    contactno TEXT,
                    status TEXT,
                    address TEXT
                )
            """)

            # Create designation table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS designation (
                    designation VARCHAR(20) PRIMARY KEY,
                    basic TEXT,
                    da TEXT,
                    Conveyance TEXT,
                    allowance TEXT,
                    fixed_salary TEXT
                )
            """)

            # Create bank_details table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bank_details (
                    emp_code VARCHAR(20) PRIMARY KEY,
                    name TEXT,
                    bank TEXT,
                    acctno TEXT,
                    ifscode TEXT,
                    ntsalary TEXT
                )
            """)

            # Create attendance table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    emp_code VARCHAR(20) PRIMARY KEY,
                    name TEXT,
                    no_of_payable TEXT,
                    no_of_days_present TEXT,
                    nh_fh_ot_days TEXT,
                    total_days_present TEXT
                )
            """)

            # Create summaryatten table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS summaryatten (
                    emp_code VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(20),
                    absent TEXT
                )
            """)

            # Create salary_details table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS salary_details (
                    emp_code VARCHAR(20),
                    name TEXT,
                    designation VARCHAR(20),
                    fixed_salary TEXT,
                    no_of_payable TEXT,
                    no_of_days_present TEXT,
                    nh_fh_ot_days TEXT,
                    total_days_present TEXT,
                    fbasic TEXT,
                    fda TEXT,
                    fallowance TEXT,
                    fconveyance TEXT,
                    fixed_salary_1 TEXT,
                    ebasic TEXT,
                    eda TEXT,
                    eallowance TEXT,
                    econveyance TEXT,
                    gross_salary TEXT,
                    pf TEXT,
                    esi TEXT,
                    advance TEXT,
                    total_deduction TEXT,
                    other TEXT,
                    ntsalary TEXT
                )
            """)

            # Commit the changes
            con.commit()

            # Close the cursor and connection
            cur.close()
            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")



    def show1(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',db='vms')
            cur=con.cursor()
            cur.execute("select * from designation")
            rows=cur.fetchall()
            self.designation_tree.delete(*self.designation_tree.get_children())
            for row in rows:
                self.designation_tree.insert('',END,values=row)
            con.close()
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def show(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',db='vms')
            cur=con.cursor()
            cur.execute("select * from employeepayroll")
            
            rows=cur.fetchall()
            self.employee_tree.delete(*self.employee_tree.get_children())
            for row in rows:
                self.employee_tree.insert('',END,values=row)
            con.close()
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}")


    def show2(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',db='vms')
            cur=con.cursor()
            cur.execute("select * from bank_details")
            rows=cur.fetchall()
            self.bank_tree.delete(*self.bank_tree.get_children())
            for row in rows:
                self.bank_tree.insert('',END,values=row)
            con.close()
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def show3(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',db='vms')
            cur=con.cursor()
            cur.execute("select * from attendance")
            rows=cur.fetchall()
            self.attendance_tree.delete(*self.attendance_tree.get_children())
            for row in rows:
                self.attendance_tree.insert('',END,values=row)
            con.close()
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def show4(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',db='vms')
            cur=con.cursor()
            cur.execute("select * from salary_details")
            rows=cur.fetchall()
            self.salary_tree.delete(*self.salary_tree.get_children())
            for row in rows:
                self.salary_tree.insert('',END,values=row)
            con.close()
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}")




    def employee_frame(self):
        self.root2=Toplevel(self.root)
        self.root2.title("Employee Payroll Management System | Developed By SRIKANTH BASKAR")
        self.root2.geometry("1000x500+120+60")
        self.root2.config(bg="White")
        title=Label(self.root2,text="ALL Employee Details",font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).pack(side=TOP,fill=X)
        self.root2.focus_force()

        scrolly=Scrollbar(self.root2,orient=VERTICAL)
        scrollx=Scrollbar(self.root2,orient=HORIZONTAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)

        self.employee_tree=ttk.Treeview(self.root2,columns=('emp_code', 'designation', 'name', 'age', 'gender', 'email', 'hired_location', 'doj', 'dob', 'experience', 'proof_id', 'contact_no', 'status', 'address'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.employee_tree.heading('emp_code',text='Employee Code')
        self.employee_tree.heading('designation',text='Designation')
        self.employee_tree.heading('name',text='Name')
        self.employee_tree.heading('age',text='Age')
        self.employee_tree.heading('gender',text='Gender')
        self.employee_tree.heading('email',text='Email')
        self.employee_tree.heading('hired_location',text='Hired Location')
        self.employee_tree.heading('doj',text='D.O.J')
        self.employee_tree.heading('dob',text='D.O.B')
        self.employee_tree.heading('experience',text='Experience')
        self.employee_tree.heading('proof_id',text='Proof Id')
        self.employee_tree.heading('contact_no',text='Contact No')
        self.employee_tree.heading('status',text='Status')
        self.employee_tree.heading('address',text='Address')
        self.employee_tree['show']='headings'

        
        self.employee_tree.column('emp_code',width=100)
        self.employee_tree.column('designation',width=100)
        self.employee_tree.column('name',width=100)
        self.employee_tree.column('age',width=100)
        self.employee_tree.column('gender',width=50)
        self.employee_tree.column('email',width=200)
        self.employee_tree.column('hired_location',width=100)
        self.employee_tree.column('doj',width=100)
        self.employee_tree.column('dob',width=100)
        self.employee_tree.column('experience',width=100)
        self.employee_tree.column('proof_id',width=100)
        self.employee_tree.column('contact_no',width=120)
        self.employee_tree.column('status',width=100)
        self.employee_tree.column('address',width=500)
        scrollx.config(command=self.employee_tree.xview)
        scrolly.config(command=self.employee_tree.yview)
        self.employee_tree.pack(fill=BOTH,expand=1)
        self.show()


        self.root2.mainloop()


    def desgination_frame(self):
        self.var_ftsalary_1=StringVar()
        self.var_convence_1=StringVar()
        self.var_da_1=StringVar()
        self.var_spl_1=StringVar()
        self.var_bsalary_1=StringVar()
        self.var_designation_1=StringVar()
        self.root3=Toplevel(self.root)
        self.root3.title("Employee Payroll Management System | Developed By SRIKANTH BASKAR")
        self.root3.geometry("1000x500+120+60")
        self.root3.config(bg="White")

        title=Label(self.root3,text="Desgination",font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).pack(side=TOP,fill=X)
        btn_delete1 = Button(self.root3,text="Delete",command=self.delete1,font=("times new roman", 13), bg="red", fg="white").place(x=860, y=15, height=30, width=120)
        btn_add = Button(self.root3,text="Add",command=self.add1,font=("times new roman", 13), bg="green", fg="white").place(x=730, y=15, height=30, width=120)
        Label(self.root3,font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).pack(side=BOTTOM,fill=X)
        #====ROW1=============
        txt_designation_1=Entry(self.root3,font=("times new roman",15),textvariable=self.var_designation_1,bg="lightyellow",fg="black").place(x=20,y=460,width=150)
        #====ROW3=============
        txt_basic_1=Entry(self.root3,font=("times new roman",15),textvariable=self.var_bsalary_1,bg="lightyellow",fg="black").place(x=180,y=460,width=150)
        txt_da_1=Entry(self.root3,font=("times new roman",15),textvariable=self.var_da_1,bg="lightyellow",fg="black").place(x=340,y=460,width=150)
        #====ROW4=============
        txt_convence_1=Entry(self.root3,font=("times new roman",15),textvariable=self.var_convence_1,bg="lightyellow",fg="black").place(x=500,y=460,width=150)
        txt_spl_1=Entry(self.root3,font=("times new roman",15),textvariable=self.var_spl_1,bg="lightyellow",fg="black").place(x=660,y=460,width=150)
        fixedsalary_1=Entry(self.root3,font=("times new roman",15),textvariable=self.var_ftsalary_1,bg="white",fg="black").place(x=820,y=460,width=150)
        calculate_button = tk.Button(self.root3, command=self.calculate_fixed_salary)
        calculate_button.place(x=980, y=460)
        
        self.root3.focus_force()

        scrolly=Scrollbar(self.root3,orient=VERTICAL)
        scrollx=Scrollbar(self.root3,orient=HORIZONTAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)


        self.designation_tree=ttk.Treeview(self.root3,columns=('designation','basic','da','conveyance','allowance','fixed_salary'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.designation_tree.heading('designation',text='Desgination')
        self.designation_tree.heading('basic',text='Basic')
        self.designation_tree.heading('da',text='DA')
        self.designation_tree.heading('conveyance',text='Conveyance')
        self.designation_tree.heading('allowance',text='Allowance')
        self.designation_tree.heading('fixed_salary',text='Fixed Salary')
        self.designation_tree['show']='headings'

        self.designation_tree.column('designation',width=100)
        self.designation_tree.column('basic',width=100)
        self.designation_tree.column('da',width=100)
        self.designation_tree.column('conveyance',width=100)
        self.designation_tree.column('allowance',width=100)
        self.designation_tree.column('fixed_salary',width=100)
        scrollx.config(command=self.designation_tree.xview)
        scrolly.config(command=self.designation_tree.yview)
        self.designation_tree.pack(fill=BOTH,expand=1)
        self.show1()

        self.root3.mainloop()
    
    def calculate_fixed_salary(self):
        # Get values from Entry widgets and convert to integers
        basic = int(self.var_bsalary_1.get() or 0)
        da = int(self.var_da_1.get() or 0)
        convence = int(self.var_convence_1.get() or 0)
        spl = int(self.var_spl_1.get() or 0)

        # Calculate total
        total = basic + da + convence + spl

        # Update the fixedsalary_1 Entry widget
        self.var_ftsalary_1.set(total)

    def bankdetails_frame(self):
        self.root4=Toplevel(self.root)
        self.root4.title("Employee Payroll Management System | Developed By SRIKANTH BASKAR")
        self.root4.geometry("1000x500+120+60")
        self.root4.config(bg="White")
        title=Label(self.root4,text="Bank Details",font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).pack(side=TOP,fill=X)
        self.root4.focus_force()

        scrolly=Scrollbar(self.root4,orient=VERTICAL)
        scrollx=Scrollbar(self.root4,orient=HORIZONTAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)


        self.bank_tree=ttk.Treeview(self.root4,columns=('emp_code','name','bank','acctno','ifscode','ntsalary'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.bank_tree.heading('emp_code',text='Emp Code')
        self.bank_tree.heading('name',text='Name')
        self.bank_tree.heading('bank',text='Bank')
        self.bank_tree.heading('acctno',text='Account No')
        self.bank_tree.heading('ifscode',text='IFS Code')
        self.bank_tree.heading('ntsalary',text='Net Salary')
        self.bank_tree['show']='headings'

        self.bank_tree.column('emp_code',width=100)
        self.bank_tree.column('name',width=100)
        self.bank_tree.column('bank',width=100)
        self.bank_tree.column('acctno',width=100)
        self.bank_tree.column('ifscode',width=100)
        self.bank_tree.column('ntsalary',width=100)
        scrollx.config(command=self.bank_tree.xview)
        scrolly.config(command=self.bank_tree.yview)
        self.bank_tree.pack(fill=BOTH,expand=1)
        self.show2()
        self.root4.mainloop()

    def attendancedetails_frame(self):
        self.root5=Toplevel(self.root)
        self.root5.title("Employee Payroll Management System | Developed By SRIKANTH BASKAR")
        self.root5.geometry("1000x500+120+60")
        self.root5.config(bg="White")
        title=Label(self.root5,text="Attendance Details",font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).pack(side=TOP,fill=X)
        self.root5.focus_force()

        scrolly=Scrollbar(self.root5,orient=VERTICAL)
        scrollx=Scrollbar(self.root5,orient=HORIZONTAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)

        self.attendance_tree=ttk.Treeview(self.root5,columns=('emp_code','name','no_of_payable','no_of_days_present','nh_fh_ot_days','total_days_present'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.attendance_tree.heading('emp_code',text='Emp Code')
        self.attendance_tree.heading('name',text='Name')
        self.attendance_tree.heading('no_of_payable',text='No of Payable')
        self.attendance_tree.heading('no_of_days_present', text='No of days Present')
        self.attendance_tree.heading('nh_fh_ot_days',text='NH FH OT Days')
        self.attendance_tree.heading('total_days_present',text='Total Days Persent')
        self.attendance_tree['show']='headings'

        self.attendance_tree.column('emp_code',width=100)
        self.attendance_tree.column('name',width=100)
        self.attendance_tree.column('no_of_payable',width=100)
        self.attendance_tree.column('no_of_days_present', width=100)
        self.attendance_tree.column('nh_fh_ot_days',width=100)
        self.attendance_tree.column('total_days_present',width=100)
        scrollx.config(command=self.attendance_tree.xview)
        scrolly.config(command=self.attendance_tree.yview)
        self.attendance_tree.pack(fill=BOTH,expand=1)
        self.show3()
        self.root5.mainloop()

    def connect_to_database(self):
        return pymysql.connect(host='localhost', user='root', password='', db='vms')

    def execute_query(self, cursor, query):
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=columns)

    def export_data_to_sheet(self, writer, data, sheet_name, title):
        if not data.empty:
            data.columns = [col.title().replace('_', ' ') for col in data.columns]  # Capitalize and replace underscores
            data.to_excel(writer, sheet_name=sheet_name, index=False, header=True, startrow=2)

            # Write the title at the beginning of the sheet
            worksheet = writer.sheets[sheet_name]
            worksheet.write(0, 0, title, writer.book.add_format({'bold': True, 'font_size': 14}))


    def primary(self):
        con = self.connect_to_database()
        cur = con.cursor()

        salary_data = self.execute_query(cur, "SELECT * FROM `salary_details` WHERE `emp_code` IN (SELECT `emp_code` FROM `employeepayroll` WHERE `status` = 'Primary')")
        salary_title = "SRI VELMURUGAN SUPERMARKET - Salary Details"

        # Execute and export data from bank_details
        bank_data = self.execute_query(cur, "SELECT * FROM `bank_details` WHERE `emp_code` IN (SELECT `emp_code` FROM `employeepayroll` WHERE `status` = 'Primary')")
        bank_title = "SRI VELMURUGAN SUPERMARKET - Bank Details"

        # Execute and export data from attendance
        attendance_data = self.execute_query(cur, "SELECT * FROM `attendance` WHERE `emp_code` IN (SELECT `emp_code` FROM `employeepayroll` WHERE `status` = 'Primary')")
        attendance_title = "SRI VELMURUGAN SUPERMARKET - Attendance Details"

        con.close()

        # Ask user to choose the destination to store the Excel file
        excel_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if excel_file_path:
            with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
                # Store data in Salary_Details sheet with total row
                self.export_data_to_sheet(writer, salary_data, 'Salary_Details', salary_title)

                # Store data in Bank_Details sheet
                self.export_data_to_sheet(writer, bank_data, 'Bank_Details', bank_title)

                # Store data in Attendance sheet
                self.export_data_to_sheet(writer, attendance_data, 'Attendance', attendance_title)

                # Create a new sheet named "Printout" with salary details and total row
                self.export_data_to_sheet(writer, salary_data, 'Printout', salary_title)

            messagebox.showinfo("Export Successful", f'Data has been exported to {excel_file_path}')

    def secondary(self):
        con = self.connect_to_database()
        cur = con.cursor()

        # Fetch and display data from salary_details
        salary_data = self.execute_query(cur, "SELECT * FROM `salary_details` WHERE `emp_code` IN (SELECT `emp_code` FROM `employeepayroll` WHERE `status` = 'Secondary')")
        salary_title = "SRI VELMURUGAN SUPERMARKET - Secondary Salary Details"

        # Fetch and export data from attendance
        attendance_data = self.execute_query(cur, "SELECT * FROM `attendance` WHERE `emp_code` IN (SELECT `emp_code` FROM `employeepayroll` WHERE `status` = 'Secondary')")
        attendance_title = "SRI VELMURUGAN SUPERMARKET - Secondary Attendance Details"

        con.close()

        # Ask user to choose the destination to store the Excel file
        excel_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if excel_file_path:
            with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
                # Store data in Salary_Details sheet
                self.export_data_to_sheet(writer, salary_data, 'Salary_Details', salary_title)

                # Store data in Attendance sheet
                self.export_data_to_sheet(writer, attendance_data, 'Attendance', attendance_title)

                # Create a new sheet named "Printout" with salary details and total row
                self.export_data_to_sheet(writer, salary_data, 'Printout', salary_title)

            messagebox.showinfo("Export Successful", f'Data has been exported to {excel_file_path}')



        



    def salary_frame(self):
        self.root6=Toplevel(self.root)
        self.root6.title("Employee Payroll Management System | Developed By SRIKANTH BASKAR")
        self.root6.geometry("1000x500+120+60")
        self.root6.config(bg="White")


        title=Label(self.root6,text="Salary Details",font=("times new roman",30,"bold"),bg="black",fg="white",anchor="w",padx=10).pack(side=TOP,fill=X)
        btn_add2 = Button(self.root6,text="PRIMARY",command=self.primary,font=("times new roman", 13), bg="green", fg="white").place(x=860, y=15, height=30, width=120)
        btn_add2 = Button(self.root6,text="OTHER",command=self.secondary,font=("times new roman", 13), bg="green", fg="white").place(x=730, y=15, height=30, width=120)
        self.root6.focus_force()

        scrolly=Scrollbar(self.root6,orient=VERTICAL)
        scrollx=Scrollbar(self.root6,orient=HORIZONTAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)
        self.salary_tree=ttk.Treeview(self.root6,columns=('emp_code', 'name', 'designation', 'fixed_salary', 'no_of_payable', 'no_of_days_present', 'nh_fh_ot_days', 'total_days_present', 'fbasic', 'fda', 'fallowance', 'fconveyance', 'fixed_salary_1', 'ebasic', 'eda', 'eallowance', 'econveyance', 'gross_salary', 'pf', 'esi','advance','total_deduction', 'other', 'ntsalary'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.salary_tree.heading('emp_code',text='Emp Code')
        self.salary_tree.heading('name',text='Name')
        self.salary_tree.heading('designation',text='Designation')
        self.salary_tree.heading('fixed_salary',text='Fixed Salary')
        self.salary_tree.heading('no_of_payable',text='No of Payable')
        self.salary_tree.heading('no_of_days_present', text='No of days Present')
        self.salary_tree.heading('nh_fh_ot_days',text='NH FH OT Days')
        self.salary_tree.heading('total_days_present',text='Total Days Persent')
        self.salary_tree.heading('fbasic',text='Basic')
        self.salary_tree.heading('fda',text='DA')
        self.salary_tree.heading('fallowance',text='HRS/SPL/Allowance')
        self.salary_tree.heading('fconveyance',text='Conveyance')
        self.salary_tree.heading('fixed_salary_1',text='Fixed Salary')
        self.salary_tree.heading('ebasic',text='Basic')
        self.salary_tree.heading('eda',text='DA')
        self.salary_tree.heading('eallowance',text='HRS/SPL/Allowance')
        self.salary_tree.heading('econveyance',text='Conveyance')
        self.salary_tree.heading('gross_salary',text='Gross Salary')
        self.salary_tree.heading('pf',text='PF')
        self.salary_tree.heading('esi',text='ESI')
        self.salary_tree.heading('advance',text='Advance')
        self.salary_tree.heading('total_deduction',text='Total Deduction')
        self.salary_tree.heading('other',text='Incentive/PF')       
        self.salary_tree.heading('ntsalary',text='Net Salary')
        self.salary_tree['show']='headings'

        self.salary_tree.column('emp_code',width=100)
        self.salary_tree.column('name',width=100)
        self.salary_tree.column('designation',width=100)
        self.salary_tree.column('fixed_salary',width=100)
        self.salary_tree.column('no_of_payable',width=100)
        self.salary_tree.column('no_of_days_present', width=100)
        self.salary_tree.column('nh_fh_ot_days',width=100)
        self.salary_tree.column('total_days_present',width=100)
        self.salary_tree.column('fbasic',width=100)
        self.salary_tree.column('fda',width=100)
        self.salary_tree.column('fallowance',width=100)
        self.salary_tree.column('fconveyance',width=100)
        self.salary_tree.column('fixed_salary_1',width=100)
        self.salary_tree.column('ebasic',width=100)
        self.salary_tree.column('eda',width=100)
        self.salary_tree.column('eallowance',width=100)
        self.salary_tree.column('econveyance',width=100)
        self.salary_tree.column('gross_salary',width=100)
        self.salary_tree.column('pf',width=100)
        self.salary_tree.column('esi',width=100)
        self.salary_tree.column('advance',width=100)
        self.salary_tree.column('total_deduction',width=100)     
        self.salary_tree.column('other',width=100)    
        self.salary_tree.column('ntsalary',width=100)
        scrollx.config(command=self.salary_tree.xview)
        scrolly.config(command=self.salary_tree.yview)
        self.salary_tree.pack(fill=BOTH,expand=1)
        self.show4()
        self.root6.mainloop()
        
if __name__ == "__main__":
    root=Tk()
    obj=EmployeeSystem(root)
    root.mainloop()

