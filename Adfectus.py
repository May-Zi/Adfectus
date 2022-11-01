from PIL import Image, ImageTk
from datetime import datetime
from datetime import date
from tkinter import Tk, Label, Button, Entry, Frame, Text, \
BooleanVar, IntVar, StringVar, Canvas, Checkbutton, \
PhotoImage, Toplevel
from tkinter import font as tkFont
import webbrowser
import random
import pickle
import cv2
import os

import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

import numpy as np
from keras.applications.inception_v3 import decode_predictions
from keras.models import load_model

model = load_model('reduced_datasets_model.h5')

profileComplete=False
signup_error=False
login_user_error=False
login_pass_error=False
cur_widgets=[]
emotions = {0:'angry', 1:'disgusted', 2:'afraid',\
 3:'happy', 4:'neutral', 5:'sad', 6:'shocked'}
reduced_emotions = {0:'angry', 1:'afraid',\
 2:'happy', 3:'neutral', 4:'sad'}
preference_dict = {}
current_user = ""
shot_path=""
cur_emotion=""
data=[date.today()]
color = "#4F8991"


if os.path.isdir(os.path.dirname(__file__).replace('\\', '/')+"/profiles")!=True:
   os.mkdir(os.path.dirname(__file__).replace('\\', '/')+"/profiles")

########################################################

instagram_link = "https://www.instagram.com/"
facebook_link = "https://www.facebook.com/"
twitter_link = "https://twitter.com/home"
snapchat_link = "https://accounts.snapchat.com/accounts/login"
tiktok_link = "https://www.tiktok.com/login/"
reddit_link = "https://www.reddit.com/"
whatsapp_link = "https://web.whatsapp.com/"
telegram_link = "https://web.telegram.org/#/im"
messenger_link = "https://www.messenger.com/"

########################################################

youtube_link = "https://youtube.com/"

netflix_link = "https://www.netflix.com/qa-en/login"

media_links = [instagram_link, facebook_link, \
twitter_link, snapchat_link, tiktok_link, reddit_link]

music_links = ["https://www.youtube.com/watch?v=Hkz4SB6wJBM", \
"https://www.youtube.com/watch?v=BsNq_sfYRvE", \
"https://www.youtube.com/watch?v=5qap5aO4i9A", \
"https://youtu.be/lTRiuFIWV54?t=15", \
"https://youtu.be/lTRiuFIWV54?t=628"]

text_links= [instagram_link, facebook_link, \
whatsapp_link, snapchat_link, telegram_link, messenger_link]

########################################################


# main window
root = Tk()
root.geometry('1000x700')
root.configure(bg=color)
root.title("Adfectus")


titleFont = tkFont.Font(family='Colonna MT', size=70)
tkFont.families()

headlineFont = tkFont.Font(family='Colonna MT', size=30)
tkFont.families()

font = tkFont.Font(family='Footlight MT Light', size=24)
tkFont.families()

smallFont = tkFont.Font(family='Footlight MT Light', size=20)
tkFont.families()



l_frame = Frame(root)
l_frame.pack(side="left", fill="both", expand=True)
l_frame.configure(bg=color)
m_frame = Frame(root)
m_frame.pack(side="left", fill="both", expand=True)
m_frame.configure(bg=color)
r_frame = Frame(root)
r_frame.pack(side="right", fill="both", expand=True)
r_frame.configure(bg=color)

tm_frame = Frame(m_frame)
tm_frame.pack(side="top", fill="both", expand=True)
tm_frame.configure(bg=color)
mm_frame = Frame(m_frame)
mm_frame.pack(side="top", fill="both", expand=True)
mm_frame.configure(bg=color)
bm_frame = Frame(m_frame)
bm_frame.pack(side="bottom", fill="both", expand=True)
bm_frame.configure(bg=color)


# to maintain the frame resizing 
l_sizer = Label(l_frame, 
   text="                  ", bg=color)
l_sizer.pack()
m_sizer = Label(mm_frame, 
   text="                    ", bg=color)
m_sizer.pack()
r_sizer = Label(r_frame, 
   text="                  ", bg=color)
r_sizer.pack()

tm_sizer = Label(tm_frame, 
   text="                  ", bg=color)
tm_sizer.pack()
bm_sizer = Label(bm_frame, 
   text="                    ", bg=color)
bm_sizer.pack()


# clearing all the widgets
def clearMain():
   for widget in cur_widgets:
      widget.destroy()

i_themes= PhotoImage(file='themes_icon.png')

# first (welcome) screen
def welcomeScreen():
   global cur_widgets, l_app_phrase, l_app_name, b_themes
   clearMain()
   l_app_phrase = Label(tm_frame, text="let's check your emotion!", \
      font=headlineFont, justify="center", fg="#ffefcc", bg=color)
   l_app_phrase.pack(side="bottom", pady=10)
   l_app_name = Label(tm_frame, text="Adfectus", \
      font=titleFont, justify="center", fg="#ffefcc", bg=color)
   l_app_name.pack(side="bottom")
   b_login=Button(mm_frame, text="Login", \
      font=font, justify="center", bg="#ffefcc",
      width=17, height=1,
      command=lambda:[loginScreen()])
   b_signup=Button(mm_frame, text="New Profile", \
      font=font, justify="center", bg="#ffefcc",
      width=17, height=1,
      command=lambda:[signUpScreen()])
   b_manual=Button(mm_frame, text="Manual", \
      font=font, justify="center", bg="#ffefcc",
      width=17, height=1,
      command=lambda:[manualScreen()])
   b_themes=Button(r_frame, image=i_themes, bg=color, \
      highlightthickness = 0, bd = 0,
      command=lambda:[themeScreen()])
   cur_widgets+=[b_login, b_signup, l_app_name, \
   l_app_phrase, b_manual, b_themes]
   b_login.pack(ipady=5, pady=2, padx=5)
   b_signup.pack(ipady=5, pady=2, padx=5)
   b_manual.pack(ipady=5, pady=2, padx=5)
   b_themes.pack(side="top", anchor="ne", ipady=5, pady=2, padx=20)


