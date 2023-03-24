import tkinter as tk
import cv2
from tkinter import filedialog
import face_recognition
import csv
import numpy as np
from datetime import datetime
import os
import pickle

class face_app():
    def __init__(self):
        global video_capture 
        video_capture= cv2.VideoCapture("testtest1.mp4")
        self.f=5
        self.inwriter = 4
        
        self.s=True
        
        self.faces_path = ""
        self.names_path = ""
        
        self.faces =[]
        self.names=[]
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.added_names=[]
        self.students = []
        self.now = datetime.now()
        self.current_date = self.now.strftime("%Y-%m-%d")

        #main window
        self.window = tk.Tk()
        self.window.geometry("420x460")
        self.window.configure(bg="#262627")
        self.window.title("Attendance monitoring using face recognition")
        
        self.start_up()
        
        
        
    def start_up(self):
        
        self.clear_window()
        
        main_frame = tk.Frame(self.window,width =420,height=460,bg='#262627')
        main_frame.pack()
        
        title = tk.Label(main_frame,text='Attendance monitoring',font = 'Arial 20 bold',bg='#262627',fg='white')
        title.place(x=50,y=10)
        

        register_button = tk.Button(main_frame,text = 'Register new students',font = 'Arial 14 bold',height = 1,
                              width = 20, bg="#16C777",fg="white",command = self.register_page)
        register_button.place(x=80,y=100)
        
        load_button = tk.Button(main_frame,text = 'Load from existing data',font = 'Arial 14 bold',height = 1,
                              width =20 ,bg="#16C777",fg="white",command = self.load_page)
        load_button.place(x=80,y=200)
        
        start_button = tk.Button(main_frame,text = 'Start taking attendance',font = 'Arial 14 bold',height = 1,
                              width =20 ,bg="#0078D7",fg="white",command = self.start_fun)
        start_button.place(x=80,y=300)
        
        
        
        
        
    
    def clear_window(self):
        for w in self.window.winfo_children():
            w.destroy()
            
    def browse_faces(self,text):
        self.faces_path = filedialog.askopenfilename()
        text.insert(tk.INSERT, self.faces_path)
    def browse_names(self,text):
        self.names_path = filedialog.askopenfilename()
        text.insert(tk.INSERT, self.names_path)
   
        
        
        
        
    def register_browse_fun(self,frame,text):
        path = filedialog.askdirectory()
        
        for folder in os.listdir(path):
            for name in os.listdir(f"{path}/{folder}"):
                image = face_recognition.load_image_file(f"{path}/{folder}/{name}")
                encoding = face_recognition.face_encodings(image)[0]
                self.face_encodings.append(encoding)
                self.face_names.append(os.path.splitext(os.path.basename(f"{path}/{folder}"))[0])
        with open('dataset_faces.dat', 'wb') as w:
            pickle.dump(self.face_encodings, w)
        with open('dataset_names.dat', 'wb') as s:
            pickle.dump(self.face_names, s)
        self.faces = self.face_encodings
        self.names = self.face_names
        self.students = self.names.copy()
        
        self.now = datetime.now()
        self.current_date = self.now.strftime("%Y-%m-%d")

        self.f = open(self.current_date+'.csv','w+',newline = '')
        self.lnwriter = csv.writer(self.f)
        fourcc =cv2.VideoWriter_fourcc(*'XVID')
        global out
        out= cv2.VideoWriter('out.avi',fourcc,24.0,(int(video_capture.get(3)),int(video_capture.get(4))))
        text.insert(tk.INSERT, path)
        
        done_label = tk.Label(frame,text = 'Done loading',font = 'Arial 14 bold',width=13
                              ,height = 1,fg='white',bg='#262627')
        done_label.place(x=120,y=290)
        
        
        
        
    
    def register_page(self):
        self.clear_window()
        
        self.register_frame = tk.Frame(self.window,width = 420,height = 460,bg = '#262627')
        self.register_frame.pack()
        
        register_label=tk.Label(self.register_frame,text = 'Select images folder path'
                                ,font = 'Arial 20 bold',bg='#262627',fg='white')
        register_label.place(x=50,y=10)
        
        register_text = tk.Text(self.register_frame,width = 50,height=2)
        register_text.place(x=8,y=180)
        
        
        register_browse = tk.Button(self.register_frame,text = "Browse",font = 'Arial 14 bold',width=13,height = 1,
                              bg="#0078D7",fg="white",command=lambda:self.register_browse_fun(self.register_frame,register_text))
        register_browse.place(x=130,y=110)
        
        back_browse = tk.Button(self.register_frame,text = "Back",font = 'Arial 14 bold',width=13,height = 1,
                              bg="red",fg="white",command=self.start_up)
        back_browse.place(x=130,y=350)
        
        

    def load_fun(self,frame):
        
        with open(self.faces_path, 'rb') as w:
            all_face_encodings = pickle.load(w)
        with open(self.names_path, 'rb') as s:
            all_face_names = pickle.load(s)
        self.faces = np.array(list(all_face_encodings))
        self.names = list(all_face_names)
        self.students = self.names.copy()
        self.faces=self.faces.astype('float64')
        
        self.now = datetime.now()
        self.current_date = self.now.strftime("%Y-%m-%d")

        self.f = open(self.current_date+'.csv','w+',newline = '')
        self.lnwriter = csv.writer(self.f)
        fourcc =cv2.VideoWriter_fourcc(*'XVID')
        global out
        out= cv2.VideoWriter('out.avi',fourcc,24.0,(int(video_capture.get(3)),int(video_capture.get(4))))
        done_label = tk.Label(frame,text = 'Done loading',font = 'Arial 14 bold',width=13
                              ,height = 1,fg='white',bg='#262627')
        done_label.place(x=120,y=320)
        
        
    def load_page(self):
        
        self.clear_window()
        
        self.load_frame = tk.Frame(self.window,width = 420,height = 460,bg = '#262627')
        self.load_frame.pack()
        
        load_label_1=tk.Label(self.load_frame,text = 'Select faces path'
                                ,font = 'Arial 16 bold',bg='#262627',fg='white')
        load_label_1.place(x=115,y=10)
        
        
        load_text_1 = tk.Text(self.load_frame,width = 50,height=2)
        load_text_1.place(x=8,y=100)
        
        
        load_browse_1 = tk.Button(self.load_frame,text = "Browse",font = 'Arial 14 bold',width=13,height = 1,
                              bg="#0078D7",fg="white",command=lambda:self.browse_faces(load_text_1))
        load_browse_1.place(x=120,y=50)
        
        
        
        load_label_2=tk.Label(self.load_frame,text = 'Select names path'
                                ,font = 'Arial 16 bold',bg='#262627',fg='white')
        load_label_2.place(x=105,y=140)
        
        
        load_text_2 = tk.Text(self.load_frame,width = 50,height=2)
        load_text_2.place(x=8,y=250)
        
        
        load_browse_2 = tk.Button(self.load_frame,text = "Browse",font = 'Arial 14 bold',width=13,height = 1,
                              bg="#0078D7",fg="white",command=lambda:self.browse_names(load_text_2))
        load_browse_2.place(x=120,y=190)
        
        
        back_browse = tk.Button(self.load_frame,text = "Back",font = 'Arial 14 bold',width=13,height = 1,
                              bg="red",fg="white",command=self.start_up)
        back_browse.place(x=120,y=400)
        
      
        load_button = tk.Button(self.load_frame,text='Load',font = 'Arial 14 bold',width=13,height = 1,
                          bg="#0078D7",fg="white",command=lambda:self.load_fun(self.load_frame))

        load_button.place(x=120,y=345)
        
    def start_fun(self):
        while True:
            _,frame = video_capture.read()
            rgb_small_frame = frame[:,:,::-1]
            if self.s:
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame,self.face_locations)
                face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.faces,face_encoding)
                    name="unknown"
                    face_distance = face_recognition.face_distance(self.faces,face_encoding)
                    best_match_index = np.argmin(face_distance)
                    if matches[best_match_index]:
                        name = self.names[best_match_index]

                    face_names.append(name)
                    if name in self.names:      

                        for (top, right, bottom, left), name in zip(self.face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size


                # Draw a box around the face
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw a label with a name below the face
                            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                            if not(name in self.added_names):
                                        if name in self.students:
                                            self.added_names.append(name)
                                            self.students.remove(name)
                                            print(self.students)
                                            self.now = datetime.now()
                                            current_time = self.now.strftime("%H-%M-%S")
                                            print(name)
                                            self.lnwriter.writerow([name,current_time])
            #time.sleep(1)
            out.write(frame)
            cv2.imshow("attendence system",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        out.release()
        cv2.destroyAllWindows()
        self.f.close()
            
        
        
        
        
    def launch(self):
        self.window.mainloop()
        
        
        
app = face_app()

app.launch()
    
        
        
        
        
        
