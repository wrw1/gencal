#!/usr/bin/env python3.6
import os.path
from platform import system
import tkinter as tk
from tkinter import TRUE, END, VERTICAL, TkVersion
import globals as G
from globals import resource_path
from ScrollableFrame import VerticalScrolledFrame
from MainWindow import Window

#-------------------------------------------------------------
#   Start of GUI setup
mw = tk.Tk()
mw.geometry("800x600")
app = Window(mw)

# set application icon

icondir = os.path.join(os.path.dirname(__file__), 'Icons')
if system() == 'Windows':
	iconfile = resource_path(os.path.join(icondir, 'gencal.ico'))
	mw.wm_iconbitmap(default=iconfile)
elif TkVersion >= 8.5:
	ext = '.png' if TkVersion >= 8.6 else '.gif'
	iconfiles = [resource_path(os.path.join(icondir, 'gencal_%d%s' % (size, ext)))
				 for size in (16, 32, 48)]
	icons = [tk.PhotoImage(file=iconfile) for iconfile in iconfiles]
	mw.wm_iconphoto(True, *icons)


#---- Global variables and there defaults
preamble = [';make sure laser is off', 'M05 S0',
		';use absolute prgraming XY', 'G90',
		';set dwell to 0', 'G4 P0']
postamble = [';set dwell to 0', 'G4 P0',
		 ';make sure laser is off', 'M05 S0',
		 ';return to home position', 'G0 X0 Y0']
#-- Common
units='G21'
kerfsize=tk.StringVar()
kerfsize.set('.2')
commGap=tk.StringVar()
commGap.set('5')

#-- Cut
incCut=tk.IntVar()
cutPower=tk.StringVar()
cutPower.set('1000')
cutFeed=tk.StringVar()
cutFeed.set('100')
cutXsize=tk.StringVar()
cutXsize.set('10')
cutYsize=tk.StringVar()
cutYsize.set('20')
cutPasses=tk.StringVar()
cutPasses.set('1')
#-- Engrave
incEngrave=tk.IntVar()
engraveFeed=tk.StringVar()
engraveFeed.set('1500')
engraveMaxP=tk.StringVar()
engraveMaxP.set('1000')
engraveMinP=tk.StringVar()
engraveMinP.set('1')
engraveNumPlev=tk.StringVar()
engraveNumPlev.set('256')
engraveDistI=tk.StringVar()
engraveDistI.set('0.5')
engraveBarLen=''
engraveBarWidth=tk.StringVar()
engraveBarWidth.set('10')
engraveIdxPwr=tk.StringVar()
engraveIdxPwr.set('200')
engraveIdxMax=tk.StringVar()
engraveIdxMax.set('5')

#-- Picture
incPicture=tk.IntVar()
picPower=tk.StringVar()
picPower.set('80')
picFeed=tk.StringVar()
picFeed.set('100')
picTestsep=tk.StringVar()
picTestsep.set('1')
picSDsep=tk.StringVar()
picSDsep.set('.3')
picSDnum=tk.StringVar()
picSDnum.set('10')
picDDsep=tk.StringVar()
picDDsep.set('.3')
picDDnum=tk.StringVar()
picDDnum.set('10')
picDashWidth=tk.StringVar()
picDashWidth.set('3')
picDashsep=tk.StringVar()
picDashsep.set('.3')
picIncDithered=tk.IntVar()
picDitheredFN=tk.StringVar()
picDitheredFN.set('dither_img.nc')

#----- App widgets-------------------------------
main_frm = tk.Frame(app)
main_frm.pack(fill='both', expand=TRUE) #New Frame

#divide main_frm into 2 frames (right side and left side)
rs_frm = tk.Frame(main_frm)
rs_frm.pack(side='right', anchor='ne',fill='both', expand=TRUE)
ls_frm=VerticalScrolledFrame(main_frm)
ls_frm.pack(side='left', anchor='nw', fill='y', expand=TRUE)

#---------Right Side Frame Widgets------------------
#--- Generate Gcode button
rs_gen_but = tk.Button(rs_frm, text="Generate Gcode",
				 bg="lime green")