def manualScreen():
   global cur_widgets
   clearMain()

   l_manual = Label(mm_frame, text="Manual", \
      font=titleFont, justify="center", fg="#ffefcc", bg=color)
   l_manual.pack()

   manual = Text(mm_frame, bg="#ffefcc", font=smallFont, \
      height=7, width=45, spacing3=30, spacing2=10, wrap=tk.WORD, padx=50)

   manual_text='''
   Welcome to Adfectus! Let's get you started.
   # Making a Profile:
   To make a profile, you will need a username and a password, as is expected. The program will not accept repeated usernames; yours has to be unique. After picking your credentials, you will be surveyed on what you like to do whenever you’re feeling a certain emotion (the range here is angry, afraid, happy, neutral, and sad), and then the social media and texting apps you prefer using. This information will dictate the services you will be getting. You’ll be able to edit and update them at any time.
   
   # Scanning Emotions:
   The first screen you encounter after logging in/signing up will be the emotion-scanning screen. There are a few instructions you’ll want to follow before shooting your picture for the best result:
      1# Remove any face coverages or glasses
      2# Be wary of dimmed or tinted lighting, as it affects the prediction
      3# Center yourself so that your *face* (not necessarily your whole head) is in the marked rectangle
      4# Avoid blurry photos and backgrounds that are dark or easily blend in with your face
   
   # Services:
   After scanning, you’ll be presented with a prediction of your current emotion and a button labeled “next.” upon pressing it, you will be given a “service” based on what your saved preferences for that emotion were. Often, that would take you to a web page, or a social media app.
   
   # Home Screen:
   The home screen is the screen you will be on most of the time. After the initial scant, you will find yourself on that screen. In the home screen you will find the option to get a second service for your predicted emotion, rescan your emotion, edit your preferences, or view your past recorded emotions. You can change the program’s color scheme by pressing the paint brush icon at the top right of this screen and picking a color. Themes can also be changed from the starting screen.
   
   Have fun! :D
   '''
   manual.insert(tk.INSERT, manual_text)
   manual.pack()

   scroll_y = tk.Scrollbar(r_frame, orient="vertical", command=manual.yview)
   scroll_y.pack(side="right", fill="y")

   manual.configure(yscrollcommand=scroll_y.set, state='disabled')

   if profileComplete:
      b_back=Button(l_frame, text="Back", \
         font=font, justify="center", bg="#ffefcc",
         width=4, height=1,
         command=lambda:[homeScreen()])
   else:
      b_back=Button(l_frame, text="Back", \
         font=smallFont, justify="center", bg="#ffefcc",
         command=lambda:[welcomeScreen()])
   b_back.pack(side="bottom", padx=5, pady=5, ipadx=3, ipady=3)

   cur_widgets+=[l_manual, manual, scroll_y, b_back]


def themeScreen():
   global cur_widgets
   top_level = Toplevel(bg="#ffefcc")
   top_level.title("Themes")

   x = root.winfo_x()
   y = root.winfo_y()
   top_level.geometry("%dx%d+%d+%d" % (285, 50, x + 700, y + 150))
   top_level.grab_set()

   b_color_1 = Button(top_level, bg="#148F77", \
      width=3, height=2, command=lambda:[changeTheme("#148F77"), \
      top_level.grab_release(), top_level.destroy()])
   b_color_1.pack(side="left", ipadx=5, padx=3, pady=3)
   b_color_2 = Button(top_level, bg="#E74C3C", \
      width=3, height=2, command=lambda:[changeTheme("#E74C3C"), \
      top_level.grab_release(), top_level.destroy()])
   b_color_2.pack(side="left", ipadx=5, padx=3, pady=3)
   b_color_3 = Button(top_level, bg="#28B463", \
      width=3, height=2, command=lambda:[changeTheme("#28B463"), \
      top_level.grab_release(), top_level.destroy()])
   b_color_3.pack(side="left", ipadx=5, padx=3, pady=3)
   b_color_4 = Button(top_level, bg="#4F8991", \
      width=3, height=2, command=lambda:[changeTheme("#4F8991"), \
      top_level.grab_release(), top_level.destroy()])
   b_color_4.pack(side="left", ipadx=5, padx=3, pady=3)
   b_color_5 = Button(top_level, bg="#F3A11E", \
      width=3, height=2, command=lambda:[changeTheme("#F3A11E"), \
      top_level.grab_release(), top_level.destroy()])
   b_color_5.pack(side="left", ipadx=5, padx=3, pady=3)
   b_color_6 = Button(top_level, bg="#9797F7", \
      width=3, height=2, command=lambda:[changeTheme("#9797F7"), \
      top_level.grab_release(), top_level.destroy()])
   b_color_6.pack(side="left", ipadx=5, padx=3, pady=3)



def changeTheme(new_hex):
   global color
   color=new_hex
   frames=[root, l_frame, m_frame, \
   tm_frame, mm_frame, bm_frame, \
   r_frame, l_sizer, r_sizer, m_sizer, \
   tm_sizer, bm_sizer, b_themes]
   if profileComplete:
      frames+=[l_cur_mood, webcam]
   else: frames+=[l_app_name, l_app_phrase]
   for i in frames:
      i.configure(bg=new_hex)

# screen for creating a profile
def signUpScreen():
   global cur_widgets
   clearMain()
   l_username=Label(mm_frame, text="Username:", \
      bg=color, fg="#ffefcc", font=font, justify="center")
   l_password=Label(mm_frame, text="Password", \
      bg=color, fg="#ffefcc", font=font, justify="center")

   e_username=Entry(mm_frame, bg="#ffefcc", \
      font=font, justify="center")
   e_password=Entry(mm_frame, bg="#ffefcc", \
      font=font, justify="center", show="*")

   cur_widgets+=[e_username, e_password]

   l_username.pack()
   e_username.pack(ipadx=90, ipady=25)
   l_password.pack()
   e_password.pack(ipadx=90, ipady=25)

   b_signup_done=Button(mm_frame, text="SignUp", 
      command=lambda:[signUp(e_username.get(), e_password.get())],
      bg="#ffefcc", font=font, justify="center")
   b_back=Button(l_frame, text="Back", 
      command=lambda:[welcomeScreen()],
      bg="#ffefcc", font=font, justify="center")
   b_signup_done.pack(side="bottom", ipadx=10, ipady=2)
   b_back.pack(side="bottom", ipadx=10, ipady=2, pady=7)

   cur_widgets+=[e_username, e_password, \
   b_signup_done, b_back, l_password, l_username]


