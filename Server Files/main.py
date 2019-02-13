import os
import socket
import datetime
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QStackedWidget, QMainWindow, QApplication, QPushButton, \
    QVBoxLayout
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from gtts import gTTS
from gpiozero import LED
from time import sleep
led = LED(17)

global order
order = dict
global food

# Global Price of the Items
price = {"Pizza":500, 'Burger':150, "Pastry":80, "Coffee":50, "Set menu":200, "Soft Drinks":30}

######################## Make the Receipt ###########################
class MakeOrderReceipt():

    def makeReceipt(self, table_Id, order, order_number):
        order_dict = order
        date = datetime.datetime.today().strftime("%d-%m-%y")
        restaurant_name = "MTE Restaurant"
        date = datetime.datetime.now().strftime("%d/%m/%y")
        day = datetime.datetime.today().strftime("%A")
        time = datetime.datetime.now().strftime("%H:%M")
        # add new order
        # Add global price dictionary
        global price

        order_file = "Order_{}_{}".format(table_Id, order_number)
        receipt = open(order_file, 'a')

        receipt.write("\t#################### {} ####################\n"
                "\t  Rajshahi University of Engineering and & Technology\n"
                "\t\t\t  Talaimari, Rajshahi\n\n"
                "\t\t\t {} {} {}\n"
                "\t--------------------------------------------------------\n"
                "\tTable Number: {}\n"
                "\tOrder Number: {}\n"
                "\t--------------------------------------------------------\n"
                "\tItem\t\t Price\t\t Quantity\t Amount\n"
                "\t--------------------------------------------------------\n"
                .format(restaurant_name, day, date, time, table_Id, order_number))

        total = 0

        for key, val in order_dict.items():
            receipt.write("\t{}\t\t {}\t\t {}\t\t {}\n".format(key, price[key], val, price[key] * val))
            total += price[key] * val

        receipt.write("\t--------------------------------------------------------\n"
                "\tTotal\t\t\t\t\t\t {}\n"
                "\tVAT (15%)\t\t\t\t\t {}\n"
                "\t--------------------------------------------------------\n"
                "\tGrand Total\t\t\t\t\t {}TK\n"
                "\t--------------------------------------------------------\n"
                "\t\t\t\tThank You\n".format(total, int(total * 0.15), int((total + total * 0.15))))

        receipt.close()
        return order_file





################ Send the Order to the Kitchen ############
class SendOrderToKitchen():
    def __init__(self):
        # Initialize the socket to send the Data to Kitchen
        self.host = 'put your host IP address here'
        self.port = 5000
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        # use this function to send the text file
        self.s.listen(5)
        print("Server Listening......")
        self.conn, self.addr = self.s.accept()
        print("Got connection from ", str(self.addr))



    def sendFile(self,file):
        try:
            self.conn.send("Sending".encode())
        except:
            pass
        text_file = file
        f = open(text_file, 'rb')
        line = f.read(1024)

        while (line):
            self.conn.send(line)
            line = f.read(1024)

        f.close()
        print("Done Sending the Order.....")
        #self.conn.close()
        #self.s.close()




########## Widget to select the amount of each item ############

class AmountWidget(QWidget):
    def __init__(self):
        super(AmountWidget, self).__init__()
        loadUi('amount.ui', self)
        self.okButton.clicked.connect(self.okClicked)
        self.setWindowTitle("Amount")

    @pyqtSlot()
    def okClicked(self):
        amount = self.spinBox.value()
        if amount>0:
            order[food] = amount
        self.spinBox.setValue(0)
        print(order)
        amountwindow.close()

################# Main Window (contains all the widgets and controls the interface) ############
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.send_obj = SendOrderToKitchen()
        self.setWindowTitle("Waiter Robot")
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color:rgb(114, 159, 207);")
        self.resize(800,400)
        self.showHelloWidget()
        self.order_number = 0

    def showItemWidget(self):
        global order
        order = dict()
        item_widget = ItemWidget(self)
        self.central_widget.addWidget(item_widget)
        self.central_widget.setCurrentWidget(item_widget)
        #os.system("mpg321 item_selection.mp3")
        item_widget.orderButton.clicked.connect(self.showOrderWidget)
        item_widget.cancelButton.clicked.connect(self.showHelloWidget)

    def showHelloWidget(self):
        hello_widget = HelloWidget()
        self.central_widget.addWidget(hello_widget)
        self.central_widget.setCurrentWidget(hello_widget)
        hello_widget.itemButton.clicked.connect(self.showItemWidget)
        hello_widget.passButton.clicked.connect(self.passTheBot)
        
    def passTheBot(self):
        # GPIO 17 no pin
        led.on()
        sleep(1)
        led.off()

    def showthankWidget(self):
        global order
        self.order_number+=1
        # Make the file Using the Order Dict
        file = MakeOrderReceipt().makeReceipt(2,order,self.order_number)
        print("Receipt Prepared....")
        # Send file to the Laptop 
        self.send_obj.sendFile(file)
        #os.system("mpg321 Thank_you.mp3")
        self.passTheBot()
        thank_widget = ThankWidget(self)
        self.central_widget.addWidget(thank_widget)
        self.central_widget.setCurrentWidget(thank_widget)
        thank_widget.restart.clicked.connect(self.showHelloWidget)

    def showOrderWidget(self):
        order_widget = OrderWidget(self)
        self.central_widget.addWidget(order_widget)
        self.central_widget.setCurrentWidget(order_widget)
        order_widget.checkButton.clicked.connect(self.showItemWidget)
        order_widget.confirmButton.clicked.connect(self.showthankWidget)


