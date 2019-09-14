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

### Set passwords

```sh
touch passwords.py | echo "email = <email password> \nuser1 = <user1 password> \nuser2 = <user2 password>" >> passwords.py
```

## Run The App!

```sh
python3 main.py
```

