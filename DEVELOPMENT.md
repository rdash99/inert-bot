# setting up dev enviroment

## Virtual env
install
```bash
pip install virtualenv
python3 -m virtualenv venv
```
windows
```cmd
venv\Scripts\activate.bat
```
linux
```bash
source venv/bin/activate
```
## Installing packages
```bash
pip install -e .
```

## .ENV Setup
Create a copy of `default.env` and call the copy `.env`
then edit `.env` and paste your discord bot token on the line called `DISCORD_TOKEN=`

## SQL Server Setup
### docker-compose

requirements:
- Docker is installed
- docker-compose is installed

```bash
docker-compose up -f mysql-compose.yml
```
This will setup a mariadb server running on your computer with the same login details as the can be found in default.env
go to http://localhost:8080 to view web interface

username: "`root`" or "`testacc`"

password: "`password123`"

### Hosting elsewhere

edit the `.env` file and adjust your credentials accodingly so the new server is connected to instead
