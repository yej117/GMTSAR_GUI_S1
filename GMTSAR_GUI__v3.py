#!/usr/bin/python3
# version: 2019-03-25 Yi-Jie Yang (EJ)
##########################################################
######################### Import #########################
##########################################################

import os
import glob
import datetime
import shutil

# [terminal] sudo apt-get install python3-tk
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as fdialog
import tkinter.messagebox as tkMessageBox

##########################################################
################## Create GUI interface ##################
##########################################################
# Create a class for the main GUI setting
class Control(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkFont.Font(family='Helvetica',
        size=18, weight="bold", slant="italic")
        self.geometry("760x400")
        self.title("GMTSAR for Sentinel-1 SAR processing")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Info, Step0, Step1, Step2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Info")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.Main()


class Info(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.Main()

    def Main(self):
        # Define some functions for uses in this section
        def Get_pwd():
            dir=os.getcwd()
            #self.Dir_proc_tmp.set(dir)
            edTxt[0].insert(0,dir)

        #def Tmp1():
        #    dir='/home/yej/main/Research/Data/Sentinel-1/Taiwan/North/Ascending'
        #    edTxt[1].insert(0,dir)

        #def Tmp2():
        #    dir='/home/yej/main/Research/Data/Sentinel-1/POD'
        #    edTxt[2].insert(0,dir)

        #def Tmp3():
        #    dir='/home/yej/main/Research/Data/DEM/TW_dem_30m.grd'
        #    edTxt[3].insert(0,dir)

        #def Tmp4():
        #    dir='/home/yej/main/Research/Data/Sentinel-1/batch_tops.config'
        #    edTxt[4].insert(0,dir)

        #def Tmp5():
        #    dir='/home/yej/main/Research/Data/Sentinel-1/s1a-aux-cal.xml'
        #    edTxt[5].insert(0,dir)

        def browse(index):
            if index == 0:
                dir=fdialog.askdirectory(
                    initialdir=os.getcwd(),
                    title="Select a directory")
            elif index == 1 or index == 2:
                dir=fdialog.askdirectory(
                    initialdir=os.getcwd(),
                    #initialdir="/home",
                    title="Select a directory")
            else:
                dir=fdialog.askopenfilename(
                    initialdir=os.getcwd(),
                    #initialdir="/home",
                    title="Select a file")
            edTxt[index].insert(0,dir)

        def Save():
            # Save some variables
            global Dir_proc, Dir_image, Dir_EOF, path_dem, path_config, path_s1a_cal
            global Not_s1a_cal_aux
            Dir_proc=self.Dir_proc_tmp.get()
            Dir_image=self.Dir_image_tmp.get()
            Dir_EOF=self.Dir_EOF_tmp.get()
            path_dem=self.path_dem_tmp.get()
            path_config=self.path_config_tmp.get()
            Not_s1a_cal_aux=self.Not_s1a_cal_aux_tmp.get()
            if Not_s1a_cal_aux == 0:
                path_s1a_cal=self.path_s1a_cal_tmp.get()

            # Change to Step0 tab
            self.controller.show_frame("Step0")

        # Labels for title / information
        label=tk.Label(self,
            text='Basic Information',
            font='Helvetica 12 bold italic')
        label.grid(row=0, column=0)

        info=[  'Processing directory ',
                'Directory for Sentinel-1 data ',
                'Directory for POD precise orbit ephemerides (EOF) ',
                'Select the dem.grd file ',
                'Select the tops.config file ',
                'Select the s1a-cal-aux.xml file ']

        for i in range (len(info)):
            label=tk.Label(self,
                text=info[i])
            label.grid(row=2*i+1,column=0, sticky='w')
            label.config(fg='#000000')

        # Variables for temp. save the info.
        self.Dir_proc_tmp=tk.StringVar()
        self.Dir_image_tmp=tk.StringVar()
        self.Dir_EOF_tmp=tk.StringVar()
        self.path_dem_tmp=tk.StringVar()
        self.path_config_tmp=tk.StringVar()
        self.path_s1a_cal_tmp=tk.StringVar()

        # Entries for typing the information ---Save---> tmp variables
        edTxt=[ tk.Entry(self, textvariable=self.Dir_proc_tmp, width=50, borderwidth=2),
                tk.Entry(self, textvariable=self.Dir_image_tmp, width=50, borderwidth=2),
                tk.Entry(self, textvariable=self.Dir_EOF_tmp, width=50, borderwidth=2),
                tk.Entry(self, textvariable=self.path_dem_tmp, width=50, borderwidth=2),
                tk.Entry(self, textvariable=self.path_config_tmp, width=50, borderwidth=2),
                tk.Entry(self, textvariable=self.path_s1a_cal_tmp, width=50, borderwidth=2),]


        for i in range (len(info)):
            edTxt[i].grid(row=2*i+2,column=0)

        # Buttons for Get_pwd / Browsing...
        # Get pwd
        btn_pwd=tk.Button(self, text="Get pwd", command=Get_pwd)
        btn_pwd.grid(row=2, column=2)

        # tmp items for get dir.
        #btn_tmp=tk.Button(self, text="Tmp", command=Tmp1)
        #btn_tmp.grid(row=4, column=2)

        #btn_tmp=tk.Button(self, text="Tmp", command=Tmp2)
        #btn_tmp.grid(row=6, column=2)

        #btn_tmp=tk.Button(self, text="Tmp", command=Tmp3)
        #btn_tmp.grid(row=8, column=2)

        #btn_tmp=tk.Button(self, text="Tmp", command=Tmp4)
        #btn_tmp.grid(row=10, column=2)

        #btn_tmp=tk.Button(self, text="Tmp", command=Tmp5)
        #btn_tmp.grid(row=12, column=2)


        # buttons for browsing dir / file
        btn=[   tk.Button(self, text="Browse", command=lambda *args:browse(0)),
                tk.Button(self, text="Browse", command=lambda *args:browse(1)),
                tk.Button(self, text="Browse", command=lambda *args:browse(2)),
                tk.Button(self, text="Browse", command=lambda *args:browse(3)),
                tk.Button(self, text="Browse", command=lambda *args:browse(4)),
                tk.Button(self, text="Browse", command=lambda *args:browse(5))]

        for i in range (len(info)):
            btn[i].grid(row=2*i+2, column=1)

        # Checkbutton for s1a-cal-aux
        self.Not_s1a_cal_aux_tmp=tk.IntVar()
        rbtn=tk.Checkbutton(self, text="Not use.",
            variable=self.Not_s1a_cal_aux_tmp, onvalue=1, offvalue=0)
        rbtn.grid(row=12, column=3)

        # Button for Next step
        btn=tk.Button(self, text=" Next >",command=lambda:Save())
        btn.grid(row=13, column=4)


class Step0(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


    def Main(self):
        # Define some functions for uses in this section
        def Save():
            global data_date, polar, iw

            data_date=[]
            s=Lb.curselection()
            for i in range (len(s)):
                #tmp=Lb.get(Lb.curselection()[i])
                data_date.append(Lb.get(Lb.curselection()[i]))
            data_date.sort()

            polar=self.polar_tmp[self.polar_index_tmp.get()]
            iw=self.iw_tmp[self.iw_index_tmp.get()]

            # Change to Step1 tab
            self.controller.show_frame("Step1")

        # Labels for title / other information
        # Step 0
        label=tk.Label(self,
            text='Step 0. Select data date',
            font='Helvetica 12 bold italic')
        label.grid(row=0, column=0)

        # other info.
        label=tk.Label(self,
            text='Other information',
            font='Helvetica 10 bold italic')
        label.grid(row=1, column=1, sticky='e')

        # Information for create a date listbox
        os.chdir(Dir_image)
        image_list=glob.glob('S1*SLC*')
        date_list=[]
        for i in range (len(image_list)):
            tmp=image_list[i].split('.')
            if tmp[1] == 'SAFE' or tmp[1] == 'safe':
                tmp=image_list[i]
                tmp_index=tmp.find('T')
                date_list.append(tmp[tmp_index-8:tmp_index])
        date_list.sort()

        # Listbox for choosing data date
        Lb=tk.Listbox(self, width=14, selectmode='multiple')
        for i in range (len(date_list)):
            Lb.insert(i,date_list[i])
        Lb.grid(row=1,column=0,rowspan=10)

        # Radiobutton for other information: polarization / sub-swath
        # polarization: polar
        frame=tk.LabelFrame(self, text='Polarization')
        self.polar_tmp=['vv','vh','hv','hh']
        self.polar_index_tmp=tk.IntVar()
        rb=[]
        for i in range (len(self.polar_tmp)):
            rb.append(tk.Radiobutton(frame,
                text=self.polar_tmp[i],
                variable=self.polar_index_tmp,
                value=i))
            rb[i].pack()
        frame.grid(row=2, column=1, sticky='nw', rowspan=8, columnspan=2)

        # sub-swath
        frame=tk.LabelFrame(self, text='Sub-swath')
        self.iw_tmp=['iw1','iw2','iw3']
        self.iw_index_tmp=tk.IntVar()
        rb=[]
        for i in range (len(self.iw_tmp)):
            rb.append(tk.Radiobutton(frame,
                text=self.iw_tmp[i],
                variable=self.iw_index_tmp,
                value=i))
            rb[i].pack()
        frame.grid(row=2, column=3, sticky='nw', rowspan=8, columnspan=2)

        # Button for Pevious / Next steps
        btn1=tk.Button(self, text="< Previous ",
            command=lambda: self.controller.show_frame("Info"))
        btn2=tk.Button(self, text=" Next >",
            command=lambda:Save())
        btn1.grid(row=13, column=3)
        btn2.grid(row=13, column=4)


class Step1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def Main(self):
        def Create():
            # make the buttons disabled
            edTxt1.config(state="readonly")
            edTxt2.config(state="readonly")
            rb1.config(state="disabled")
            rb2.config(state="disabled")
            btn1.config(state="disabled")
            btn2.config(state="normal")
            btn_create.config(state="disabled")

            # get some needed variables
            global ESD_YN, Master_date, prep_sh
            global Num_data, date_list
            ESD_YN=self.ESD_YN_tmp.get()
            Master_date=self.Master_data_tmp.get()
            prep_sh=self.prep_sh_tmp.get()
            Num_data=len(data_date)

            # Link the data are going to use & create the *.sh file
            # .: batch_tops.config
            # raw / raw_orig: *_manifest, *.xml, *.tiff, *.EOF, [, s1a-aux-cal], dem.grd
            # topo: dem.grd
            os.chdir(Dir_proc)

            # config file
            f=open(path_config,'r')
            content=f.read()
            f.close()

            ## Replace the target string
            content=content.replace('master_image = ',
                'master_image = S1_'+Master_date+'_ALL_F'+iw[-1])

            ## Write the file out again
            g=open('batch_tops.config', 'w')
            g.write(content)
            g.close()

            # raw / raw_orig
            g=open(prep_sh,'w',encoding='UTF-8')
            g.write('#!/bin/csh -f\n'+'cd raw\n\n')
            os.makedirs('raw')

            # variables for recording data
            manifest_list=[]
            xml_list=[]
            EOF_list=[]
            date_list=[] # Format: date

            ## Link: *_manifest, *.xml [, s1a-aux-cal]
            if Not_s1a_cal_aux == 0:
                os.makedirs('raw_orig')

            os.chdir('raw')
            for i in range (Num_data):
                info=Dir_image+'/*'+data_date[i]+'*'

                if Not_s1a_cal_aux == 0:
                    os.chdir('../raw_orig')

                else:
                    os.chdir('../raw')

                # manifest
                tmp=glob.glob(info+'/manifest.safe')
                os.link(tmp[0],data_date[i]+'_manifest.safe')
                manifest_list.append(data_date[i]+'_manifest.safe')

                # xml
                tmp1=glob.glob(info+'/annotation/*'+iw+'*'+polar+'*.xml')
                tmp2=tmp1[0].split('/')
                os.link(tmp1[0],tmp2[-1])
                xml_list.append(tmp2[-1])

                if Not_s1a_cal_aux == 0:
                    # write *.sh file
                    g.write("awk 'NR>1 {print $0}' < ../raw_orig/"
                        + manifest_list[i]
                        + ' > tmp_file\n'
                        + 'cat ../raw_orig/'
                        + xml_list[i]
                        + ' tmp_file ../raw_orig/s1a-aux-cal.xml > ./'
                        + xml_list[i] +'\n')

                # tiff
                os.chdir('../raw')
                tmp1=glob.glob(info+'/measurement/*'+iw+'*'+polar+'*'+'.tiff')
                tmp2=tmp1[0].split('/')
                tmp2=tmp2[-1]
                os.link(tmp1[0],tmp2)

	            # *.EOF
                # S1AB is for someone puts all the POD in the same directory, and avoid choosing the wrong satellite POD file.
                S1AB=glob.glob(info)
                S1AB=S1AB[0].split('/')
                S1AB=S1AB[-1]
                S1AB=S1AB[:3]
                info=data_date[i]
                info=datetime.date(int(info[0:4]),int(info[4:6]),int(info[6:8]))
                date_list.append(info)
                info1=info-datetime.timedelta(1)
                info1=str(info1)
                info1=eval("info1[0:4]+info1[5:7]+info1[8:10]")
                info2=info+datetime.timedelta(1)
                info2=str(info2)
                info2=eval("info2[0:4]+info2[5:7]+info2[8:10]")
                tmp1=Dir_EOF+'/'+S1AB+'*'+info1+'*'+info2+'*'
                tmp1=glob.glob(tmp1)
                tmp1=str(tmp1[0])
                tmp2=tmp1.split('/')
                os.link(tmp1,tmp2[-1])
                EOF_list.append(tmp2[-1])


            if Not_s1a_cal_aux == 0:
                os.chdir('../raw_orig')
                # s1a-aux-cal.xml
                #   - Link to ./raw_orig ('.')
                os.link(path_s1a_cal,'s1a-aux-cal.xml')

            # Link dem.grd => raw & topo
            os.chdir('..')
            os.makedirs('topo')
            os.chdir('topo')
            os.link(path_dem,'dem.grd')

            os.chdir('../raw')
            os.link(path_dem,'dem.grd')
            os.chdir('..')

            # write *.sh file
            if ESD_YN == 1:
                g.write('preproc_batch_tops_esd.csh data.in dem.grd 1\n')
                g.write('preproc_batch_tops_esd.csh data.in dem.grd 2\n')
            elif ESD_YN==0:
	            g.write('preproc_batch_tops.csh data.in dem.grd 1\n')
	            g.write('preproc_batch_tops.csh data.in dem.grd 2\n')
            g.close()


            # Create data.in file for preprocessing
            os.chdir('raw')
            g=open('data.in','w')
            for i in range (Num_data):
                info=xml_list[i].split('.')
                tmp=info[0]+':'+EOF_list[i]
                g.write(tmp+'\n')
            g.close()
            os.chdir('..')

        def Save():
            #print(self.prep_sh_tmp.get())
            self.controller.show_frame("Step2")

        # Labels for title
        label=tk.Label(self,
            text='Step 1. Preprocessing',
            font='Helvetica 12 bold italic')
        label.grid(row=0, column=0, sticky='w')

        # Dispaly the data date
        if len(data_date) == 0:
            label=tk.Label(self, text='Please choose the data date in previous page!!')
            label.grid(row=1, column=1, sticky='w')
        else:
            frame=tk.LabelFrame(self,text='Chosen Date')
            for i in range (len(data_date)):
                label=tk.Label(frame, text=data_date[i])
                label.pack()
            frame.grid(row=1, column=0, rowspan=len(data_date))

        # Label / Radiobutton for information
        label=tk.Label(self, text='Do you want to use Enhanced Spectral diversity (ESD)?')
        label.grid(row=2, column=2, columnspan=5, sticky='w')

        self.ESD_YN_tmp=tk.IntVar()
        rb1=tk.Radiobutton(self, text='yes',
                variable=self.ESD_YN_tmp, value=1)
        rb1.grid(row=3, column=2, sticky='w')
        rb2=tk.Radiobutton(self, text='no',
                variable=self.ESD_YN_tmp, value=0)
        rb2.grid(row=3, column=3, sticky='w')

        # Label / entry for Master data
        label=tk.Label(self, text='Master data fo alignment.')
        label.grid(row=4, column=2, columnspan=5, sticky='w')

        self.Master_data_tmp=tk.StringVar()
        edTxt1=tk.Entry(self, textvariable=self.Master_data_tmp, width=20, borderwidth=2)
        edTxt1.insert(0,data_date[0])
        edTxt1.grid(row=5,column=2, columnspan=5)

        # Label / entry for output file name
        label=tk.Label(self, text='File name for step 1.')
        label.grid(row=6, column=2, columnspan=5, sticky='w')

        self.prep_sh_tmp=tk.StringVar()
        edTxt2=tk.Entry(self, textvariable=self.prep_sh_tmp, width=20, borderwidth=2)
        edTxt2.insert(0,'01_prep.sh')
        edTxt2.grid(row=7,column=2, columnspan=5)

        # Button for Pevious / Next steps / create *.csh file
        btn1=tk.Button(self, text="< Previous ",
            command=lambda: self.controller.show_frame("Step0"))
        btn2=tk.Button(self, text=" Next >",
            state="disabled",
            command=lambda:Save())
        btn1.grid(row=20, column=12)
        btn2.grid(row=20, column=13)

        btn_create=tk.Button(self, text="Create", command=Create)
        btn_create.grid(row=8, column=6, sticky='e')


class Step2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


    def Main(self):
        def Create():
            # make the buttons disabled
            scale1.config(state="disabled")
            scale2.config(state="disabled")
            edTxt.config(state="readonly")
            btn1.config(state="disabled")
            btn2.config(state="normal")
            btn_create.config(state="disabled")

            # variables
            global time_delta_min, time_delta_max
            global proc_sh
            time_delta_min=self.time_delta_min_tmp.get()
            time_delta_max=self.time_delta_max_tmp.get()
            proc_sh=self.proc_sh_tmp.get()

            # Create intf.in for DInSAR pairs
            g=open('intf.in','w')
            time_delta_max=datetime.timedelta(days=time_delta_max)
            time_delta_min=datetime.timedelta(days=time_delta_min)
            for i in range (Num_data):
                for j in range (i+1,Num_data):
                    delta=date_list[j]-date_list[i]
                    if time_delta_min <= delta <= time_delta_max:
                        g.write('S1_'+data_date[i]+'_ALL_F'+iw[-1]
                            +':S1_'+data_date[j]+'_ALL_F'+iw[-1]+'\n')
            g.close()

            # Create proc.sh
            g=open(proc_sh,'w')
            g.write('#!/bin/csh -f\n')
            g.write('\nintf_tops.csh intf.in batch_tops.config\n')
            g.close()

        #def Confirm():
        #    tkMessageBox.askokcancel("Confirm", "Go to next step?")
        #    Create()

        #def Save():
        #    self.controller.show_frame("Execute")

        def Done():
            # close the GUI interface
            self.quit()

        # Labels for title
        label=tk.Label(self,
            text='Step 2. Processing (DInSAR)',
            font='Helvetica 12 bold italic')
        label.grid(row=0, column=0)

        # Scale for choosing the day interval for interferograms
        self.time_delta_min_tmp=tk.IntVar()
        self.time_delta_max_tmp=tk.IntVar()

        scale1=tk.Scale(self,
            variable=self.time_delta_min_tmp,
            label='min. day interval',
            from_=0, to=300, resolution=6,
            orient='horizontal',
            length=200)
        scale1.grid(row=1, column=0, rowspan=3)

        scale2=tk.Scale(self,
            variable=self.time_delta_max_tmp,
            label='Max. day interval',
            from_=0, to=300, resolution=6,
            orient='horizontal',
            length=200)
        scale2.grid(row=4, column=0, rowspan=3)

        # Label / entry for output file name
        label=tk.Label(self, text='File name for step 1.')
        label.grid(row=1, column=4, sticky='w')

        self.proc_sh_tmp=tk.StringVar()
        edTxt=tk.Entry(self, textvariable=self.proc_sh_tmp, width=20, borderwidth=2)
        edTxt.insert(0,'02_proc.sh')
        edTxt.grid(row=2,column=4)

        # Button for Pevious / Next steps / create *.csh file
        btn1=tk.Button(self, text="< Previous ",
            command=lambda: self.controller.show_frame("Step1"))
        btn2=tk.Button(self, text="Done",
            state="disabled",
            command=lambda:Done())
        btn1.grid(row=10, column=15)
        btn2.grid(row=10, column=16)

        btn_create=tk.Button(self, text="Create", command=Create)
        btn_create.grid(row=3, column=10, sticky='e')

if __name__ == "__main__":
    app=Control()
    app.mainloop()
