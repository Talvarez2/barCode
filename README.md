# barCode

Project built with [python 3.7.4](https://www.python.org/) for Millma Hilados.

## Prerequisites:

* Python > 3.0.0
* pip3

## Setup

* Clone repository
* install dependencies:

	* `pip3 install json`
	* `pip3 install openpyxl`

### Database setup

```sh
touch InventarioMillma.xlsx
```

* set color of product in column C
* set composition of product in column E
* set barcode of product in column F
* set store value of product in column AN

### Set passwords

```sh
touch passwords.py | echo "email = <email password> \nuser1 = <user1 password> \nuser2 = <user2 password>" >> passwords.py
```

## Run The App!

```sh
python3 main.py
```

