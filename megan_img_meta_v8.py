#-------------------------------------------------------------------------------
# Name:        metadata_imgV8
#
# Purpose:      To collect metadata about images including their ID, file name and extension, title, owner, and licence type, then write data to a CSV file so that it may be imported to a database
# Author:      Megan
# Sources:      http://stackoverflow.com/questions/21043387/how-do-you-add-input-from-user-into-list-in-python
#               http://stackoverflow.com/questions/5278122/checking-if-all-elements-in-a-list-are-unique
#               http://stackoverflow.com/questions/1549641/how-to-capitalize-the-first-letter-of-each-word-in-a-string-python
#
# Created:     28/07/2014
# Copyright:   (c) Megan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

#import GUI library
from tkinter import *

#for Python V3 you must explicitely load the messagebox
import tkinter.messagebox

#create the Image class incorporating instance variables and methods
class Image:
    def __init__(self, image_id, filename, file_ext, title, owner_fn, owner_sn, licence):
        self.image_id = image_id
        self.filename = filename
        self.file_ext = file_ext
        self.title = title
        self.owner_fn = owner_fn
        self.owner_sn = owner_sn
        self.licence = licence

    def get_id(self):

        return self.image_id

    def get_filename(self):
        return self.filename

    def get_file_ext(self):
        return self.file_ext

    def get_title(self):
        return self.title

    def get_owner_fn(self):
        return self.owner_fn

    def get_owner_sn(self):
        return self.owner_sn

    def get_licence(self):
        return self.licence