# screen for logging back in 
def loginScreen():
   global cur_widgets, e_password, e_username
   clearMain()

   l_username=Label(mm_frame, text="Username:", \
      bg=color, fg="#ffefcc", font=font, justify="center")
   l_password=Label(mm_frame, text="Password", \
      bg=color, fg="#ffefcc", font=font, justify="center")
   e_username=Entry(mm_frame, bg="#ffefcc", \
      font=font, justify="center")
   e_password=Entry(mm_frame, bg="#ffefcc", \
      font=font, justify="center", show="*")

   l_username.pack()
   e_username.pack(ipadx=90, ipady=25)
   l_password.pack()
   e_password.pack(ipadx=90, ipady=25)

   b_login_done=Button(mm_frame, text="LogIn", 
      command=lambda:[logIn(e_username.get(), e_password.get())],
      bg="#ffefcc", font=font, justify="center")
   b_back=Button(l_frame, text="Back", 
      command=lambda:[welcomeScreen()],
      bg="#ffefcc", font=font, justify="center")
   b_login_done.pack(side="bottom", ipadx=10, ipady=2)
   b_back.pack(side="bottom", ipadx=10, ipady=2, pady=7)

   cur_widgets+=[e_username, e_password, \
   b_login_done, b_back, l_username, l_password]


# checks user and password and creates an account
def signUp(username, password):
   global current_user, cur_widgets, signup_error

   if username=="" or password=="":
      return

   path=os.path.dirname(__file__).replace('\\', '/')
   path+="/profiles/"
   path+=username

   if os.path.isdir(path)==True and signup_error==False:
      signup_error=True
      user_taken=Label(tm_frame, text="Username taken", \
         bg="#ffefcc", font=font, justify="center")
      user_taken.pack(side="bottom", ipadx=10, ipady=5)
      cur_widgets+=[user_taken]
   elif os.path.isdir(path)==True and signup_error==True:
      return
   else:
      signup_error=False
      os.mkdir(path)
      outfile = open(path+"/password",'wb')
      pickle.dump(password,outfile)
      outfile.close()
      outfile = open(path+"/data",'wb')
      data=[date.today()]
      pickle.dump(data,outfile)
      outfile.close()
      os.mkdir(path+'/shots')
      os.mkdir(path+'/diary')
      current_user = username
      survey(0)


# checks user and password and logs in an old account
def logIn(username, password):
   global current_user, cur_widgets, preference_dict, \
   media_links, text_links, data, profileComplete, \
   login_user_error, login_pass_error, incorrect_pass, \
   incorrect_user

   if username=="" or password=="":
      return

   path=os.path.dirname(__file__).replace('\\', '/')+"/profiles/"
   path+=username

   if os.path.isdir(path)!=True:
      if login_pass_error==True:
         incorrect_pass.destroy()
      if login_user_error==False:
         login_user_error=True
         incorrect_user=Label(tm_frame, \
            text="Username not recognized.", \
            bg="#ffefcc", font=font, justify="center")
         incorrect_user.pack(ipadx=10, ipady=5)
         cur_widgets+=[incorrect_user]
      elif login_user_error==True:
         return
   else:
      infile = open(path+'/password','rb')
      saved_password = pickle.load(infile)
      infile.close()
      if saved_password!=password:
         if login_user_error==True:
            incorrect_user.destroy()
         if login_pass_error==False:
            login_pass_error=True
            incorrect_pass=Label(tm_frame, \
               text="Wrong password.", bg="#ffefcc", \
               font=font, justify="center")
            incorrect_pass.pack(ipadx=10, ipady=5)
            cur_widgets+=[incorrect_pass]
         elif login_pass_error==True:
            return
      else:
         login_pass_error=False
         login_user_error=False
         current_user = username
         infile = open(path+'/preferences','rb')
         preference_dict = pickle.load(infile)
         infile.close()
         infile = open(path+'/media','rb')
         media_links = pickle.load(infile)
         infile.close()
         infile = open(path+'/text','rb')
         text_links = pickle.load(infile)
         infile.close()
         infile = open(path+'/data','rb')
         data = pickle.load(infile)
         infile.close()
         profileComplete=True
         root.after(1000, shootScreen())


