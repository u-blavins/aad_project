from utils import Database

class Item:
    """ Item Model """

    @staticmethod
    def get_all_items():
        query = """
            SELECT [Code],
            [Name],
            [UnitName],
            [Risk],
            [Price]
            FROM [itm].[Item]
        """
        rows = Database.execute_query(query)
        items = []

        for row in rows:
            item = Item()
            item.set_code(row[0])
            item.set_name(row[1])
            item.set_unit_name(row[2])
            item.set_risk(row[3])
            item.set_price(row[4])
            items.append(item)

        return items

    @staticmethod
    def get_item(code):
        item = None

        query = """
        SELECT [Code], [Name], [UnitName], [Risk], [Price] FROM
        [itm].[Item] WHERE [Code] = '%s'
        """ % code

        rows = Database.execute_query(query)

        for row in rows:
            item = Item()
            item.set_code(row[0])
            item.set_name(row[1])
            item.set_unit_name(row[2])
            item.set_risk(row[3])
            item.set_price(row[4])
        
        return item

    def __init__(self):
        self.code = None
        self.item = {}
        return
    
    def set_code(self, code):
        self.code = code
        return self
    
    def get_code(self):
        return self.code

    def set_name(self, name):
        self.item['name'] = name
        return self

    def get_name(self):
        return self.item['name']
    
    def set_unit_name(self, unit):
        self.item['unit_name'] = unit
        return self

    def get_unit_name(self):
        return self.item['unit_name']

    def set_risk(self, risk):
        self.item['risk'] = risk
        return self
    
    def get_risk(self):
        return self.item['risk']

    def set_price(self, price):
        self.item['price'] = price
        return self
    
    def get_price(self):
        return self.item['price']