########### Class to make the First Hello Widget ###############
class HelloWidget(QWidget):
    def __init__(self, parent=None):
        super(HelloWidget, self).__init__(parent)
        self.helloLabel = QLabel()
        self.itemButton = QPushButton('Items')
        self.passButton = QPushButton('Pass')

        movie = QtGui.QMovie("hello.gif")
        self.helloLabel.setMovie(movie)
        movie.start()
        
        layout_horiz = QHBoxLayout()
        layout = QVBoxLayout()
        
        layout.addWidget(self.helloLabel)
        layout_horiz.addWidget(self.passButton)
        layout_horiz.addWidget(self.itemButton)
        layout.addLayout(layout_horiz)
        
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


########## Class to create Item widget, show the items ################
class ItemWidget(QWidget):
    def __init__(self, parent=None):
        super(ItemWidget, self).__init__(parent)
        loadUi('items_widget.ui', self)
        self.pizzaButton.clicked.connect(self.pizzaClicked)
        self.burgerButton.clicked.connect(self.burgerClicked)
        self.pastryButton.clicked.connect(self.pastryClicked)
        self.coffeeButton.clicked.connect(self.coffeeClicked)
        self.drinkButton.clicked.connect(self.drinkClicked)
        self.setmenuButton.clicked.connect(self.setmenuClicked)
        self.orderButton.clicked.connect(self.orderClicked)


    @pyqtSlot()
    def orderClicked(self):
        print(order)

    @pyqtSlot()
    def pizzaClicked(self):
        global food
        food = "Pizza"
        amountwindow.show()


    @pyqtSlot()
    def burgerClicked(self):
        global food
        food = "Burger"
        amountwindow.show()


    @pyqtSlot()
    def pastryClicked(self):
        global food
        food = "Pastry"
        amountwindow.show()

    @pyqtSlot()
    def coffeeClicked(self):
        global food
        food = "Coffee"
        amountwindow.show()


    @pyqtSlot()
    def drinkClicked(self):
        global food
        food = "Soft Drinks"
        amountwindow.show()

    @pyqtSlot()
    def setmenuClicked(self):
        global food
        food = "Set menu"
        amountwindow.show()


#### Class to create the Thank you widget, you can change the image in plcae of 'thank.png'file####
class ThankWidget(QWidget):
    def __init__(self, parent=None):
        super(ThankWidget, self).__init__(parent)
        self.thankLabel = QLabel()
        self.restart = QPushButton('Restart')

        self.thankLabel.setPixmap(QtGui.QPixmap("thank.png"))
        layout = QVBoxLayout()
        layout.addWidget(self.thankLabel)
        layout.addWidget(self.restart)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)



############## Class to show the selected items and amount ############
class OrderWidget(QWidget):
    def __init__(self, parent=None):
        super(OrderWidget, self).__init__(parent)
        self.confirmButton = QPushButton('Confirm', self)


        self.checkButton = QPushButton('Edit Oder', self)

        self.topLabel = QLabel()
        self.topLabel.setText("You have Ordered")

        self.bottom_layout = QHBoxLayout()
        self.top_layout = QHBoxLayout()

        self.top_layout.addWidget(self.topLabel)
        self.top_layout.setAlignment(Qt.AlignCenter)

        self.dd = {}
        vlayout = QVBoxLayout()

        vlayout.addLayout(self.top_layout)
        for key, val in order.items():
            lb1 = key +str(1)
            lb2 = key +str(2)
            lb3 = key +str(3)

            self.dd[lb1] = QLabel()
            self.dd[lb2] = QLabel()
            self.dd[lb3] = QLabel()

            self.dd[lb1].setPixmap(QtGui.QPixmap("{}.png".format(key)).scaledToWidth(60))
            self.dd[lb2].setText("X")
            self.dd[lb3].setText(str(val))

            lbhb = key +str("hb")
            self.dd[lbhb] = QHBoxLayout()

            self.dd[lbhb].addWidget(self.dd[lb1])
            self.dd[lbhb].addWidget(self.dd[lb2])
            self.dd[lbhb].addWidget(self.dd[lb3])

            self.dd[lbhb].setAlignment(Qt.AlignCenter)


            vlayout.addLayout(self.dd[lbhb])


        self.bottom_layout.addWidget(self.checkButton)

        self.bottom_layout.addWidget(self.confirmButton)

        self.bottom_layout.setAlignment(Qt.AlignCenter)
        vlayout.addLayout(self.bottom_layout)
        self.setLayout(vlayout)


########## Main function ################
if __name__ == '__main__':
    app = QApplication([])
    amountwindow = AmountWidget()
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()

