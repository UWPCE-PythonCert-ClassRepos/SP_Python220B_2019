"""create source file for lesson8"""

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals
# pylint: disable=W0612 # too many variables

from csv import writer


class BuildCsvFile:
    """build csv file
    csv_file, full filename including path
    rows_to_add, count of rows to add to the file
    """

    def __init__(self, invoice_file, customer_name, item_code, item_description,
                 item_monthly_price):
        self.invoice_file = invoice_file
        self.customer_name = customer_name
        self.item_code = item_code
        self.item_description = item_description
        self.item_monthly_price = item_monthly_price


    def add_rows(self):
        """add rows to the csv file"""

        row_contents = [self.customer_name, self.item_code,
                        self.item_description, self.item_monthly_price]
        with open(self.invoice_file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(row_contents)
