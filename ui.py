# http://www.jython.org/jythonbook/en/1.0/GUIApplications.html
#from javax.swing import JButton, JFrame, JPanel, JTextField, JButton, JButton
#from java.awt import BorderLayout, GridLayout
from javax.swing import*
from javax.swing.border import TitledBorder
from java.awt import*

from hello import*

frame = JFrame('Hello, Jython!',defaultCloseOperation = JFrame.EXIT_ON_CLOSE, size = (2000, 2000))

def getPressureLabel():

    pressure_label = JLabel("Pressure");
    pressure_icon = ImageIcon(ImageIcon("pressure.png").getImage().getScaledInstance(50, 50, Image.SCALE_DEFAULT));
    pressure_label = JLabel("", pressure_icon, JLabel.LEFT);

    return pressure_label

def getTempLabel():

    temp_label = JLabel("Temparature");
    temp_icon = ImageIcon(ImageIcon("temp.png").getImage().getScaledInstance(60, 60, Image.SCALE_DEFAULT));
    temp_label = JLabel("", temp_icon, JLabel.LEFT);

    return temp_label
    

def prepareStaticTPScreen():
    print 'prepareStaticTPScreen'
    global liveDataPanel
    global vehName_label_s
    global tp_font, tpHeader_font

    liveDataPanel.layout = BorderLayout()
    vehName_label_s.preferredSize = Dimension(200, 70)
    vehName_label_s.horizontalAlignment = SwingConstants.CENTER
    vehName_label_s.font = Font("Arial", Font.PLAIN, 40)
    vehName_label_s.text = "Veh Name"

    liveDataPanel.add(vehName_label_s, BorderLayout.NORTH)
    bottomMainPanel = JPanel()
    bottomMainPanel.layout = GridLayout(1, 3)

    sizeLayout = GridLayout(2, 2, 10, 10)
    liveDataPanel.add(bottomMainPanel, BorderLayout.CENTER)

    # Left side values
    leftPanel = JPanel()
    leftLayout = BoxLayout(leftPanel, BoxLayout.Y_AXIS)
    leftPanel.setLayout(leftLayout)

    panel11 = JPanel()
    panel11.border = BorderFactory.createTitledBorder(None, "Front Left", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font)

    fl_pressure_label_s.font = tp_font
    fl_temp_label_s.font = tp_font
    fl_panel = JPanel(sizeLayout)
    fl_panel.add(getPressureLabel())
    fl_panel.add(fl_pressure_label_s)
    fl_panel.add(getTempLabel())
    fl_panel.add(fl_temp_label_s)

    panel11.add(fl_panel)
    leftPanel.add(panel11)

    panel12 = JPanel()
    panel12.border = BorderFactory.createTitledBorder(None, "Rear Left Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font)

    rlo_pressure_label_s.font = tp_font
    rlo_temp_label_s.font  = tp_font
    rlo_panel = JPanel(sizeLayout);
    rlo_panel.add(getPressureLabel());
    rlo_panel.add(rlo_pressure_label_s);
    rlo_panel.add(getTempLabel());
    rlo_panel.add(rlo_temp_label_s);

    panel12.add(rlo_panel);

    leftPanel.add(panel12);

    panel13 = JPanel()
    panel13.border = BorderFactory.createTitledBorder(None, "Rear Left Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font)

    rli_pressure_label_s.font = tp_font
    rli_temp_label_s.font = tp_font
    rli_panel = JPanel(sizeLayout)
    rli_panel.add(getPressureLabel())
    rli_panel.add(rli_pressure_label_s)
    rli_panel.add(getTempLabel())
    rli_panel.add(rli_temp_label_s)

    panel13.add(rli_panel)

    leftPanel.add(panel13)

    centralPanel = JPanel()
    imgLabel = JLabel("Vehicle")
    veh_icon = ImageIcon(ImageIcon("bustyres.png").getImage().getScaledInstance(250, 600, Image.SCALE_SMOOTH))
    imgLabel = JLabel("", veh_icon, JLabel.CENTER)
    
    centralPanel.add(imgLabel);

    # Right side values
    rightPanel = JPanel()
    rightLayout = BoxLayout(rightPanel, BoxLayout.Y_AXIS)
    rightPanel.setLayout(rightLayout)

    panelFR =  JPanel()
    panelFR.border = BorderFactory.createTitledBorder(None, "Front Right", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font)

    fr_pressure_label_s.font = tp_font
    fr_temp_label_s.font = tp_font
    fr_panel = JPanel(sizeLayout)
    fr_panel.add(getPressureLabel())
    fr_panel.add(fr_pressure_label_s)
    fr_panel.add(getTempLabel())
    fr_panel.add(fr_temp_label_s)

    panelFR.add(fr_panel)
    rightPanel.add(panelFR)

    panelRRO = JPanel()
    panelRRO.border = BorderFactory.createTitledBorder(None, "Rear Right Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font)

    rro_pressure_label_s.font = tp_font
    rro_temp_label_s.font = tp_font
    rro_panel = JPanel(sizeLayout)
    rro_panel.add(getPressureLabel())
    rro_panel.add(rro_pressure_label_s)
    rro_panel.add(getTempLabel())
    rro_panel.add(rro_temp_label_s)
    panelRRO.add(rro_panel)

    rightPanel.add(panelRRO)

    panelRRI = JPanel();
    panelRRI.border = BorderFactory.createTitledBorder(None, "Rear Right Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font)

    rri_pressure_label_s.font = tp_font
    rri_temp_label_s.font = tp_font 
    rri_panel = JPanel(sizeLayout)
    rri_panel.add(getPressureLabel())
    rri_panel.add(rri_pressure_label_s)
    rri_panel.add(getTempLabel())
    rri_panel.add(rri_temp_label_s)

    panelRRI.add(rri_panel)

    rightPanel.add(panelRRI)

    leftPanel.setMaximumSize(leftPanel.getPreferredSize());
    leftPanel.setMinimumSize(leftPanel.getPreferredSize());

    bottomMainPanel.add(leftPanel)
    bottomMainPanel.add(centralPanel);
    bottomMainPanel.add(rightPanel);


def prepareKeyboardPanel():
    global keyboardPanel
    global b1,b2, b3, b4, b5, b6, b7, b8, b9, b0, bbackspace, bclear

    b1.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b1)
    b1.actionPerformed = keyboardEvent

    b2.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b2)
    b2.actionPerformed = keyboardEvent

    b3.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b3)
    b3.actionPerformed = keyboardEvent

    b4.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b4)
    b4.actionPerformed = keyboardEvent

    b5.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b5)
    b5.actionPerformed = keyboardEvent

    b6.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b6)
    b6.actionPerformed = keyboardEvent

    b7.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b7)
    b7.actionPerformed = keyboardEvent

    b8.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b8)
    b8.actionPerformed = keyboardEvent

    b9.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b9)
    b9.actionPerformed = keyboardEvent

    bbackspace.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(bbackspace)
    bbackspace.actionPerformed = keyboardEvent

    b0.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(b0)
    b0.actionPerformed = keyboardEvent

    bclear.font = Font("Arial", Font.PLAIN, 50)
    keyboardPanel.add(bclear)
    bclear.actionPerformed = keyboardEvent