rs_gen_but.pack()
rs_lstfrm = tk.Frame(rs_frm)
rs_lstfrm.pack(fill='both', expand=TRUE)
rs_lstbox = tk.Listbox(rs_lstfrm, width=60)
rs_lstbox.pack(side='left',fill='both', expand=TRUE)
rs_lstbox_scb = tk.Scrollbar(rs_lstfrm, orient=VERTICAL)
rs_lstbox_scb.config(command=rs_lstbox.yview)
rs_lstbox_scb.pack(side='right', fill='y')
rs_lstbox.config(yscrollcommand=rs_lstbox_scb.set)

#---------Left Side Frame Widgets------------------
#--- Common
ls_comm_lab = tk.Label(ls_frm.interior, text="Common")
ls_comm_lab.pack()
ls_comm_unitfrm = tk.Frame(ls_frm.interior)
ls_comm_unitfrm.pack()
ls_comm_selunitLab = tk.Label(ls_comm_unitfrm, text="Toggle Units")
ls_comm_selunitLab.pack(side = 'left', fill='x', expand=TRUE)
ls_comm_selunitBut = tk.Button(ls_comm_unitfrm, text="mm")
ls_comm_selunitBut.pack(side='left')
ls_comm_kerfFrm = tk.Frame(ls_frm.interior)
ls_comm_kerfFrm.pack()
ls_comm_kerfLab = tk.Label(ls_comm_kerfFrm, text="kerf size")
ls_comm_kerfLab.pack(side = 'left', fill='x', expand=TRUE)
ls_comm_kerfEntry = tk.Entry(ls_comm_kerfFrm, relief='sunken', textvariable=kerfsize)
ls_comm_kerfEntry.pack(side='left')
ls_comm_gapFrm =  tk.Frame(ls_frm.interior)
ls_comm_gapFrm.pack()
ls_comm_gapLab =  tk.Label(ls_comm_gapFrm, text="Y Gap between cal. tests")
ls_comm_gapLab.pack(side='left')
ls_comm_gapEntry =  tk.Entry(ls_comm_gapFrm, relief='sunken', textvariable=commGap)
ls_comm_gapEntry.pack(side = 'left')

#--- Cut
ls_cut_sep = tk.Frame(ls_frm.interior, height=1, bg="black")
ls_cut_sep.pack(fill = 'x')
ls_cut_lab = tk.Label(ls_frm.interior, text="Cut Cal.")
ls_cut_lab.pack()
ls_cut_inc =  tk.Checkbutton(ls_frm.interior, text = 'Include Cut gcode',
			  onvalue=1, offvalue= 0,
			  variable=incCut)
ls_cut_inc.pack()
ls_cut_feedFrm = tk.Frame(ls_frm.interior)
ls_cut_feedFrm.pack()
ls_cut_feedLab = tk.Label(ls_cut_feedFrm, text="Feed Rate")
ls_cut_feedLab.pack(side='left')
ls_cut_feedEntry = tk.Entry(ls_cut_feedFrm, relief='sunken', textvariable=cutFeed)
ls_cut_feedEntry.pack(side='left')
ls_cut_powerFrm = tk.Frame(ls_frm.interior)
ls_cut_powerFrm.pack()
ls_cut_powerLab = tk.Label(ls_cut_powerFrm, text="Laser Power")
ls_cut_powerLab.pack(side='left')
ls_cut_powerEntry = tk.Entry(ls_cut_powerFrm, relief ='sunken', textvariable=cutPower)
ls_cut_powerEntry.pack(side='left')
ls_cut_XsizeFrm = tk.Frame(ls_frm.interior)
ls_cut_XsizeFrm.pack()
ls_cut_XsizeLab = tk.Label(ls_cut_XsizeFrm, text="X Dim. of box")
ls_cut_XsizeLab.pack(side='left')
ls_cut_XsizeEntry = tk.Entry(ls_cut_XsizeFrm, relief = 'sunken', textvariable=cutXsize)
ls_cut_XsizeEntry.pack(side='left')
ls_cut_YsizeFrm = tk.Frame(ls_frm.interior)
ls_cut_YsizeFrm.pack()
ls_cut_YsizeLab = tk.Label(ls_cut_YsizeFrm, text="Y Dim. of box")
ls_cut_YsizeLab.pack(side='left')
ls_cut_YsizeEntry = tk.Entry(ls_cut_YsizeFrm, relief='sunken', textvariable=cutYsize)
ls_cut_YsizeEntry.pack(side='left')
ls_cut_passesFrm = tk.Frame(ls_frm.interior)
ls_cut_passesFrm.pack()
ls_cut_passesLab = tk.Label(ls_cut_passesFrm, text="Number of passes")
ls_cut_passesLab.pack(side='left')
ls_cut_passesEntry = tk.Entry(ls_cut_passesFrm, relief='sunken', textvariable=cutPasses)
ls_cut_passesEntry.pack(side='left')

