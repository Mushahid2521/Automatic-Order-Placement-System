# Automatic-Order-Placement-System
Please go through [this](https://www.youtube.com/watch?v=jHJsRyRvs8c) link to see the demonstration. 

Due to advancement of technology and tendency to replace human for the non techical tasks we are substituting human with machine. Here this repository demonstrate an Automatic Order Placement system where the Customer can choose the items and set the amount for each item to consume. This order data is autmatically sent to the client side and the receipt is printed with the necessary information(total cost with VAT, time of order placement etc). 

## Usage
- Create a folder in the home directory in the RaspberryPi with name ```CaseStudy``` and put the files of the ```Server Files``` folder on it.
- Put the files of the ```Client Files``` folder in the laptop with `Linux` operating System.
- Install the required packages using the following Commands
- Connect your raspberry pi and laptop with a same network and find the IP arrdess of it. (Use the ```ifconfig``` command to see the IP address. 
- Put the IP address in the host variable in the main.py script and client.py script. 
- Run the ```main.py``` script.
- After that run the ```client.py``` script. (The app won't start if the client.py file is not run in the client side)
## Package Installation
- ```pip3 install PyQt5``` to insatll the user interface designing package in Python.
- Use ```pip3``` command if other packages are not installed. (All the other packages remains preinsatlled. 
