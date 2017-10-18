import vk
import MySQLdb
from config import *
def get_id():
    connection = MySQLdb.connect( MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, charset='utf8',use_unicode = True)
    cursor = connection.cursor()
    cursor.execute( "SELECT vk_id FROM user;")
    vk_id = cursor.fetchall()
    vk_id = [ int( each[0] ) for each in vk_id ]
    connection.close()
    return vk_id

def get_info():
    session = vk.Session(access_token=token )
    vk_api = vk.API(session)
