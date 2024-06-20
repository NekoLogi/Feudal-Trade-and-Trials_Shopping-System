import mysql.connector


class DB:
    def __init__(self, host, username, password, database):
        self.db_host = host
        self.db_username = username
        self.db_password = password
        self.db_database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.db_host,
            user=self.db_username,
            password=self.db_password,
            database=self.db_database
            )

# Banking
    def user_get_by_uuid(self, uuid, username):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM banking WHERE uuid = '{uuid}' AND username = '{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    def user_get_by_pin(self, pin, username):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM banking WHERE password = '{pin}' AND username = '{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    def user_get_by_id(self, id):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM banking WHERE id = {id}"
            cursor.execute(query)
            result = cursor.fetchone()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    def user_create(self, uuid, username, password, balance):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"INSERT INTO banking (uuid, username, password, balance) VALUES ('{uuid}', '{username}', '{password}', {balance})"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False
    
    def user_remove(self, uuid, username):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"DELETE FROM banking WHERE uuid = '{uuid}' AND username = '{username}'"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def user_set_balance_by_uuid(self, uuid, username, amount):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"UPDATE banking SET balance = {amount} WHERE uuid = '{uuid}' AND username = '{username}'"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def user_set_balance_by_id(self, id, amount):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"UPDATE banking SET balance = {amount} WHERE id = {id}"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def user_transfer(self, uuid, from_user, to_id, amount):
        if amount <= 0:
            print("Amount to send is negative or zero!")
            return False
        sender = self.user_get_by_uuid(uuid, from_user)
        if not sender:
            print("User not found!")
            return False
        if sender['balance'] < amount:
            print("Not enough balance to transfer!")
            return False
        
        receiver = self.user_get_by_id(to_id)
        if not receiver:
            print("User not found by this id!")
            return False
        
        self.user_set_balance_by_uuid(uuid, from_user, (sender['balance'] - amount))
        self.user_set_balance_by_id(to_id, (receiver['balance'] + amount))       
        return True

    def user_deposit(self, uuid, username, amount):
        if amount <= 0:
            print("Amount is negative or zero!")
            return False
        sender = self.user_get_by_uuid(uuid, username)
        if not sender:
            print("User not found!")
            return False
                
        self.user_set_balance_by_uuid(uuid, username, (sender['balance'] + amount))
        return True

    def user_withdraw(self, uuid, username, amount):
        if amount <= 0:
            print("Amount is negative or zero!")
            return False
        sender = self.user_get_by_uuid(uuid, username)
        if not sender:
            print("User not found!")
            return False
        if sender['balance'] < amount:
            print("Not enough balance to transfer!")
            return False
                
        self.user_set_balance_by_uuid(uuid, username, (sender['balance'] - amount))
        return True


# Shop
    def shop_get_item_count(self):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT COUNT(*) FROM shop"
            cursor.execute(query)
            count = cursor.fetchall()[0]["COUNT(*)"]
            print(count)
            return count
        except mysql.connector.Error as err:
            print(err.msg)
        except Exception as err:
            print(err)
        return None

    def shop_item_create(self, tier, display_name, name):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            cursor.execute(f"INSERT INTO shop (tier, displayname, name) VALUES ({tier}, '{display_name}', '{name}')")
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def shop_get_item_by_name(self, name):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM shop WHERE name = '{name}'"
            cursor.execute(query)
            result = cursor.fetchone()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None
    
    def shop_get_item_by_tier(self, tier):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM shop WHERE tier = '{tier}' AND recycled = TRUE"
            cursor.execute(query)
            result = cursor.fetchall()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    def shop_get_all_items(self):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM shop"
            cursor.execute(query)
            result = cursor.fetchall()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    def shop_item_remove(self, name):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"DELETE FROM shop WHERE name = '{name}'"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def shop_set_tier(self, name, tier):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"UPDATE shop SET tier = {tier} WHERE name = '{name}'"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def shop_item_recycled(self, name):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"UPDATE shop SET recycled = TRUE WHERE name = '{name}'"
            cursor.execute(query)
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

# Item Roller
    def roller_item_add(self, id, amount, sale):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            cursor.execute(f"INSERT INTO itemroll (name, amount, sale) VALUES ('{id}', {amount}, {sale})")
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def roller_item_get(self, name):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM itemroll WHERE name = '{name}'"
            cursor.execute(query)
            result = cursor.fetchone()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None

    def roller_table_delete(self):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            cursor.execute(f"DROP TABLE itemroll")
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def roller_table_create(self):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            cursor.execute(f"CREATE TABLE itemroll (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, amount INT NOT NULL DEFAULT 0, sale INT NOT NULL DEFAULT 0, UNIQUE(name))")
            db.commit()
            self.disconnect(db)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def roller_get_all_items(self):
        try:
            db = self.connect()
            cursor = db.cursor(dictionary=True)
            query = f"SELECT * FROM itemroll"
            cursor.execute(query)
            result = cursor.fetchall()
            self.disconnect(db)
            return result
        except mysql.connector.Error as err:
            print(err.msg)
            return None




    def disconnect(self, db):
        if db.is_connected():
            db.close()