#--- Engrave
ls_engrave_sep = tk.Frame(ls_frm.interior, height=1, bg="black")
ls_engrave_sep.pack(fill = 'x')
ls_engrave_lab = tk.Label(ls_frm.interior, text="Engrave Cal.")
ls_engrave_lab.pack()
ls_engrave_inc = tk.Checkbutton(ls_frm.interior, text='Include Engrave gcode',
				 onvalue=1, offvalue=0,
				 variable=incEngrave)
ls_engrave_inc.pack()
ls_engrave_feedFrm = tk.Frame(ls_frm.interior)
ls_engrave_feedFrm.pack()
ls_engrave_feedlab = tk.Label(ls_engrave_feedFrm, text="Feed Rate")
ls_engrave_feedlab.pack(side='left')
ls_engrave_feedEntry = tk.Entry(ls_engrave_feedFrm, relief='sunken',
				 textvariable=engraveFeed)
ls_engrave_feedEntry.pack(side='left')
ls_engrave_maxPfrm = tk.Frame(ls_frm.interior)
ls_engrave_maxPfrm.pack()
ls_engrave_maxPlab = tk.Label(ls_engrave_maxPfrm, text="Max. Power")
ls_engrave_maxPlab.pack(side='left')
ls_engrave_maxPentry = tk.Entry(ls_engrave_maxPfrm, relief='sunken',
				 textvariable=engraveMaxP)
ls_engrave_maxPentry.pack(side='left')
ls_engrave_minPfrm = tk.Frame(ls_frm.interior)
ls_engrave_minPfrm.pack()
ls_engrave_minPlab = tk.Label(ls_engrave_minPfrm, text="Min. Power")
ls_engrave_minPlab.pack(side='left')
ls_engrave_minPentry = tk.Entry(ls_engrave_minPfrm, relief='sunken',
				 textvariable=engraveMinP)
ls_engrave_minPentry.pack(side='left')
ls_engrave_numPlevFrm = tk.Frame(ls_frm.interior)
ls_engrave_numPlevFrm.pack()
ls_engrave_numPlevLab = tk.Label(ls_engrave_numPlevFrm, text="Number of Power levels in bar")
ls_engrave_numPlevLab.pack(side='left')
ls_engrave_numPlevEntry = tk.Entry(ls_engrave_numPlevFrm, relief='sunken',
				textvariable=engraveNumPlev)
ls_engrave_numPlevEntry.pack(side='left')
ls_engrave_distIFrm = tk.Frame(ls_frm.interior)
ls_engrave_distIFrm.pack()
ls_engrave_distILab = tk.Label(ls_engrave_distIFrm, text="Distance between power changes")
ls_engrave_distILab.pack(side='left')
ls_engrave_distIEntry = tk.Entry(ls_engrave_distIFrm, relief='sunken',
				  textvariable=engraveDistI)
ls_engrave_distIEntry.pack(side='left')
ls_engrave_barLenLab =  tk.Label(ls_frm.interior, text=engraveBarLen)
ls_engrave_barLenLab.pack()
ls_engrave_barWidthFrm = tk.Frame(ls_frm.interior)
ls_engrave_barWidthFrm.pack()
ls_engrave_barWidthLab = tk.Label(ls_engrave_barWidthFrm, text="Width of bar to engrave")
ls_engrave_barWidthLab.pack(side='left')
ls_engrave_barWidthEntry = tk.Entry(ls_engrave_barWidthFrm, relief='sunken',
				 textvariable=engraveBarWidth)
