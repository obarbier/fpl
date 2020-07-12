import click

HOST = click.option("--host", "-h", metavar="HOST", default="127.0.0.1",
                    help="The network address to listen on (default: 127.0.0.1). "
                         "Use 0.0.0.0 to bind to all addresses if you want to access the tracking "
                         "server from other machines.")

PORT = click.option("--port", "-p", default=5000,
                    help="The port to listen on (default: 5000).")

_INITYPE = {"1":"initFile", "2": "Vault"}
_REFRESH_DATA={"1":"6 hours" , "2":"12 hours", "3":"24 hours" }
_DBTYPE = {"1":"mongo DB" , "2":"postgreSQL"}
USERNAME = click.option("--username", "-U",prompt="Username needed to Login to FPL: ", type=click.STRING)
PASSWORD = click.option( "--password", "-P", prompt="Password needed to Login to FPL: ", type=click.STRING, confirmation_prompt=True ,hide_input=True)
INITYPE = click.option("--initype", "-I",prompt="How to Save Metada: "+ str(_INITYPE), type=click.Choice(_INITYPE.keys()))
REFRESH_DATA  = click.option("--refresh", "-R", prompt="How often FPL Data will be updated: " + str(_REFRESH_DATA), type=click.Choice(_REFRESH_DATA.keys()) )
DBTYPE = click.option("--dbtype", "-d",prompt="DB type that will be used: "+ str(_DBTYPE),type=click.Choice(_DBTYPE.keys()))
DATABASEURL = click.option("--dburl",prompt="DBURL:", type=click.STRING) 
DATABASEPASSWORD = click.option("--dbpass",prompt="DB password:", type=click.STRING, confirmation_prompt=True ,hide_input=True) 