# survey recursive function
def survey(index):
   global cur_widgets, emotions, media_var, music_var,\
   text_var, diary_var, netflix_var, youtube_var,\
   current_user, preference_dict

   clearMain()

   if index==5:
      updatePreferenceFile()
      mediaPrefs()
      return

   question=Label(tm_frame, \
      text=f"What do you like to do when you're feeling {reduced_emotions[index]}?", 
      bg="#ffefcc", font=font, justify="center")
   question.pack(ipadx=10, ipady=2)
   clarify=Label(tm_frame, text="Select all that applies.",
      bg="#ffefcc", font=font, justify="center")
   clarify.pack(ipadx=10, ipady=2)

   music_var = IntVar()
   youtube_var = IntVar()
   netflix_var = IntVar()
   diary_var = IntVar()
   text_var = IntVar()
   media_var = IntVar()

   c_music = Checkbutton(mm_frame, \
      text = "Listen to music", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = music_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_music.pack(ipadx=10, ipady=2)
   c_youtube = Checkbutton(mm_frame, \
      text = "Watch youtube", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = youtube_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_youtube.pack(ipadx=10, ipady=2)
   c_netflix = Checkbutton(mm_frame, \
      text = "Watch netflix", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = netflix_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_netflix.pack(ipadx=10, ipady=2)
   c_diary = Checkbutton(mm_frame, \
      text = "Write a diary", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = diary_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_diary.pack(ipadx=10, ipady=2)
   c_text = Checkbutton(mm_frame, \
      text = "Text a friend", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = text_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_text.pack(ipadx=10, ipady=2)
   c_media = Checkbutton(mm_frame, \
      text = "Go on social media", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = media_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_media.pack(ipadx=10, ipady=2)
   
   b_next = Button(r_frame, text="Next", \
      command=lambda:[updatePreference(reduced_emotions[index]), survey(index+1)], \
      bg="#ffefcc", font=smallFont, justify="center")

   if index>0:
      b_back = Button(l_frame, text="Go Back", \
         command=lambda:[updatePreference(reduced_emotions[index]), survey(index-1)], \
         bg="#ffefcc", font=smallFont, justify="center")
      b_back.pack(side="bottom", ipadx=10, ipady=2)
      cur_widgets+=[b_back]

   cur_widgets+=[question, clarify, c_media, \
   c_music, c_text, c_diary, c_netflix, c_youtube, b_next]
   b_next.pack(side="bottom", ipadx=10, ipady=2)


# updates the preference in the loaded preference-dict
def updatePreference(emotion):
   global preference_dict

   if emotion=="":
      return
   elif emotion=="media":
      updateMedia(instagram_var.get(), facebook_var.get(), \
         twitter_var.get(), snapchat_var.get(), tiktok_var.get(), reddit_var.get())
   elif emotion=="text":
      updateText(instagram_var.get(), facebook_var.get(), \
         whatsapp_var.get(), snapchat_var.get(), telegram_var.get(), messenger_var.get())
   else:
      d = {0:'music', 1:'youtube', 2:'netflix', \
      3:'diary', 4:'text', 5:'media'}

      var_list = [music_var, youtube_var, \
      netflix_var, diary_var, text_var, media_var]
      results=[]
      preference_dict[emotion]=[]

      for i in var_list:
         results.append(i.get())
      for i in range(len(results)):
         if results[i]==1:
            preference_dict[emotion].append(d[i])

      updatePreferenceFile()
   

def mediaPrefs():
   global cur_widgets
   clearMain()

   question=Label(tm_frame, \
      text=f"What social media platforms do you like browsing?", 
      bg="#ffefcc", font=font, justify="center")
   question.pack(ipadx=10, ipady=2)
   clarify=Label(tm_frame, text="Select all that applies.",
      bg="#ffefcc", font=font, justify="center")
   clarify.pack(ipadx=10, ipady=2)

   instagram_var = IntVar()
   facebook_var = IntVar()
   twitter_var = IntVar()
   snapchat_var = IntVar()
   tiktok_var = IntVar()
   reddit_var = IntVar()

   c_instagram = Checkbutton(mm_frame, \
      text = "Instagram", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = instagram_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_instagram.pack(ipadx=10, ipady=2)
   c_facebook = Checkbutton(mm_frame, \
      text = "facebook", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = facebook_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_facebook.pack(ipadx=10, ipady=2)
   c_twitter = Checkbutton(mm_frame, \
      text = "twitter", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = twitter_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_twitter.pack(ipadx=10, ipady=2)
   c_snapchat = Checkbutton(mm_frame, \
      text = "snapchat", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = snapchat_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_snapchat.pack(ipadx=10, ipady=2)
   c_tiktok = Checkbutton(mm_frame, \
      text = "tiktok", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = tiktok_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_tiktok.pack(ipadx=10, ipady=2)
   c_reddit = Checkbutton(mm_frame, \
      text = "reddit", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = reddit_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_reddit.pack(ipadx=10, ipady=2)
   
   b_media_done = Button(r_frame, text="OK", \
      command=lambda:[updateMedia(instagram_var.get(), \
         facebook_var.get(), twitter_var.get(), \
         snapchat_var.get(), tiktok_var.get(), \
         reddit_var.get())],\
      bg="#ffefcc", font=smallFont, justify="center")
   b_media_done.pack(side="bottom", ipadx=10, ipady=2)

   cur_widgets+=[c_instagram, c_facebook, c_twitter, \
   c_snapchat, c_tiktok, c_reddit, b_media_done, \
   question, clarify]


def updateMedia(instagram, facebook, twitter, snapchat, tiktok, reddit):
   global media_links
   if sum([instagram, facebook, twitter, snapchat, tiktok, reddit])!=0:
      if instagram==0 and instagram_link in media_links:
         media_links.remove(instagram_link)
      if facebook==0 and facebook_link in media_links:
         media_links.remove(facebook_link)
      if twitter==0 and twitter_link in media_links:
         media_links.remove(twitter_link)
      if snapchat==0 and snapchat_link in media_links:
         media_links.remove(snapchat_link)
      if tiktok==0 and tiktok_link in media_links:
         media_links.remove(tiktok_link)
      if reddit==0 and reddit_link in media_links:
         media_links.remove(reddit_link)

      if instagram==1 and instagram_link not in media_links:
         media_links.append(instagram_link)
      if facebook==1 and facebook_link not in media_links:
         media_links.append(facebook_link)
      if twitter==1 and twitter_link not in media_links:
         media_links.append(twitter_link)
      if snapchat==1 and snapchat_link not in media_links:
         media_links.append(snapchat_link)
      if tiktok==1 and tiktok_link not in media_links:
         media_links.append(tiktok_link)
      if reddit==1 and reddit_link not in media_links:
         media_links.append(reddit_link)

   path=os.path.dirname(__file__).replace('\\', '/')+"/profiles/"
   path+=current_user

   if os.path.exists(path+"/media"):
      os.remove(path+"/media")

   outfile = open(path+"/media",'wb')
   pickle.dump(media_links, outfile)
   outfile.close()
   
   if profileComplete==False:
      textPrefs()

def textPrefs():
   global cur_widgets
   clearMain()

   question=Label(tm_frame, \
      text=f"What apps do you typically use for texting?", 
      bg="#ffefcc", font=smallFont, justify="center")
   question.pack(ipadx=10, ipady=2)
   clarify=Label(tm_frame, text="Select all that applies.",
      bg="#ffefcc", font=smallFont, justify="center")
   clarify.pack(ipadx=10, ipady=2)

   instagram_var = IntVar()
   facebook_var = IntVar()
   whatsapp_var = IntVar()
   snapchat_var = IntVar()
   telegram_var = IntVar()
   messenger_var = IntVar()

   c_instagram = Checkbutton(mm_frame, \
      text = "Instagram", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = instagram_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_instagram.pack(ipadx=10, ipady=2)
   c_facebook = Checkbutton(mm_frame, \
      text = "facebook", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = facebook_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_facebook.pack(ipadx=10, ipady=2)
   c_whatsapp = Checkbutton(mm_frame, \
      text = "whatsapp", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = whatsapp_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_whatsapp.pack(ipadx=10, ipady=2)
   c_snapchat = Checkbutton(mm_frame, \
      text = "snapchat", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = snapchat_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_snapchat.pack(ipadx=10, ipady=2)
   c_telegram = Checkbutton(mm_frame, \
      text = "telegram", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = telegram_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_telegram.pack(ipadx=10, ipady=2)
   c_messenger = Checkbutton(mm_frame, \
      text = "messenger", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = messenger_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_messenger.pack(ipadx=10, ipady=2)
   
   b_text_done = Button(r_frame, text="OK", \
      command=lambda:[updateText(instagram_var.get(), \
         facebook_var.get(), whatsapp_var.get(), \
         snapchat_var.get(), telegram_var.get(), \
         messenger_var.get())],\
      bg="#ffefcc", font=smallFont, justify="center")
   b_text_done.pack(side="bottom", ipadx=10, ipady=2)

   cur_widgets+=[c_instagram, c_facebook, c_whatsapp, \
   c_snapchat, c_telegram, c_messenger, b_text_done, \
   question, clarify]


def updateText(instagram, facebook, whatsapp, snapchat, telegram, messenger):
   global text_links
   if sum([instagram, facebook, whatsapp, snapchat, telegram, messenger])!=0:
      if instagram==0 and instagram_link in text_links:
         text_links.remove(instagram_link)
      if facebook==0 and facebook_link in text_links:
         text_links.remove(facebook_link)
      if whatsapp==0 and whatsapp_link in text_links:
         text_links.remove(whatsapp_link)
      if snapchat==0 and snapchat_link in text_links:
         text_links.remove(snapchat_link)
      if telegram==0 and telegram_link in text_links:
         text_links.remove(telegram_link)
      if messenger==0 and messenger_link in text_links:
         text_links.remove(messenger_link)

      if instagram==1 and instagram_link not in text_links:
         text_links.append(instagram_link)
      if facebook==1 and facebook_link not in text_links:
         text_links.append(facebook_link)
      if whatsapp==1 and whatsapp_link not in text_links:
         text_links.append(whatsapp_link)
      if snapchat==1 and snapchat_link not in text_links:
         text_links.append(snapchat_link)
      if telegram==1 and telegram_link not in text_links:
         text_links.append(telegram_link)
      if messenger==1 and messenger_link not in text_links:
         text_links.append(messenger_link)
   
   path=os.path.dirname(__file__).replace('\\', '/')+"/profiles/"
   path+=current_user

   if os.path.exists(path+"/text"):
      os.remove(path+"/text")

   outfile = open(path+"/text",'wb')
   pickle.dump(text_links, outfile)
   outfile.close()

   if profileComplete==False:
      shootScreen()


def shootScreen():
   global cur_widgets, cap, webcam, \
   shoot, webcam_width, webcam_height, profileComplete
   clearMain()

   profileComplete=True

   l_act_natural = Label(tm_frame, \
      text="Position your face in the center and try to act natural.", \
      bg="#ffefcc", font=font, justify="center")
   l_act_natural.pack(side="top", ipadx=10, ipady=1, pady=3)

   # boolean to stop webcam based off of
   shoot=BooleanVar()
   shoot.set(False)

   # get webcam size
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   webcam_height, webcam_width = frame.shape[:2]

   # set window size to webcam size
   webcam = Canvas(mm_frame, width=webcam_width-10, height=webcam_height-10)
   webcam.pack(ipady=1, pady=1)
   showFrames()

   b_shoot=Button(bm_frame, text="Shoot", \
      command=lambda:[shoot.set(True)], \
      bg="#ffefcc", font=smallFont, justify="center")
   b_shoot.pack(ipadx=10, ipady=2, pady=2)
   cur_widgets+=[webcam, b_shoot, l_act_natural]


# displays the current frame on the tk window (recursive)
def showFrames():
   if shoot.get()==1:
      frame = cap.read()[1]
      saveShot(frame)
   else:
      image = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)

      # mirrors the image
      image = cv2.flip(image, 1)

      # reading image using PIL 
      image = Image.fromarray(image)
      image = ImageTk.PhotoImage(image = image)
      webcam.background = image
      bg = webcam.create_image(0, 0, anchor='nw', image=image)

      webcam.create_rectangle(webcam_width//3, webcam_height//5, \
         2*webcam_width//3, 4*webcam_height//5, outline=color, width=3)

      webcam.after(20, showFrames)


# saves the picture/frame
def saveShot(frame):
   global shot_path

   shot_path = os.path.dirname(__file__).replace('\\', '/') +\
    f"/profiles/{current_user}/shots/"
   now=datetime.now()

   for i in str(now):
      if i.isalnum():
         shot_path+=i

   shot_path += '.jpg'
   cv2.imwrite(shot_path, cv2.flip(frame, 1))
   cap.release()
   resultScreen(shot_path)


# predicts picture's emotion using the model
def predict(shot_path):
   global cur_emotion, data

   img = Image.open(shot_path)
   w, h = img.size

   left = w/4
   right = 3*w/4
   upper = h/4
   lower = 3.5*h/4

   img = img.crop([ left, upper, right, lower])
   img = img.convert('L')
   img = img.resize((48,48))
   img = np.array(img)
   img = img / 255.0
   img = img.reshape(1,48,48,1)
   preds = model.predict(img)
   prediction = max(preds[0])
   cur_emotion=emotions[list(preds[0]).index(prediction)]

   data.append(cur_emotion)
   updateData()

   return cur_emotion


# views result
def resultScreen(shot_path):
   global cur_widgets
   clearMain()

   result=predict(shot_path)
   if result=="shocked":
      result="afraid"
   if result=="disgusted":
      result="angry"
   l_result = Label(tm_frame, text=f"It appears you are {result}!",
      bg="#ffefcc", font=font, justify="center")
   l_result.pack(side="bottom" ,ipadx=10, ipady=2)
   if result=="happy":
      l_result2 = Label(mm_frame, text="That's good! :D",
         bg="#ffefcc", font=font, justify="center")
   elif result=="sad":
      l_result2 = Label(mm_frame, text="Oh no :/",
         bg="#ffefcc", font=font, justify="center")
   elif result=="angry" or result=="afraid" or \
   result=="disgusted" or result=="shocked":
      l_result2 = Label(mm_frame, text="Hmm, let's calm you down.",
         bg="#ffefcc", font=font, justify="center")
   elif result=="neutral":
      l_result2 = Label(mm_frame, text="Set back and relax!",
         bg="#ffefcc", font=font, justify="center")
   l_result2.pack(ipadx=10, ipady=2)
   b_okay=Button(r_frame, text="Okay", command=lambda:[runService()],
      bg="#ffefcc", font=font, justify="center")
   b_okay.pack(side="bottom" ,ipadx=10, ipady=2)

   cur_widgets+=[l_result, l_result2, b_okay]


# runs a random service according to the preference-dict
def runService():
   if preference_dict[cur_emotion]==[]:
      service = random.choice(['youtube', 'netflix', \
         'music', 'media', 'text', 'diary'])
   else:
      service = random.choice(preference_dict[cur_emotion])

   if service=='youtube':
      webbrowser.open(youtube_link)
      homeScreen()
   elif service=='netflix':
      webbrowser.open(netflix_link)
      homeScreen()
   elif service=='music':
      webbrowser.open(random.choice(music_links))
      homeScreen()
   elif service=='media':
      webbrowser.open(random.choice(media_links))
      homeScreen()
   elif service=='text':
      webbrowser.open(random.choice(text_links))
      homeScreen()
   elif service=='diary':
      diaryEntry()
   

# a window to type a diary entry into
def diaryEntry():
   global cur_widgets
   clearMain()

   e_title = Text(mm_frame, bg="#ffefcc", font=font, \
      height=1, width=15, spacing1=30, spacing2=10, wrap=tk.WORD, padx=20)
   e_title.pack(ipadx=20, ipady=10, padx=30, pady=20)
   e_title.insert(tk.END, "Name this diary entry")
   e_title.tag_configure("center", justify='center')

   e_text = Text(mm_frame, bg="#ffefcc", font=font, \
      height=4, width=30, spacing1=30, spacing2=10, wrap=tk.WORD, padx=50)
   e_text.pack(ipadx=20, ipady=30, padx=30, pady=20)
   e_text.insert(tk.END, "What would you like to say?")
   e_text.tag_configure("center", justify='center')


   b_make_diary = Button(mm_frame, text="Save entry",
   bg="#ffefcc", font=font, justify="center",
   command=lambda:[makeEntry(e_text.get("1.0",'end-1c'), e_title.get("1.0",'end-1c')), \
   homeScreen()])
   b_make_diary.pack(padx=10, pady=10)
   cur_widgets+=[e_title, e_text, b_make_diary]


# saves the diary entry as a txt file
def makeEntry(text, title):

   path=os.path.dirname(__file__).replace('\\', '/')+"/profiles"+f"/{current_user}/"
   path+='diary/'
   filename=""

   if title=="Name this diary entry" or title=="":
      for i in str(datetime.now())[:-6]:
         if i.isalnum():
            filename+=i
   else:
      filename=title

   completeName=os.path.join(path, filename+'.txt')
   print(completeName)
   new_file = open(completeName, 'w+')
   new_file.write(text)
   new_file.close()



# main screen of the app, with the options and such 
def homeScreen():
   global cur_widgets, l_cur_mood, webcam, b_themes
   clearMain()

   l_cur_mood = Label(l_frame, \
      text=f"Current emotion: {cur_emotion}", \
      width=20, height=1, bg=color, fg="#ffefcc", \
      font=headlineFont, justify="center")
   b_new_service = Button(l_frame, \
      text="Do something else", \
      command=lambda:[runService()],
      width=20, height=1, bg="#ffefcc", \
      font=font, justify="center")
   b_rescan = Button(l_frame, \
      text="Rescan emotion", \
      command=lambda:[shootScreen()],
      width=20, height=1, bg="#ffefcc", \
      font=font, justify="center")
   b_edit_preferences = Button(l_frame, \
      text="Edit preferences", \
      command=lambda:[preferenceScreen()],
      width=20, height=1, bg="#ffefcc", \
      font=font, justify="center")
   b_show_data = Button(l_frame, \
      text="Show past emotions", \
      command=lambda:[dataScreen()],
      width=20, height=1, bg="#ffefcc", \
      font=font, justify="center")
   b_themes=Button(r_frame, image=i_themes, bg=color, \
      highlightthickness = 0, bd = 0,
      command=lambda:[themeScreen()])
   b_themes.pack(side="top", anchor="ne", ipady=5, pady=2, padx=20)

   l_cur_mood.pack(side="top", ipadx=7, ipady=4, pady=50)
   b_new_service.pack(padx=10, pady=5)
   b_rescan.pack(padx=10, pady=5)
   b_edit_preferences.pack(padx=20, pady=5)
   b_show_data.pack(padx=20, pady=5)

   if shot_path!="":
      shot = ImageTk.PhotoImage(file = shot_path)

      webcam = Canvas(mm_frame, width=400, height=500, bg=color)
      webcam.pack()

      webcam.background = shot
      bg = webcam.create_image(200, 250, anchor='center', image=shot)

      cur_widgets+=[webcam]

   b_logout = Button(l_frame, text="LogOut", command=lambda:[welcomeScreen(), profileIncomplete()],
      bg="#ffefcc", font=font, justify="center")
   b_logout.pack(side="bottom", padx=3, pady=10)

   cur_widgets+=[l_cur_mood, b_rescan, b_new_service, \
   b_edit_preferences, b_show_data, b_logout, b_themes]

def profileIncomplete():
   global profileComplete
   profileComplete=False

# screen for showing and editing a user's preferences 
def preferenceScreen():
   global cur_widgets, b_go_back, \
   b_angry_prefs, b_disgusted_prefs,\
    b_afraid_prefs, b_happy_prefs, \
    b_neutral_prefs, b_sad_prefs, \
    b_shocked_prefs, l_preference_page, \
    b_media_prefs, b_text_prefs, l_apps
   clearMain()

   last_viewed_prefs = StringVar()
   last_viewed_prefs.set("")

   l_preference_page = Label(l_frame, \
      text="Preferences:",
      bg="#ffefcc", font=font, justify="center")
   b_go_back = Button(l_frame, \
      text="Go Back", command=lambda:[homeScreen(), \
      updatePreference(last_viewed_prefs.get())],
      width=10, height=1, bg="#ffefcc", \
      font=font, justify="center")
   b_angry_prefs = Button(l_frame, \
      text="Angry", command=lambda:[updatePreference(last_viewed_prefs.get()),\
       prefList("angry"), last_viewed_prefs.set("angry")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")
   b_afraid_prefs = Button(l_frame, \
      text="Afraid", command=lambda:[updatePreference(last_viewed_prefs.get()), \
      prefList("afraid"), last_viewed_prefs.set("afraid")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")
   b_happy_prefs = Button(l_frame, \
      text="Happy", command=lambda:[updatePreference(last_viewed_prefs.get()), \
      prefList("happy"), last_viewed_prefs.set("happy")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")
   b_neutral_prefs = Button(l_frame, \
      text="Neutral", command=lambda:[updatePreference(last_viewed_prefs.get()), \
      prefList("neutral"), last_viewed_prefs.set("neutral")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")
   b_sad_prefs = Button(l_frame, \
      text="Sad", command=lambda:[updatePreference(last_viewed_prefs.get()), \
      prefList("sad"), last_viewed_prefs.set("sad")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")
   b_media_prefs = Button(l_frame, \
      text="Social Media", command=lambda:[updatePreference(last_viewed_prefs.get()), \
      prefAppList("media"), last_viewed_prefs.set("media")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")
   b_text_prefs = Button(l_frame, \
      text="Text Apps", command=lambda:[updatePreference(last_viewed_prefs.get()), \
      prefAppList("text"), last_viewed_prefs.set("text")],
      width=10, height=1, bg="#ffefcc", \
      font=smallFont, justify="center")


   b_go_back.pack(side="bottom", padx=20, pady=10)
   l_preference_page.pack(pady=35, ipadx=10, ipady=4)
   b_angry_prefs.pack(pady=4, ipadx=30)
   b_afraid_prefs.pack(pady=4, ipadx=30)
   b_happy_prefs.pack(pady=4, ipadx=30)
   b_neutral_prefs.pack(pady=4, ipadx=30)
   b_sad_prefs.pack(pady=4, ipadx=30)
   b_media_prefs.pack(pady=4, ipadx=30)
   b_text_prefs.pack(pady=4, ipadx=30)

   cur_widgets+=[b_go_back, b_angry_prefs, \
   b_afraid_prefs, b_happy_prefs, \
   b_neutral_prefs, b_sad_prefs, l_preference_page, \
   b_media_prefs, b_text_prefs]
   

def prefList(emotion):
   global cur_widgets, media_var, music_var, text_var,\
   diary_var, netflix_var, youtube_var

   for i in cur_widgets:
      if i not in [b_go_back, b_angry_prefs, \
      b_afraid_prefs, b_happy_prefs, \
      b_neutral_prefs, b_sad_prefs,\
      l_preference_page, b_media_prefs, b_text_prefs]:
         i.destroy()

   music_var = IntVar()
   if "music" in preference_dict[emotion]: music_var.set(1)
   youtube_var = IntVar()
   if "youtube" in preference_dict[emotion]: youtube_var.set(1)
   netflix_var = IntVar()
   if "netflix" in preference_dict[emotion]: netflix_var.set(1)
   diary_var = IntVar()
   if "diary" in preference_dict[emotion]: diary_var.set(1)
   text_var = IntVar()
   if "text" in preference_dict[emotion]: text_var.set(1)
   media_var = IntVar()
   if "media" in preference_dict[emotion]: media_var.set(1)


   c_music = Checkbutton(mm_frame, \
      text = "Listen to music", 
      variable = music_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20,
      bg="#ffefcc", font=smallFont, justify="center")
   c_music.pack(ipadx=10, ipady=2)
   c_youtube = Checkbutton(mm_frame, \
      text = "Watch youtube", 
      variable = youtube_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20,
      bg="#ffefcc", font=smallFont, justify="center")
   c_youtube.pack(ipadx=10, ipady=2)
   c_netflix = Checkbutton(mm_frame, \
      text = "Watch netflix", 
      variable = netflix_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20,
      bg="#ffefcc", font=smallFont, justify="center")
   c_netflix.pack(ipadx=10, ipady=2)
   c_diary = Checkbutton(mm_frame, \
      text = "Write a diary", 
      variable = diary_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20,
      bg="#ffefcc", font=smallFont, justify="center")
   c_diary.pack(ipadx=10, ipady=2)
   c_text = Checkbutton(mm_frame, \
      text = "Text a friend", 
      variable = text_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20,
      bg="#ffefcc", font=smallFont, justify="center")
   c_text.pack(ipadx=10, ipady=2)
   c_media = Checkbutton(mm_frame, \
      text = "Go on social media", 
      variable = media_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20,
      bg="#ffefcc", font=smallFont, justify="center")
   c_media.pack(ipadx=10, ipady=2)


   cur_widgets += [c_text, c_diary, c_netflix, \
   c_youtube, c_music, c_media]


def prefAppList(app):
   global cur_widgets, instagram_var, facebook_var, twitter_var,\
   snapchat_var, tiktok_var, reddit_var, whatsapp_var, telegram_var,\
   messenger_var

   for i in cur_widgets:
      if i not in [b_go_back, b_angry_prefs, \
      b_afraid_prefs, b_happy_prefs, \
      b_neutral_prefs, b_sad_prefs,\
      l_preference_page, b_media_prefs, b_text_prefs]:
         i.destroy()

   
   tiktok_var = IntVar()
   if tiktok_link in media_links: tiktok_var.set(1)
   reddit_var = IntVar()
   if reddit_link in media_links: reddit_var.set(1)
   twitter_var = IntVar()
   if twitter_link in media_links: twitter_var.set(1)

   whatsapp_var = IntVar()
   if whatsapp_link in text_links: whatsapp_var.set(1)
   telegram_var = IntVar()
   if telegram_link in text_links: telegram_var.set(1)
   messenger_var = IntVar()
   if messenger_link in text_links: messenger_var.set(1)

   if app=="media":
      instagram_var = IntVar()
      if instagram_link in media_links: instagram_var.set(1)
      facebook_var = IntVar()
      if facebook_link in media_links: facebook_var.set(1)
      snapchat_var = IntVar()
      if snapchat_link in media_links: snapchat_var.set(1)
   elif app=="text":
      instagram_var = IntVar()
      if instagram_link in text_links: instagram_var.set(1)
      facebook_var = IntVar()
      if facebook_link in text_links: facebook_var.set(1)
      snapchat_var = IntVar()
      if snapchat_link in text_links: snapchat_var.set(1)


   c_instagram = Checkbutton(mm_frame, \
      text = "Instagram", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = instagram_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_instagram.pack(ipadx=10, ipady=2)
   c_facebook = Checkbutton(mm_frame, \
      text = "facebook", bg="#ffefcc", \
      font=smallFont, justify="center", 
      variable = facebook_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_facebook.pack(ipadx=10, ipady=2)
   c_snapchat = Checkbutton(mm_frame, \
      text = "snapchat", bg="#ffefcc", \
      font=smallFont, justify="center",
      variable = snapchat_var, onvalue = 1, \
      offvalue = 0, height=2, width = 20)
   c_snapchat.pack(ipadx=10, ipady=2)

   if app=="media":
      c_twitter = Checkbutton(mm_frame, \
         text = "twitter", bg="#ffefcc", \
         font=smallFont, justify="center",
         variable = twitter_var, onvalue = 1, \
         offvalue = 0, height=2, width = 20)
      c_twitter.pack(ipadx=10, ipady=2)
      c_tiktok = Checkbutton(mm_frame, \
         text = "tiktok", bg="#ffefcc", \
         font=smallFont, justify="center",
         variable = tiktok_var, onvalue = 1, \
         offvalue = 0, height=2, width = 20)
      c_tiktok.pack(ipadx=10, ipady=2)
      c_reddit = Checkbutton(mm_frame, \
         text = "reddit", bg="#ffefcc", \
         font=smallFont, justify="center",
         variable = reddit_var, onvalue = 1, \
         offvalue = 0, height=2, width = 20)
      c_reddit.pack(ipadx=10, ipady=2)

      cur_widgets+=[c_twitter, c_tiktok, c_reddit]

   elif app=="text":
      c_whatsapp = Checkbutton(mm_frame, \
         text = "whatsapp", bg="#ffefcc", \
         font=smallFont, justify="center",
         variable = whatsapp_var, onvalue = 1, \
         offvalue = 0, height=2, width = 20)
      c_whatsapp.pack(ipadx=10, ipady=2)
      c_telegram = Checkbutton(mm_frame, \
         text = "telegram", bg="#ffefcc", \
         font=smallFont, justify="center",
         variable = telegram_var, onvalue = 1, \
         offvalue = 0, height=2, width = 20)
      c_telegram.pack(ipadx=10, ipady=2)
      c_messenger = Checkbutton(mm_frame, \
         text = "messenger", bg="#ffefcc", \
         font=smallFont, justify="center",
         variable = messenger_var, onvalue = 1, \
         offvalue = 0, height=2, width = 20)
      c_messenger.pack(ipadx=10, ipady=2)

      cur_widgets+=[c_whatsapp, c_telegram, c_messenger]


   cur_widgets += [c_instagram, c_facebook, c_snapchat]


def updatePreferenceFile():
   path=os.path.dirname(__file__).replace('\\', '/')+"/profiles/"
   path+=current_user

   if os.path.exists(path+"/preferences"):
      os.remove(path+"/preferences")

   outfile = open(path+"/preferences",'wb')
   pickle.dump(preference_dict, outfile)
   outfile.close()


def updateData():
   path=os.path.dirname(__file__).replace('\\', '/')+"/profiles/"
   path+=current_user

   if os.path.exists(path+"/data"):
      os.remove(path+"/data")

   outfile = open(path+"/data",'wb')
   pickle.dump(data, outfile)
   outfile.close()

def dataScreen():
   global cur_widgets
   clearMain()

   d={}
   for i in data[1:]:
      if i not in d:
         d[i]=0
      d[i]+=1

   lables=d.keys()
   freq=[]
   for i in lables:
       freq.append(d[i])


   fig = matplotlib.figure.Figure(figsize=(7,7))

   fig.patch.set_facecolor(color)

   ax = fig.add_subplot(111)

   ax.pie(freq) 
   ax.legend(lables)

   circle=matplotlib.patches.Circle( (0,0), 0.6, color=color, ec="white", lw=2.0)
   circle1=matplotlib.patches.Circle( (0,0), 1.0, fill=False, ec="white", lw=2.0)
   circle2=matplotlib.patches.Circle( (0,0), 1.1, fill=False, ec="white", lw=2.0)
   ax.add_artist(circle)
   ax.add_artist(circle1)
   ax.add_artist(circle2)

   chart = FigureCanvasTkAgg(fig, master=r_frame)
   chart.get_tk_widget().pack(padx=50, pady=25)
   root.config(bg=color)

   b_back = Button(l_frame, text="Go back", \
      command=lambda:[homeScreen(), chart.get_tk_widget().destroy()], \
      bg="#ffefcc", font=font, justify="center")
   b_back.pack(side="bottom", ipadx=10, ipady=2, padx=60, pady=20)

   string=""
   for key, value in d.items():
      string+='\n'+key+' : '+str(value)
   string+='\n'

   l_data_title = Label(l_frame, \
      text=f"Entries from\n{data[0]} to {date.today()}",
      bg="#ffefcc", font=font, justify="center")
   l_data = Label(l_frame, \
      text=string, width=20,
      bg="#ffefcc", font=font, justify="left")

   l_data_title.pack(ipadx=10, ipady=10, padx=30, pady=50)
   l_data.pack(ipadx=10, ipady=10, padx=30, pady=50)

   cur_widgets+=[b_back, l_data, l_data_title]





########################################################
# run
########################################################

# manualScreen()
welcomeScreen()
root.mainloop()