ls_engrave_barWidthEntry.pack(side='left')
ls_engrave_IdxPfrm = tk.Frame(ls_frm.interior)
ls_engrave_IdxPfrm.pack()
ls_engrave_IdxPLab = tk.Label(ls_engrave_IdxPfrm, text="Power to use for index marks")
ls_engrave_IdxPLab.pack(side='left')
ls_engrave_IdxPEntry = tk.Entry(ls_engrave_IdxPfrm, relief='sunken',
				 textvariable=engraveIdxPwr)
ls_engrave_IdxPEntry.pack(side='left')
ls_engrave_maxIdxFrm = tk.Frame(ls_frm.interior)
ls_engrave_maxIdxFrm.pack()
ls_engrave_maxIdxLab = tk.Label(ls_engrave_maxIdxFrm, text="Maximum length of index marks")
ls_engrave_maxIdxLab.pack(side='left')
ls_engrave_maxIdxEntry = tk.Entry(ls_engrave_maxIdxFrm, relief='sunken',
				   textvariable=engraveIdxMax)
ls_engrave_maxIdxEntry.pack(side='left')

#--- Picture
ls_pic_sep = tk.Frame(ls_frm.interior, height=1, bg="black")
ls_pic_sep.pack(fill = 'x')
ls_pic_lab = tk.Label(ls_frm.interior, text="Picture Cal.")
ls_pic_lab.pack()
ls_pic_inc = tk.Checkbutton(ls_frm.interior, text='Include Picture gcode',
			 onvalue=1, offvalue=0,
			 variable=incPicture)
ls_pic_inc.pack()
ls_pic_feedFrm = tk.Frame(ls_frm.interior)
ls_pic_feedFrm.pack()
ls_pic_feedlab = tk.Label(ls_pic_feedFrm, text="Feed Rate")
ls_pic_feedlab.pack(side='left')
ls_pic_feedEntry = tk.Entry(ls_pic_feedFrm, relief='sunken',
			 textvariable=picFeed)
ls_pic_feedEntry.pack(side='left')
ls_pic_pwrFrm = tk.Frame(ls_frm.interior)
ls_pic_pwrFrm.pack()
ls_pic_pwrlab = tk.Label(ls_pic_pwrFrm, text="Laser Power")
ls_pic_pwrlab.pack(side='left')
ls_pic_pwrEntry = tk.Entry(ls_pic_pwrFrm, relief='sunken',
			textvariable=picPower)
ls_pic_pwrEntry.pack(side='left')
ls_pic_tstsepFrm = tk.Frame(ls_frm.interior)
ls_pic_tstsepFrm.pack()
ls_pic_tstseplab = tk.Label(ls_pic_tstsepFrm, text="Separation between lines in Y axis")
ls_pic_tstseplab.pack(side='left')
ls_pic_tstsepEntry = tk.Entry(ls_pic_tstsepFrm, relief='sunken',
			   textvariable=picTestsep)
ls_pic_tstsepEntry.pack(side='left')
ls_pic_SDsepFrm = tk.Frame(ls_frm.interior)
ls_pic_SDsepFrm.pack()
ls_pic_SDseplab = tk.Label(ls_pic_SDsepFrm, text="Single dots separation")
ls_pic_SDseplab.pack(side='left')
ls_pic_SDsepEntry = tk.Entry(ls_pic_SDsepFrm, relief='sunken',
			  textvariable=picSDsep)
ls_pic_SDsepEntry.pack(side='left')
ls_pic_SDnumFrm = tk.Frame(ls_frm.interior)
ls_pic_SDnumFrm.pack()
ls_pic_SDnumlab = tk.Label(ls_pic_SDnumFrm, text="Number of Single dots")
ls_pic_SDnumlab.pack(side='left')
ls_pic_SDnumEntry = tk.Entry(ls_pic_SDnumFrm, relief='sunken',
			  textvariable=picSDnum)
ls_pic_SDnumEntry.pack(side='left')
ls_pic_DDsepFrm = tk.Frame(ls_frm.interior)
ls_pic_DDsepFrm.pack()
ls_pic_DDseplab = tk.Label(ls_pic_DDsepFrm, text="Double dots separation")
ls_pic_DDseplab.pack(side='left')
ls_pic_DDsepEntry = tk.Entry(ls_pic_DDsepFrm, relief='sunken',
			  textvariable=picDDsep)
