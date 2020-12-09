import os
import sys

from PyQt5.QtCore import QUrl,Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget,QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.Qt import QHBoxLayout,QVBoxLayout

import folium

def create(marker):
    map = folium.Map(location=[marker[0],marker[1]], zoom_start=50)
    folium.Marker(location=[marker[0], marker[1]], popup='test').add_to(map)
    icon = folium.Icon(color='gray').add_to(map)
    #folium.PolyLine([[41.3165, 69.1876], [41.3165, 69.1776]]).add_to(map)
    #folium.CircleMarker([41.3165, 69.1876], radius=5, fill_color="#3db7e4").add_to(map)

    map.save("map1.html")



def main(app):
    pm=QMainWindow()
    centralWidget=QWidget(pm)
    browser=QWebEngineView(pm)
    btn=QLineEdit()
    btn.setMaximumWidth(600)

    def myprint():
        v = btn.text()
        create([v.split(" ")[0],v.split(" ")[1]])

        filename = os.path.join(current_dir, "map1.html")
        url = QUrl.fromLocalFile(filename)
        browser.setUrl(url)

    def readlist():
        with open("coord_list.txt") as f:
            data = f.read()

        res = []
        lst = data.split("\n")
        for x in lst:
            v = x.split(",")
            if len(v)==2:
                res.append([float(v[0]), float(v[1])])


        map = folium.Map(location=[res[0][0],res[0][1]], zoom_start=50)

        i=0
        for geo in res:
            folium.CircleMarker(location=geo, radius=5, fill_color="#3db7e4",popup=str(i+1)).add_to(map)
            i=i+1

        for i in range(len(res)-1):
            folium.PolyLine([res[i], res[i+1]],dash_array='10').add_to(map)

        map.save("map1.html")

        filename = os.path.join(current_dir, "map1.html")
        url = QUrl.fromLocalFile(filename)
        browser.setUrl(url)


    btn2 =QPushButton("Marker")
    btn2.clicked.connect(myprint)

    btn3 = QPushButton("Load from file")
    btn3.clicked.connect(readlist)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(current_dir, "map1.html")
    url = QUrl.fromLocalFile(filename)
    browser.setUrl(url)

    box=QVBoxLayout()

    box.addWidget(browser)
    box.addWidget(btn,  0, Qt.AlignLeft | Qt.AlignRight)
    box.addWidget(btn2, 1, Qt.AlignLeft | Qt.AlignRight)
    box.addWidget(btn3, 2, Qt.AlignLeft | Qt.AlignRight)

    centralWidget.setLayout(box)
    pm.setCentralWidget(centralWidget)
    pm.show()
    app.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main(app)
    #app = QApplication(sys.argv)
    #window = MainWindow()
    #window.show()
    #sys.exit(app.exec_())
