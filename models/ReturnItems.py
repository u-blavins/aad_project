from utils.Database import Database
from utils import Basket as ReturnControl

from models.Item import Item as ItemModel


class ReturnItems:
    """ Return Items Model """

    def __init__(self):
        self.returns = {}
        self.valid_codes = ItemModel.get_codes()
        return

    def set_returns(self, item, quantity, unit, option):
        message = ''
        if option not in self.returns:
            self.returns[option] = {}
        if item in self.valid_codes:
            if unit in ItemModel.get_unit_types(item):
                if item not in self.returns[option]:
                    resp = ReturnControl.get_return_quantity(item, unit, quantity, 0)
                    if resp['Status'] == 200:
                        self.returns[option][item] = {
                            'units': {unit: quantity}, 'quantity': resp['Info']}
                    else:
                        message = resp['Info']
                else:
                    resp = ReturnControl.get_return_quantity(item, unit, quantity,
                        self.returns[option][item]['quantity'])
                    if resp['Status'] == 200:
                        if unit not in self.returns[option][item]['units']:
                            self.returns[option][item]['units'][unit] = quantity
                        else:
                            self.returns[option][item]['units'][unit] += quantity
                        self.returns[option][item]['quantity'] = resp['Info']
                    else:
                        message = resp['Info']
            else: 
                message = f"{item} does not have a unit type of {unit}"
        else:
            message = f'{item} is not a valid item'             
        return message

    def get_returns(self):
        return self.returns

    def return_items(self, user_id, staff_id):
        message = ''
        for option in self.returns:
            if option == 'refund':
                self.handle_returns(user_id, self.returns[option], 1)
                message = 'Successfully refunded items'
            if option == 'broken':
                self.handle_returns(user_id, self.returns[option], 1)
                self.handle_returns(staff_id, self.returns[option], 0)
                message = 'Successfully refunded broken items'
        if 'refund' in self.returns and 'broken' in self.returns:
            message = 'Successfully returned item(s) and broken item(s)'
        return message

    def handle_returns(self, user_id, items, is_return):
        if items != {}:
            conn = Database.connect()
            cursor = conn.cursor()
            price = ReturnControl.get_price(items)
            sproc = """
            [itm].[createTransaction] @UserID = ?, @Price = ?, @isRefund = ?"""
            params = (user_id, price, is_return)
            trans_id = Database.execute_sproc(sproc, params, cursor)
            cursor.commit()
            for item in items:
                for unit in items[item]['units']:
                    sproc = """
                        [itm].[createTransactionInfo] @ItemCode = ?, @TransactionID = ?, @UnitName = ?,
                        @Quantity = ?
                    """
                    params = (
                        item, trans_id[0][0], unit, items[item]['units'][unit]
                    )
                    result = Database.execute_sproc(sproc, params, cursor)
                    cursor.commit()
            conn.close()