ls_pic_DDsepEntry.pack(side='left')
ls_pic_DDnumFrm = tk.Frame(ls_frm.interior)
ls_pic_DDnumFrm.pack()
ls_pic_DDnumlab = tk.Label(ls_pic_DDnumFrm, text="Number of Double dots")
ls_pic_DDnumlab.pack(side='left')
ls_pic_DDnumEntry = tk.Entry(ls_pic_DDnumFrm, relief='sunken',
			  textvariable=picDDnum)
ls_pic_DDnumEntry.pack(side='left')
ls_pic_DashDotLab1 = tk.Label(ls_frm.interior, text="Pattern Test _ _ _ . . _ _ _")
ls_pic_DashDotLab1.pack()
ls_pic_DashWidthFrm = tk.Frame(ls_frm.interior)
ls_pic_DashWidthFrm.pack()
ls_pic_DashWidthLab = tk.Label(ls_pic_DashWidthFrm, text="Dash Length = (kerf*x)")
ls_pic_DashWidthLab.pack(side='left')
ls_pic_DashWidthEntry = tk.Entry(ls_pic_DashWidthFrm, relief='sunken',
				  textvariable=picDashWidth)
ls_pic_DashWidthEntry.pack(side='left')

ls_pic_DashsepFrm = tk.Frame(ls_frm.interior)
ls_pic_DashsepFrm.pack()
ls_pic_DashsepLab = tk.Label(ls_pic_DashsepFrm, text="Separation size")
ls_pic_DashsepLab.pack(side='left')
ls_pic_DashsepEntry = tk.Entry(ls_pic_DashsepFrm, relief='sunken', textvariable=picDashsep)
ls_pic_DashsepEntry.pack(side='left')
ls_pic_incDithered = tk.Checkbutton(ls_frm.interior, text='Include Dithered image gcode',
			 onvalue=1, offvalue=0,
			 variable=picIncDithered)
ls_pic_incDithered.pack()
ls_pic_DitherFNFrm = tk.Frame(ls_frm.interior)
ls_pic_DitherFNFrm.pack()
ls_pic_DitheredFNLab = tk.Label(ls_pic_DitherFNFrm, text="Dithered Image Filename")
ls_pic_DitheredFNLab.pack(side='left')
ls_pic_DitheredFNEntry = tk.Entry(ls_pic_DitherFNFrm, relief='sunken', textvariable=picDitheredFN)
ls_pic_DitheredFNEntry.pack(side='left')

#--- Function and bindings to update the Engrave Bar Length text
def update_eng_len(event):
	temp=float(ls_engrave_numPlevEntry.get()) * float(ls_engrave_distIEntry.get())
	engraveBarLen='Length of engrave bar = ' + str(temp)
	ls_engrave_barLenLab.configure(text=engraveBarLen);


update_eng_len(0)
ls_engrave_numPlevEntry.bind("<Return>", update_eng_len)
ls_engrave_distIEntry.bind("<Return>", update_eng_len)