#End of Keyboard Panel preparation

def keyboardEvent(event):

    if event.getSource() == b1:
	searchBox.text = searchBox.text + "1"
    elif event.getSource() == b2:
	searchBox.text = searchBox.text + "2"
    elif event.getSource() == b3:
	searchBox.text = searchBox.text + "3"
    elif event.getSource() == b4:
	searchBox.text = searchBox.text + "4"
    elif event.getSource() == b5:
	searchBox.text = searchBox.text + "5"
    elif event.getSource() == b6:
	searchBox.text = searchBox.text + "6"
    elif event.getSource() == b7:
	searchBox.text = searchBox.text + "7"
    elif event.getSource() == b8:
	searchBox.text = searchBox.text + "8"
    elif event.getSource() == b9:
	searchBox.text = searchBox.text + "9"
    elif event.getSource() == b0:
	searchBox.text = searchBox.text + "0"
    elif event.getSource() == bbackspace:
	searchBox.text = searchBox.text[:-1]
    elif event.getSource() == bclear:
	searchBox.text = ""

def scanClickEvent(event):

    headerPanel.remove(searchBox)
    headerPanel.remove(bscan)
    
    headerPanel.add(vehName_label_s)
    headerPanel.add(bdone)

    keyboardPanel.visible = False
    liveDataPanel.visible = True
    run('123456')

