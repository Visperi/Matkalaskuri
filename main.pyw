"""
Copyright (C) 2018-2019  Visperi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import sys
import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QInputDialog, \
    QMessageBox, QCalendarWidget, QLineEdit, QGridLayout, QMainWindow, QAction, QShortcut, QFileDialog
from PyQt5.QtGui import QIcon, QDoubleValidator, QCloseEvent, QKeySequence
from PyQt5.QtCore import QDate, QTimer
import matplotlib.pyplot as plt
import json
import configparser

config = configparser.ConfigParser()
mainpath = "{}\\".format(os.path.dirname(os.path.abspath(__file__)))
if mainpath == "\\":
    mainpath = ""
filepath = f"{mainpath}User_files\\"


# noinspection PyArgumentList,PyCallByClass,PyTypeChecker
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainwidget = QWidget()
        self.setWindowTitle("Matkalaskuri")
        self.setGeometry(300, 300, 300, 150)
        self.setWindowIcon(QIcon(f"{mainpath}icon.ico"))
        self.goal_lbl = QLabel("Jokin meni pieleen tietojen hankinnassa", self)
        self.status_lbl = QLabel("")
        self.menubar = None
        self.menubarshortcut = None
        self.file_window = None
        self.name_edit = None
        self.goalform = None
        self.dist_edit = None
        self.date_edit = None
        self.calendarwindow = None
        self.cal = None
        self.cal_label = None
        self.date = None
        self.timer = None

        self.update_goalinfo()
        self.init_mainwidget()
        self.init_ui()

    def init_mainwidget(self):
        """
        Tekee näppäimet pääwidgettiin ja määrittelee mitä niitä klikatessa tapahtuu. Tämän jälkeen asettelee näppäimet
        vasempaan yläkulmaan, tavoitetiedot oikeaan yläkulmaan ja poistumisnäppäimen oikeaan alakulmaan.
        """

        add_trip = QPushButton("Lisää matka", self)
        add_trip.clicked.connect(self.add_trip)

        inspect_btn = QPushButton("Tarkastele matkoja", self)
        inspect_btn.clicked.connect(self.inspect_trips)

        plot_btn = QPushButton("Piirrä Kuvaaja", self)
        plot_btn.clicked.connect(self.plot_trips)

        goal_btn = QPushButton("Aseta tavoite", self)
        goal_btn.clicked.connect(self.set_goal)

        quit_btn = QPushButton("Poistu", self)
        quit_btn.clicked.connect(QApplication.instance().quit)

        # Ikkunan asettelu
        hbox = QHBoxLayout()
        hbox.addWidget(self.status_lbl)
        hbox.addStretch()
        hbox.addWidget(quit_btn)

        buttons = QVBoxLayout()
        buttons.addWidget(add_trip)
        buttons.addWidget(inspect_btn)
        buttons.addWidget(plot_btn)
        buttons.addWidget(goal_btn)

        hlayout = QHBoxLayout()
        hlayout.addLayout(buttons)
        hlayout.addStretch()
        hlayout.addWidget(self.goal_lbl)

        vbox = QVBoxLayout()
        vbox.addLayout(hlayout)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.mainwidget.setLayout(vbox)

    def init_ui(self):
        """
        Lisää pääwidgetin pääikkunaan ja näyttää käyttöliittymän.
        """
        self.menubar = self.menuBar()
        self.menubarshortcut = QShortcut(QKeySequence("Alt+M"), self)
        filemenu = self.menubar.addMenu("Tiedosto")
        viewmenu = self.menubar.addMenu("Näytä")
        helpmenu = self.menubar.addMenu("Help")

        view_goalinfo = QAction("Tavoitetiedot", self, checkable=True)
        view_goalinfo.setChecked(True)
        view_goalinfo.triggered.connect(self.toggle_goalinfo)

        about_btn = QAction("About", self)
        about_btn.triggered.connect(self.program_info)

        exit_btn = QAction("Poistu", self)
        exit_btn.setShortcut("Ctrl+Q")
        exit_btn.triggered.connect(self.close)

        refresh_btn = QAction("Päivitä tiedot", self)
        refresh_btn.setShortcut("Ctrl+R")
        refresh_btn.triggered.connect(self.update_goalinfo)

        new_file_btn = QAction("Uusi tiedosto", self)
        new_file_btn.setShortcut("Ctrl+N")
        new_file_btn.triggered.connect(self.new_file)

        change_file_btn = QAction("Vaihda tiedostoa", self)
        change_file_btn.setShortcut("Ctrl+C")
        change_file_btn.triggered.connect(self.change_file)

        filemenu.addAction(refresh_btn)
        filemenu.addAction(new_file_btn)
        filemenu.addAction(change_file_btn)
        filemenu.addAction(exit_btn)
        viewmenu.addAction(view_goalinfo)
        helpmenu.addAction(about_btn)
        self.setCentralWidget(self.mainwidget)
        self.show()

    def toggle_goalinfo(self, state):
        if state:
            self.goal_lbl.show()
        else:
            self.goal_lbl.hide()

    def add_trip(self):
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        trip, ok_pressed = QInputDialog.getDouble(self, "Lisää matka", "Anna matka kilometreinä", 0, 0.1, 1000, 1)
        if ok_pressed:
            trip_to_file(trip, current_date)
            self.update_goalinfo()
            QMessageBox.information(self, "Lisääminen onnistui",
                                    f"Lisättiin matka: {current_date}: {trip} km", QMessageBox.Ok)

    def inspect_trips(self, get_total=False):
        total_dist = 0
        total_trips = 0
        total_dates = 0
        max_trips = []
        min_trips = []
        date_totals = []
        with open(f"{filepath}cycling_trips.json") as data_file:
            data = json.load(data_file)
        if not get_total and len(data.keys()) <= 2:
            QMessageBox.warning(self, "Ei dataa", "Matkoihisi ei ole vielä kirjattu yhtään matkaa.", QMessageBox.Ok)
            return
        for date in data:
            if date == "_comment" or date == "goals":
                continue
            total_dates += 1
            total_dist += sum(data[date])
            total_trips += len(data[date])
            date_totals.append(round(sum(data[date]), 2))
            max_trips.append(max(data[date]))
            min_trips.append(min(data[date]))
        if get_total:
            return total_dist
        QMessageBox.about(self, "Tarkastele matkoja", f"Matkojen pituus yhteensä: {round(total_dist, 2)} km\n"
                                                      f"Pisin yksittäinen matka: {max(max_trips)} km\n"
                                                      f"Lyhin yksittäinen matka: {min(min_trips)} km\n"
                                                      f"Päiväennätys: {max(date_totals)} km\n\n"
                                                      f"Matkoja kirjattu yhteensä: {total_trips}\n"
                                                      f"Päiviä kirjattu yhteensä: {total_dates}")

    def plot_trips(self):
        dates = []
        distances = []
        with open(f"{filepath}cycling_trips.json") as data_file:
            data = json.load(data_file)
        if len(data) <= 2:
            QMessageBox.warning(self, "Liian vähän dataa", "Tiedostoihin täytyy olla kirjattu vähintään kahden päivän "
                                                           "matkat kuvaajan piirtämiseksi.", QMessageBox.Ok)
            return
        for date in data:
            if date == "_comment":
                continue
            dates.append(date)
            distances.append(round(sum(data[date]), 2))
        plt.plot(dates, distances)
        plt.ylim(0, max(distances) + 1)
        plt.xlabel("Päivämäärä"), plt.ylabel("Kokonaismatka [km]"), plt.title("Kaikki lenkit")
        plt.show()

    def new_file(self):

        def make_file():
            new_file_name = self.name_edit.text()
            default_extensions = []
            if new_file_name == "":
                trip_files = os.listdir(filepath)
                for file in trip_files:
                    if file.startswith("cycling_trips") and len(file) <= 20 and file.endswith(".json"):
                        file_stripped = file.replace(".json", "")
                        if file_stripped[-1].isdigit():
                            default_extensions.append(int(file_stripped[-1]))
                if len(default_extensions) == 0:
                    new_file_name = "cycling_trips2"
                else:
                    new_file_name = f"cycling_trips{max(default_extensions) + 1}"
            new_file_path = f"{filepath}{new_file_name}.json"
            file_exists = os.path.isfile(f"{new_file_path}")
            if file_exists:
                msgbox = QMessageBox(self)
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setWindowTitle("Tiedosto on jo olemassa")
                msgbox.setGeometry(600, 300, 100, 100)
                msgbox.setText("Samalla nimellä on jo olemassa tiedosto. Haluatko korvata sen uudella?")
                msgbox.setStandardButtons(QMessageBox.Ok)
                cancel_btn2 = msgbox.addButton("Peruuta", QMessageBox.ActionRole)
                signal = msgbox.exec_()
                if signal == QMessageBox.Ok:
                    pass
                elif msgbox.clickedButton() == cancel_btn2:
                    QCloseEvent()
                    return
            with open(new_file_path, "w") as data_file:
                data = {"_comment": "All trips are stored in this file. They must be in format dd.mm.yyyy: "
                                    "[float, float, ...]", "goals": {"distance": "", "date": ""}}
                json.dump(data, data_file, indent=4)
            QMessageBox.information(self, "Uusi matkatiedosto",
                                    f"Tehtiin uusi tiedosto nimellä {new_file_name}", QMessageBox.Ok)
            self.file_window.close()

        self.file_window = QWidget()
        filename = QLabel("Anna tiedostolle nimi")

        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(20)

        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(make_file)
        cancel_btn = QPushButton("Peruuta")
        cancel_btn.clicked.connect(self.file_window.close)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(filename, 1, 0)
        grid.addWidget(self.name_edit, 1, 1)

        info_lbl = QLabel("Jos jätät kentän tyhjäksi, annetaan tiedostolle oletusnimi")

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(info_lbl)
        vbox.addLayout(grid)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.file_window.setLayout(vbox)
        self.file_window.setGeometry(600, 300, 300, 50)
        self.file_window.setWindowTitle("Uusi matkatiedosto")
        self.file_window.setWindowIcon(QIcon(f"{mainpath}icon.ico"))
        self.file_window.show()

    def change_file(self):
        import ntpath
        filename, _ = QFileDialog.getOpenFileName(self, "Vaihda tiedostoa", f"{filepath}", "Json Files (*.json)")
        if filename:
            filename = ntpath.basename(filename)
            config.read(f"{mainpath}settings.ini")
            config["current"]["filename"] = filename
            with open(f"{mainpath}settings.ini", "w") as configfile:
                config.write(configfile)
                configfile.close()
            self.update_goalinfo(new_file=True)

    def set_goal(self):
        self.goalform = QWidget()
        goal_dist = QLabel("Kilometrimäärä")
        goal_date = QLabel("Tavoitepäivämäärä")

        self.dist_edit = QLineEdit()
        self.dist_edit.setValidator(QDoubleValidator())
        self.dist_edit.setMaxLength(5)
        self.date_edit = QLineEdit()
        self.date_edit.setDisabled(True)
        open_calendar = QPushButton("")
        open_calendar.setIcon(QIcon(f"{mainpath}calendar.png"))
        open_calendar.clicked.connect(self.open_calendar)

        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(self.confirm)
        cancel_btn = QPushButton("Peruuta")
        cancel_btn.clicked.connect(self.goalform.close)

        info_lbl = QLabel("Voit antaa sekä matkan että päivämäärän tai jättää kumman tahansa tyhjäksi.")

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(goal_dist, 1, 0)
        grid.addWidget(self.dist_edit, 1, 1)
        grid.addWidget(goal_date, 2, 0)
        grid.addWidget(self.date_edit, 2, 1)
        grid.addWidget(open_calendar, 2, 2)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(info_lbl)
        vbox.addLayout(grid)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.goalform.setLayout(vbox)
        self.goalform.setWindowIcon(QIcon(f"{mainpath}icon.ico"))
        self.goalform.setWindowTitle("Aseta tavoite")
        self.goalform.setGeometry(600, 300, 100, 100)
        self.goalform.show()

    def confirm(self):
        dist = self.dist_edit.text()
        date = self.date_edit.text()
        config.read(f"{mainpath}settings.ini")
        filename = config["current"]["filename"]
        with open(f"{filepath}{filename}") as data_file:
            data = json.load(data_file)
        goal_dist, goal_date = data["goals"]["distance"], data["goals"]["date"]
        if goal_dist != "" or goal_date != "":
            msgbox = QMessageBox(self)
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle("Varmista tavoitteen tallennus")
            msgbox.setGeometry(600, 300, 100, 100)
            msgbox.setText(f"Sinulla on jo tavoite.\n\n"
                           f"Matka: {goal_dist} km\nPäivämäärä: {goal_date}\n\n"
                           f"Haluatko nollata sen ja lisätä uuden tavoitteen?")
            msgbox.setStandardButtons(QMessageBox.Ok)
            cancel_btn = msgbox.addButton("Peruuta", QMessageBox.ActionRole)
            signal = msgbox.exec_()
            if signal == QMessageBox.Ok:
                goal_to_file(dist, date, filename)
                self.goalform.close()
                self.update_goalinfo()
            elif msgbox.clickedButton() == cancel_btn:
                QCloseEvent()
        else:
            goal_to_file(dist, date, filename)
            self.goalform.close()
            self.update_goalinfo()

    # noinspection PyUnresolvedReferences
    def open_calendar(self):
        self.calendarwindow = QWidget()
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.show_date)

        self.cal_label = QLabel(self)
        self.date = self.cal.selectedDate()
        self.cal_label.setText(self.date.toPyDate().strftime("%d.%m.%Y"))

        choose_btn = QPushButton("Valitse")
        choose_btn.clicked.connect(self.set_date)
        cancel_btn = QPushButton("Peruuta")
        cancel_btn.clicked.connect(self.calendarwindow.close)

        # Ikkunan asettelu
        hbox = QHBoxLayout()
        hbox.addWidget(self.cal_label)
        hbox.addStretch()
        hbox.addWidget(choose_btn)
        hbox.addWidget(cancel_btn)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.cal)
        vbox.addLayout(hbox)

        self.calendarwindow.setLayout(vbox)
        self.calendarwindow.setGeometry(600, 300, 300, 200)
        self.calendarwindow.setWindowTitle("Valitse päivämäärä")
        self.calendarwindow.setWindowIcon(QIcon(f"{mainpath}icon.ico"))
        self.calendarwindow.show()

    def show_date(self, date):
        self.cal_label.setText(date.toPyDate().strftime("%d.%m.%Y"))

    def set_date(self):
        self.date_edit.setText(self.cal_label.text())
        self.calendarwindow.close()

    def update_goalinfo(self, new_file=False):
        date_fmt = "%d.%m.%Y"
        config.read(f"{mainpath}settings.ini")
        current_file = config["current"]["filename"]
        try:
            with open(f"{filepath}{current_file}") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            if not os.path.exists(filepath):
                os.mkdir("User_files")
            with open(f"{filepath}{current_file}", "w") as outfile:
                data = {"_comment": "All trips are stored in this file. They must be in format dd.mm.yyyy: "
                                    "[float, float, ...]", "goals": {"distance": "", "date": ""}}
                json.dump(data, outfile, indent=4)
            with open(f"{filepath}{current_file}") as data_file:
                data = json.load(data_file)
        current_file = current_file.replace(".json", "")
        goal_dist = data["goals"]["distance"]
        goal_date = data["goals"]["date"]
        curr_dist = self.inspect_trips(get_total=True)
        curr_date = datetime.datetime.now()
        if goal_dist != "":
            dist_diff = float(goal_dist) - curr_dist
            goal_dist = f"{goal_dist} km"
            if dist_diff <= 0:
                dist_diff = f"Tavoite saavutettu {round(abs(dist_diff), 2)} km sitten"
            else:
                dist_diff = f"Tavoitteeseen matkaa: {round(dist_diff, 2)} km"
        else:
            goal_dist = "Ei asetettu"
            dist_diff = "Tavoitteeseen matkaa: -"
        if goal_date != "":
            date_diff = (datetime.datetime.strptime(goal_date, date_fmt) - curr_date).days
            if date_diff <= 0:
                date_diff = f"Tavoitepäivämäärä ylitetty {abs(date_diff)} päivällä"
            else:
                date_diff = f"Tavoitepäivään jäljellä: {date_diff} pv"
        else:
            goal_date = "Ei asetettu"
            date_diff = "Tavoitepäivään jäljellä: -"
        self.goal_lbl.setText(f"Tiedosto: {current_file}\n\n"
                              f"Tavoite: {goal_dist}\n"
                              f"{dist_diff}\n"
                              f"Tavoitepvm: {goal_date}\n"
                              f"{date_diff}")
        if new_file:
            self.status_lbl.setText("Vaihdettiin tiedostoa")
        else:
            self.status_lbl.setText("Päivitettiin tavoitetiedot")
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_statuslabel)
        self.timer.start(2000)

    def clear_statuslabel(self):
        self.status_lbl.setText("")

    def program_info(self):
        QMessageBox.about(self, "About Matkalaskuri", "Matkalaskuri 2.0\n"
                                                      "Copyright (C) 2018-2019  Visperi\n\n"
                                                      "Lisenssi: GNU General Public License v3.0\n"
                                                      "Lähdekoodi: Python 3.6")


def trip_to_file(trip, date):
    file = f"{filepath}cycling_trips.json"
    with open(file) as data_file:
        data = json.load(data_file)
    if date in data:
        data[date].append(trip)
    else:
        data[date] = [trip]
    with open(file, "w") as data_file:
        json.dump(data, data_file, indent=4)


def goal_to_file(dist, date, filename):
    file = f"{filepath}{filename}"
    with open(file) as data_file:
        data = json.load(data_file)
    data["goals"]["distance"] = dist
    data["goals"]["date"] = date
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = App()
    sys.exit(app.exec_())
