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

modulelist = ["datetime", "sys", "os", "PyQt5", "matplotlib",  "json", "configparser"]


def check_modules():
    not_found = 0
    for package in modulelist:
        try:
            __import__(package)
            dots = "." * (25 - (len(package) + 2))
            print(f"{package}{dots}OK")
        except ModuleNotFoundError:
            not_found += 1
            dots = "." * (25 - (len(package) + 5))
            print(f"{package}{dots}NOT FOUND")
    print("")
    if not_found > 0:
        print("Modules not found must be installed for the program to work. Program will exit now. ")
    else:
        print("All necessary modules are installed. Program will exit now.")
    input("Press enter to continue.")
    exit()


if __name__ == '__main__':
    check_modules()
