from utils.Database import Database


class Billing:

    @staticmethod
    def get_billing_rows():
        billing_rows = []

        query = """
            SELECT DISTINCT
                [BillingMonth],
                [BillingYear]
            FROM 
                [StoreManagement].[itm].[DepartmentCosts]
            ORDER BY
            [BillingYear] DESC, [BillingMonth] DESC
            """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if len(rows) != 0:
            for row in rows:
                billing_row = Billing()
                billing_row.set_billing_month(row[0])
                billing_row.set_billing_year(row[1])
                billing_rows.append(billing_row)

        return billing_rows

    @staticmethod
    def get_department_billing(year, month):
        department_billing = []
        
        query = f"""
            SELECT 
                [DepartmentCode],
                [Total Price]
            FROM 
                [StoreManagement].[itm].[DepartmentCosts]
            WHERE
                [BillingYear] = {year}
                AND
                [BillingMonth] = {month}
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if len(rows) != 0:
            for row in rows:
                department = Billing()
                department.set_department_code(row[0])
                department.set_total(row[1])
                department_billing.append(department)

        return department_billing

    @staticmethod
    def get_billing_month_name(month):
        switcher = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        return switcher.get(month, "Invalid Month")

    def __init__(self):
        self.department_code = None
        self.billing_info = {}
        return

    def set_department_code(self, department_code):
        self.department_code = department_code
        return self

    def get_department_code(self):
        return self.department_code

    def set_billing_month(self, billing_month):
        self.billing_info['billing_month'] = billing_month
        return self

    def get_billing_month(self):
        return self.billing_info['billing_month']

    def set_billing_year(self, billing_year):
        self.billing_info['billing_year'] = billing_year
        return self

    def get_billing_year(self):
        return self.billing_info['billing_year']

    def set_total(self, total):
        self.billing_info['total'] = total
        return self

    def get_total(self):
        return self.billing_info['total']