def doneClickEvent(event):
    headerPanel.add(searchBox)
    headerPanel.add(bscan)
    
    headerPanel.remove(vehName_label_s)
    headerPanel.remove(bdone)

    keyboardPanel.visible = True
    liveDataPanel.visible = False

#Declare all the variables
tp_font = Font("Arial", Font.PLAIN, 30)
tpHeader_font = Font("Arial", Font.PLAIN, 15).deriveFont(Font.BOLD)

vehName_label_s = JLabel()
searchBox = JTextField()
bscan = JButton("Scan")
bdone = JButton("Done")

b1 = JButton("1")
b2 = JButton("2")
b3 = JButton("3")
b4 = JButton("4")
b5 = JButton("5")
b6 = JButton("6")
b7 = JButton("7")
b8 = JButton("8")
b9 = JButton("9")
bbackspace = JButton("Backspace")
b0 = JButton("0")
bclear = JButton("Clear")

fl_pressure_label_s = JLabel(" --- ")
fl_temp_label_s = JLabel(" --- ")
fr_pressure_label_s = JLabel(" --- ")
fr_temp_label_s = JLabel(" --- ")
rlo_pressure_label_s = JLabel(" --- ")
rlo_temp_label_s = JLabel(" --- ")
rli_pressure_label_s = JLabel(" --- ")
rli_temp_label_s = JLabel(" --- ")
rri_pressure_label_s = JLabel(" --- ")
rri_temp_label_s = JLabel(" --- ")
rro_pressure_label_s = JLabel(" --- ")
rro_temp_label_s = JLabel(" --- ")

#Basic Panel
mainPanel = JPanel()
mainPanel.layout = BorderLayout()

#Header panel contains textbox (Search & Lable (Veh Name) ) & Button (Scan & Done)
headerPanel = JPanel()
headerPanel.layout = GridLayout(1, 2)

#Keyboard panel
keyboardPanel = JPanel()
keyboardPanel.layout = GridLayout(4, 3)

#Live Data panel (Shows Tyre Temp & Pressure)
liveDataPanel = JPanel()

#Contains both Keyboard panel & Live Data panel (Shows any one at one time)
borderCenterLayout = JPanel()

#End of declaration


#Preparing header panel elements
searchBox.horizontalAlignment = SwingConstants.CENTER
searchBox.font = Font("Arial", Font.PLAIN, 50)

bscan.actionPerformed = scanClickEvent
bdone.actionPerformed = doneClickEvent

#Adding searchbox & bscan button
headerPanel.add(searchBox)
headerPanel.add(bscan)

#Prepare Keyboard panel
prepareKeyboardPanel()

#prepare Static Live Data panel
prepareStaticTPScreen()

#Add keyboard & Live Data panels to borderCenterLayout

keyboardPanel.visible = True
borderCenterLayout.add(keyboardPanel)

liveDataPanel.visible = False
borderCenterLayout.add(liveDataPanel)


# Add header Panel and borderCenterLayout panels to main panel
mainPanel.add(headerPanel, BorderLayout.NORTH)
mainPanel.add(borderCenterLayout, BorderLayout.CENTER);


frame.add(mainPanel)
frame.visible = True