def gen_gcode():
	global preamble
	global postamble
	global units
	global kerfsize
	global commGap

	#-- Cut
	global incCut
	global cutPower
	global cutFeed
	global cutXsize
	global cutYsize
	global cutPasses

	#-- Engrave
	global incEngrave
	global engraveFeed
	global engraveMaxP
	global engraveMinP
	global engraveNumPlev
	global engraveDistI
	global engraveBarWidth
	global engraveIdxPwr
	global engraveIdxMax

	#-- Picture
	global incPicture
	global picPower
	global picFeed
	global picTestsep
	global picSDsep
	global picSDnum
	global picDDsep
	global picDDnum
	global picDashWidth
	global picDashsep
	global picIncDithered
	global picDitheredFN

	#gcode[:] = [] #clear current gcode
	del G.gcode[:]

	# Gcode starting comments and preamble
	G.gcode.append('; Gencal_gcode generate calibration code')
	G.gcode.append('; kerfsize = ' + ls_comm_kerfEntry.get())
	G.gcode.append('; PREAMBLE')
	G.gcode.extend(preamble)

	if units == "G21" :
		tmp='; set units to mm'
	else :
		tmp='; set units to inches'
	G.gcode.append(tmp)
	G.gcode.append(units)

	curX = 0.0
	curY = 0.0
	curPwr = 0
	i = 0
	k = 0

	#-- Cut gcode
	if incCut.get() == 1 :
		G.gcode.append('; Cut calibration box size ' + cutXsize.get() + ' x ' + cutYsize.get())
		G.gcode.append('G1 F' + cutFeed.get() + ' ;set feed rate')
		G.gcode.append('M04 S' + cutPower.get() + ' ;Turn laser on and set power')
		# Cut box
		while i < float(cutPasses.get()) :
			i+=1
			G.gcode.append(';Pass ' + str(i))
			G.gcode.append('G1 X' + strXY(curX) + 'Y' + strXY(curY))
			curY += float(cutYsize.get())
			G.gcode.append('G1 X' + strXY(curX) + 'Y' + strXY(curY))
			curX += float(cutXsize.get())
			G.gcode.append('G1 X' + strXY(curX) + 'Y' + str(curY))
			curY -= float(cutYsize.get())
			G.gcode.append('G1 X' + str(curX) + 'Y' + strXY(curY))
			curX -= float(cutXsize.get())
			G.gcode.append('G1 X' + strXY(curX) + 'Y' + strXY(curY))

		G.gcode.append('M05 S0 ;Turn Laser off and set power to 0')

		#-- move to next starting point
		curY += float(cutYsize.get()) + float(commGap.get())
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))
		G.gcode.append(';End of Cut calibration gcode')

	#-- Engrave gcode
	if incEngrave.get() == 1 :
		G.gcode.append('; Engrave calibration')
		G.gcode.append('G1 F' + engraveFeed.get());
		#Loop drawing the lines of the engrave bar
		lstline = curY + float(engraveBarWidth.get())
		pwrinc = (float(engraveMaxP.get()) - float(engraveMinP.get()))/float(engraveNumPlev.get())

		while curY <= lstline :
			curX = 0;
			curPwr = float(engraveMinP.get())
			G.gcode.append('M04 S' + str(curPwr))
			k = float(engraveNumPlev.get())-1
			while k > 0 :
				curX += float(engraveDistI.get())
				curPwr += pwrinc
				G.gcode.append('G1 X' + strXY(curX) + 'Y' + strXY(curY) + ' S' + str(int(curPwr)))
				k-=1

			#last segment at Max power
			G.gcode.append('M04 S' + engraveMaxP.get())
			G.gcode.append('G1 X' + strXY(curX + float(engraveDistI.get())) + 'Y' + strXY(curY))

			#return X and increment to next Y for next line
			G.gcode.append('M05 S0')  #Turn laser off
			curX = 0
			curY += float(kerfsize.get())
			G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))

		# make indexing marks where power levels changed
		curY += float(kerfsize.get())
		G.gcode.append('; engrave make power index marks')
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))
		G.gcode.append('M04 S' + engraveIdxPwr.get())
		k = 0

		while k <= int(engraveNumPlev.get()) :
			i = int(engraveIdxMax.get())
			if (k % 5) != 0 :
				i /= 2

			G.gcode.append('G1 X' + str(curX) + 'Y' + strXY(curY + i))
			curX += float(engraveDistI.get())
			G.gcode.append('G0 X' + str(curX) + 'Y' + str(curY))
			k+=1

		G.gcode.append('M05 S0')  #Turn Laser off
		#-- move to next starting point
		curX = 0.0
		curY += float(engraveIdxMax.get()) + float(commGap.get())
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))


		G.gcode.append('M05 S0 ;Turn Laser off and set power to 0')

		#-- move to next starting point
		curY += float(cutYsize.get()) + float(commGap.get())
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))
		G.gcode.append(';End of Engrave calibration gcode')

	#-- Picture gcode
	if incPicture.get() == 1 :
		G.gcode.append('; Picture calibration')
		G.gcode.append('G0 F' + picFeed.get())
		G.gcode.append('M03 S0')

		# Create a single row of dots
		G.gcode.append('; Picture single row of dots')
		i = 0;
		G.gcode.append('G1')
		while i <= int(picSDnum.get()) :
			G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
			curX += float(picSDsep.get())
			G.gcode.append('X' + strXY(curX) + 'S0')
			curX += float(kerfsize.get())
			i+=1

		curX = 0
		curY += float(picTestsep.get())
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))

		# Create a double row of dots
		G.gcode.append('; Picture double row of dots')
		i = 0
		while i <= int(picDDnum.get()) :
			G.gcode.append('G1 X' + strXY(curX) + ' S' + picPower.get())
			curX += float(kerfsize.get())
			G.gcode.append('X' + strXY(curX) + ' S0')
			curX += float(picSDsep.get())
			i+=1

		curX = 0
		curY += float(kerfsize.get())
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))
		i = 0
		while i <= int(picDDnum.get()) :
			G.gcode.append('G1 X' + strXY(curX) + ' S' + picPower.get())
			curX += float(kerfsize.get())
			G.gcode.append('X' + strXY(curX) + ' S0')
			curX += float(picSDsep.get())
			i+=1

		curX = 0
		curY += float(picTestsep.get())
		G.gcode.append('G0 X' + strXY(curX) + 'Y' + strXY(curY))

		# Create _ _ _ . . _ _ _ Pattern
		G.gcode.append('; Picture _ _ _ . . _ _ _ Pattern')

		dashwidth=float(kerfsize.get()) * float(picDashWidth.get())
		dashsep=float(picDashsep.get())
		# Dash 1
		G.gcode.append(';Dash 1')
		G.gcode.append('G1 X' + strXY(curX) + ' S0')
		curX += dashwidth
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += dashsep
		# Dash 2
		G.gcode.append(';Dash 2')
		G.gcode.append('X' + strXY(curX) + ' S0')
		curX += dashwidth
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += dashsep
		# Dash 3
		G.gcode.append(';Dash 3')
		G.gcode.append('X' + strXY(curX) + ' S0')
		curX += dashwidth
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += dashsep
		# Dot 1
		G.gcode.append(';Dot 1')
		G.gcode.append('X' + strXY(curX) + ' S0')
		curX += float(kerfsize.get())
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += float(picSDsep.get())
		# Dot 2
		G.gcode.append(';Dot 2')
		G.gcode.append('X' + strXY(curX) + ' S0')
		curX += float(kerfsize.get())
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += dashsep
		# Dash 4
		G.gcode.append(';Dash 4')
		G.gcode.append('X' + strXY(curX) + ' S0')
		curX += dashwidth
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += dashsep
		# Dash 5
		G.gcode.append(';Dash 5')
		G.gcode.append('X' + strXY(curX) + ' S0')
		curX += dashwidth
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		curX += dashsep
		# Dash 6
		G.gcode.append(';Dash 6')
		G.gcode.append('X' + strXY(curX) + 'S0')
		curX += dashwidth
		G.gcode.append('X' + strXY(curX) + ' S' + picPower.get())
		G.gcode.append('G0 S0')

		#-- move to next starting point
		curX = 0;
		curY += float(commGap.get())
		G.gcode.append('G0 X' + str(curX) + 'Y' + str(curY))

		#-- Dithered Image
		if picIncDithered.get() == 1:
			G.gcode.append("; Including Dithered Image Gcode")
			G.gcode.append("G92 X0 Y0 ;use current position as origin")
			with open(resource_path(picDitheredFN.get()), 'r') as f:
				picBuf = f.readlines()

			for line in picBuf:
				line = line.rstrip('\r\n')
				if len(line) != 0:
					line = line.replace('Feed', 'F' + picFeed.get())
					line = line.replace('Spwr', 'S' + picPower.get())
					G.gcode.append(line)

	# Gcode ending comments and postamble
	G.gcode.append('; POSTAMBLE')
	G.gcode.extend(postamble)

	#-- update Gcode in the right-side Listbox
	rs_lstbox.delete(0,END)
	for line in G.gcode :
		rs_lstbox.insert(END, line)
	return TRUE

#strXY() converts a floating point number to string and rounds it to the nears 10th
def strXY(value):
	return str(int((value * 100) + 0.5) / 100.0)

rs_gen_but.configure(command=gen_gcode)

def toggle_units() :
	global units
	if units == 'G21' :
		units = 'G20'
		ls_comm_selunitBut.configure(text="inches")
	else :
		units = 'G21'
		ls_comm_selunitBut.configure(text="mm")

ls_comm_selunitBut.configure(command=toggle_units)

mw.mainloop()