#create the GUI interface
class GUI:
    #init should return None, only self
    def __init__(self):

        window = Tk()
        window.title("Metadata Entry for Images")
        #setting root window and size
        window.minsize(width=600, height=400)

        #INITIALIZATION VARIABLES
        #this variable stores whether the data has been validated or not
        self.ready_to_write = False
        self.recordlist = []

        self.licence_init = ""

        #creating label and field variables in GUI
        image_id_label = Label(window, text='Enter image ID:')
        image_id_label.pack() #.pack() places the component in the window
        self.image_id_field = Entry(window)
        self.image_id_field.pack()

        file_ext_label = Label(window, text = 'Enter filename and select extension:')
        file_ext_label.pack()
        self.filename_field = Entry(window)
        self.filename_field.pack()

        self.file_ext = StringVar()
        self.ext_init= "Select extension of image"
        self.file_ext.set(self.ext_init)
        # image formats in list decided by what majority of browsers can support
        #http://en.wikipedia.org/wiki/Comparison_of_web_browsers#Image_format_support
        extensions = [".JPEG", ".GIF", ".PNG"]
        OptionMenu(window, self.file_ext, *extensions).pack()

        title_label = Label(window, text = 'Enter title:')
        title_label.pack()
        self.title_field = Entry(window)
        self.title_field.pack()

        owner_fn_label = Label(window, text = "Enter owner's first name:")
        owner_fn_label.pack()
        self.owner_fn_field = Entry(window)
        self.owner_fn_field.pack()

        owner_sn_label = Label(window, text = "Enter owner's surname:")
        owner_sn_label.pack()
        self.owner_sn_field = Entry(window)
        self.owner_sn_field.pack()

        licence_label = Label(window, text = 'Select licence type:')
        licence_label.pack()
        self.licence = StringVar()
        self.licence_init = "Select licence type"
        self.licence.set(self.licence_init)
        attribution = ["Attribution alone","Attribution + NoDerivatives","Attribution + ShareAlike", "Attribution + Noncommercial", "Attribution + Noncommercial + NoDerivatives", "Attribution + Noncommercial + ShareAlike"]
        #OptionMenu() only allows one variable to be chosen as opposed to MenuButton(),  it is also much clearer and straightforward (seen in V1)
        OptionMenu(window, self.licence, *attribution).pack()

        #creates a button. The command function is run when the button is pressed
        validate_label = Label(window, text='Press to validate:')
        validate_button = Button(window, text='Submit', command=self.doSubmit)

        csv_label = Label(window, text='Convert Record to csv')
        csv_button = Button(window, text='write to csv', command=self.writetocsv)

        validate_label.pack()
        validate_button.pack()

        csv_label.pack()
        csv_button.pack()

        #waiting for user input - event driven program
        window.mainloop()

    def doSubmit(self):

        #test uniqueness of each school name entered u
        noduplicate = True;
        for record in self.recordlist:
            if self.image_id_field.get() == record.get_id():
                noduplicate= False
                tkinter.messagebox.showwarning('Warning!','Duplicate image ID');
                print('Please enter image ID again');

        if noduplicate == True:
            if len(self.image_id_field.get()) <1 or len(self.filename_field.get()) <1 or self.file_ext.get() == (self.ext_init) or len(self.title_field.get()) <1 or len(self.owner_fn_field.get()) <1 or len(self.owner_sn_field.get()) <1 or self.licence.get() == (self.licence_init) :
                tkinter.messagebox.showwarning('Warning!','Please enter a value for all fields')
            else:
                try:
                    validated_integer = int(self.image_id_field.get())
                    self.recordlist.append(Image(self.image_id_field.get(), self.filename_field.get(), self.file_ext.get(), self.title_field.get(), self.owner_fn_field.get(), self.owner_sn_field.get(), self.licence.get()))


                    self.ready_to_write= True
                    tkinter.messagebox.showinfo('Notice','Submission Successful')

                    self.image_id_field.delete(0, END) #command to clear field
                    self.filename_field.delete(0, END)
                    self.file_ext.set(self.ext_init)
                    self.title_field.delete(0, END)
                    self.owner_fn_field.delete(0, END)
                    self.owner_sn_field.delete(0, END)
                    self.licence.set(self.licence_init)


                except:
                    tkinter.messagebox.showwarning('Warning!','Please enter numeric data for image ID')
                    print('Please enter numeric data for image ID')
    def writetocsv(self):
        #this is the callback method for the 'write to csv' button
        import csv
        file_name = 'database.txt'

        if self.ready_to_write: #cheacks data has been validated
            #I have decided to write instead of append because when appending, duplicate IDs and records occur
            ofile = open(file_name, 'w')
            writer = csv.writer(ofile, delimiter=',')


            for record in self.recordlist:
                #for filenames, it is convention to have no spaces, this takes out the spaces
                filename = record.get_filename().replace(" ", "")
                #this joins the filename and extension back together i.e. flowers.JPEG
                filename = filename + record.get_file_ext()
                #Capitalises the owner's first name when written to csv file
                #Used this code instead of title() as title has some inconsistencies such as when "McDonald" is typed. "Mcdonald" is outputted.
                #This code fixes this by splitting the words, initial-capitalising the words and then rejoining the words, which changes the white space separating the words into a single white space.
                # e.g. if "hi                           megan" was someone's name, it  would output "hi megan"
                owner_fn = ' '.join(word[0].upper() + word[1:] for word in record.get_owner_fn().split())
                #when comma or speech marks are entered, extra speech marks are added. replace() prevents this from happening
                owner_fn = owner_fn.replace("," , "") and owner_fn.replace("'", "") and owner_fn.replace('"', '') and owner_fn.replace("," , "")

                owner_sn = ' '.join(word[0].upper() + word[1:] for word in record.get_owner_sn().split())
                owner_sn = owner_sn.replace("," , "") and owner_sn.replace("'", "")

                title = ' '.join(word[0].upper() + word[1:] for word in record.get_title().split())
                title = title.replace("," , "") and title.replace("'", "") and title.replace('"', '')
                #writes the input into a csv file. Listing the input separates the
                writer.writerow([record.get_id(),filename, title, owner_fn, owner_sn, record.get_licence()])
            #In v7, when the user writes to csv without validating, the error message is shown as well as the 'File Generated Successfully' message.
            #Moving it here means that the 'File Generated Successfully' message will only be activated when everything is validated.
            tkinter.messagebox.showinfo('Notice',file_name+' File Generated Successfully')
            # closes the output file
            ofile.close()
        else:
            tkinter.messagebox.showwarning('Error!', 'You need to Validate your data')

        self.ready_to_write= False


#initialises the programme
GUI()
