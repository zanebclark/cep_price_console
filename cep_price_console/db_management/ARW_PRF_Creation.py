from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import Column, Table, func
from sqlalchemy.sql import case, and_, or_, literal
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.types import Date, DateTime, Integer, Numeric, String, Time
from sqlalchemy.dialects.mysql import LONGTEXT
import cep_price_console.db_management.server_utils as server_utils


# Workbook Filename: C:\Users\zane\PycharmProjects\cep_price_console\data\ARW_PRF_Mapping\ARW_PRF_Definitions_v1
# _03.xlsm

# Timestamp: 2019-07-18 13:53:51


class InformReflection(DeferredReflection, server_utils.mysql_base):
    __abstract__ = True


# noinspection PyPep8Naming
class days_since_last_sale_01_current(server_utils.mysql_base):
    __table__ = Table('days_since_last_sale_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The reference number of the customer who purchased the product'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To Code',
                             comment='The reference code for the Ship To address that the product was sent to on the'
                                     'last invoice for the product. Pair this field with the Product Number and'
                                     'Customer Number fields'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number of the item that was sold to the customer. Pair this field'
                                     'with the Customer Number field to identify the customer that it was sold to.'),
                      Column('Days_Since_Last_Purch',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Purchase',
                             comment='The number of days since the customer last purchased the product. Pair this'
                                     'field with the Customer Number and Product Number fields.'),
                      schema='cpsh')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class days_since_last_sale_02_archive(server_utils.mysql_base):
    __table__ = Table('days_since_last_sale_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The reference number of the customer who purchased the product'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To Code',
                             comment='The reference code for the Ship To address that the product was sent to on the'
                                     'last invoice for the product. Pair this field with the Product Number and'
                                     'Customer Number fields'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number of the item that was sold to the customer. Pair this field'
                                     'with the Customer Number field to identify the customer that it was sold to.'),
                      Column('Days_Since_Last_Purch',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Purchase',
                             comment='The number of days since the customer last purchased the product. Pair this'
                                     'field with the Customer Number and Product Number fields.'),
                      schema='cpsh')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class cust_alias_01_current(server_utils.mysql_base):
    __table__ = Table('cust_alias_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The DDI Part Number'),
                      Column('Cust_Part_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Customer Part Number',
                             comment='The customer part number assigned.'),
                      schema='cust.pn.xref')


# noinspection PyPep8Naming
class cust_alias_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_alias_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The DDI Part Number'),
                      Column('Cust_Part_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Customer Part Number',
                             comment='The customer part number assigned.'),
                      schema='cust.pn.xref')


# noinspection PyPep8Naming
class cust_01_static(server_utils.mysql_base):
    __table__ = Table('cust_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Keyword',
                             String(length=30),
                             nullable=True,
                             doc='Keyword',
                             comment='The customer keyword.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_address_01_current(server_utils.mysql_base):
    __table__ = Table('cust_address_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Address_Line1',
                             String(length=40),
                             nullable=True,
                             doc='Address Line1',
                             comment='The first line of the main company address'),
                      Column('Address_Line2',
                             String(length=40),
                             nullable=True,
                             doc='Address Line2',
                             comment='The second line of the main company address'),
                      Column('Address_Line3',
                             String(length=40),
                             nullable=True,
                             doc='Address Line3',
                             comment='The third line of the main company address'),
                      Column('City',
                             String(length=20),
                             nullable=True,
                             doc='City',
                             comment='The city that is listed in the customer"s main address. This will display both'
                                     'in capital and lower case type.'),
                      Column('State',
                             String(length=5),
                             nullable=True,
                             doc='State',
                             comment='The state of the customer"s main address (Customer Master > Information tab).'),
                      Column('Zip_Code',
                             String(length=10),
                             nullable=True,
                             doc='Zip Code',
                             comment='The zip code of the customer"s main address.'),
                      Column('Country',
                             String(length=30),
                             nullable=True,
                             doc='Country',
                             comment='The country of the customer"s primary address.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_address_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_address_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Address_Line1',
                             String(length=40),
                             nullable=True,
                             doc='Address Line1',
                             comment='The first line of the main company address'),
                      Column('Address_Line2',
                             String(length=40),
                             nullable=True,
                             doc='Address Line2',
                             comment='The second line of the main company address'),
                      Column('Address_Line3',
                             String(length=40),
                             nullable=True,
                             doc='Address Line3',
                             comment='The third line of the main company address'),
                      Column('City',
                             String(length=20),
                             nullable=True,
                             doc='City',
                             comment='The city that is listed in the customer"s main address. This will display both'
                                     'in capital and lower case type.'),
                      Column('State',
                             String(length=5),
                             nullable=True,
                             doc='State',
                             comment='The state of the customer"s main address (Customer Master > Information tab).'),
                      Column('Zip_Code',
                             String(length=10),
                             nullable=True,
                             doc='Zip Code',
                             comment='The zip code of the customer"s main address.'),
                      Column('Country',
                             String(length=30),
                             nullable=True,
                             doc='Country',
                             comment='The country of the customer"s primary address.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_attachments_01_current(server_utils.mysql_base):
    __table__ = Table('cust_attachments_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Attachment_Name',
                             String(length=255),
                             nullable=True,
                             doc='Attachment Name',
                             comment='The name of the attachment file on Customer Master'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_attachments_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_attachments_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Attachment_Name',
                             String(length=255),
                             nullable=True,
                             doc='Attachment Name',
                             comment='The name of the attachment file on Customer Master'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_credit_01_current(server_utils.mysql_base):
    __table__ = Table('cust_credit_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Credit_Manager',
                             String(length=14),
                             nullable=True,
                             doc='Credit Manager',
                             comment='The initials of the customer"s Credit Manager.'),
                      Column('Credit_Appl_Year',
                             String(length=16),
                             nullable=True,
                             doc='Credit Appl Year',
                             comment='The Credit Application Year that the customer applied for credit from your'
                                     'company. Listed under the Credit tab in the Customer Master.'),
                      Column('AR_Terms',
                             String(length=8),
                             nullable=True,
                             doc='AR Terms',
                             comment='The reference code for the customer"s terms. For the description and additional'
                                     'terms information, link the report to the terms file.'),
                      Column('AR_Parent_Acct',
                             String(length=17),
                             nullable=True,
                             doc='AR Parent Account',
                             comment='The parent account for the customer'),
                      Column('Master_AR_Acct',
                             String(length=17),
                             nullable=True,
                             doc='Master AR Account',
                             comment='The Customer Number  of the Parent A/R Account. If this is the same as the'
                                     'Customer Number, then a separate Parent Account has not been designated.'),
                      Column('Finance_Chrg_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Finance Charge Percent',
                             comment='The percentage of the total invoice that the customer will be charged if the'
                                     'invoice is not paid in the number of allotted days.'),
                      Column('Credit_Limit',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credit Limit',
                             comment='The customer"s Credit Limit'),
                      Column('Credit_Limit_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credit Limit Dollars',
                             comment='The customer"s credit limit in currency format, allowing this field to be'
                                     'compared against AR Balance or other dollar amount fields.'),
                      Column('Credit_Hold_Max_Inv_Days',
                             Integer,
                             nullable=True,
                             doc='Credit Hold Max Invoice Days',
                             comment='The Open Invoice Number of Days that the customer has to pay before the invoice'
                                     'is considered overdue.'),
                      Column('POS_Open_Inv_Days',
                             Integer,
                             nullable=True,
                             doc='POS Open Invoice Days',
                             comment='Credit hold will check this field and compare it against oldest open invoice,'
                                     'and switch the order to POS if necessary. If this value is blank, credit hold'
                                     'will look at Max Open Invoice # of days and set the order on hold.'),
                      Column('POS_AR_Bal_Limit',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='POS AR Balance Limit',
                             comment='The system will check only the open A/R balance. If they exceed this, sales'
                                     'order entry will be marked Point of Sale.'),
                      Column('Print_Stmnt',
                             String(length=15),
                             nullable=True,
                             doc='Print Statement',
                             comment='The setting for the type of statement that will print for the customer: Y'
                                     'Regular, B  Balance Forward, N  No Statement.'),
                      Column('Personal_Guarantee',
                             String(length=18),
                             nullable=True,
                             doc='Personal Guarantee',
                             comment='This Y/N field indicates if you have a Personal Guarantee for the customer"s'
                                     'credit'),
                      Column('Include_On_Aging',
                             String(length=16),
                             nullable=True,
                             doc='Include On Aging',
                             comment='This Y/N field indicates if the customer is set to be suppressed from the A/R'
                                     'aging report.'),
                      Column('Save_Credit_Card_Info',
                             String(length=21),
                             nullable=True,
                             doc='Save Credit Card Info',
                             comment='This Y/N field indicates if the customer"s information will automatically be'
                                     'saved when they pay by credit card.'),
                      Column('Credit_Card_Level_3',
                             String(length=19),
                             nullable=True,
                             doc='Credit Card Level 3',
                             comment='A Y in this field indicates that Level Three Credit Card Processing has been'
                                     'turned on for this customer.'),
                      Column('POS_Acct',
                             String(length=13),
                             nullable=True,
                             doc='POS Account',
                             comment='This Y/N field indicates if the customer is a Point of Sale Cash Account'),
                      Column('Credit_Limit_By_Ship_To',
                             String(length=23),
                             nullable=True,
                             doc='Credit Limit By Ship To',
                             comment='This Y/N field determines if the ship to will have credit limit.'),
                      Column('Tax_Code',
                             String(length=8),
                             nullable=True,
                             doc='Tax Code',
                             comment='The customer"s default Tax Code. For the description and additional tax'
                                     'information , link the report to the Tax file.'),
                      Column('Tax_Exempt_Num',
                             String(length=20),
                             nullable=True,
                             doc='Tax Exempt Number',
                             comment='The customer"s tax exempt number'),
                      Column('Taxable',
                             String(length=7),
                             nullable=True,
                             doc='Taxable',
                             comment='This Y/N field indicates if the customer is taxable'),
                      Column('Chrg_Acct',
                             String(length=14),
                             nullable=True,
                             doc='Charge Account',
                             comment='This Y/N field indicates if the customer"s account is a sales order charge'
                                     'account'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_credit_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_credit_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Credit_Manager',
                             String(length=14),
                             nullable=True,
                             doc='Credit Manager',
                             comment='The initials of the customer"s Credit Manager.'),
                      Column('Credit_Appl_Year',
                             String(length=16),
                             nullable=True,
                             doc='Credit Appl Year',
                             comment='The Credit Application Year that the customer applied for credit from your'
                                     'company. Listed under the Credit tab in the Customer Master.'),
                      Column('AR_Terms',
                             String(length=8),
                             nullable=True,
                             doc='AR Terms',
                             comment='The reference code for the customer"s terms. For the description and additional'
                                     'terms information, link the report to the terms file.'),
                      Column('AR_Parent_Acct',
                             String(length=17),
                             nullable=True,
                             doc='AR Parent Account',
                             comment='The parent account for the customer'),
                      Column('Master_AR_Acct',
                             String(length=17),
                             nullable=True,
                             doc='Master AR Account',
                             comment='The Customer Number  of the Parent A/R Account. If this is the same as the'
                                     'Customer Number, then a separate Parent Account has not been designated.'),
                      Column('Finance_Chrg_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Finance Charge Percent',
                             comment='The percentage of the total invoice that the customer will be charged if the'
                                     'invoice is not paid in the number of allotted days.'),
                      Column('Credit_Limit',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credit Limit',
                             comment='The customer"s Credit Limit'),
                      Column('Credit_Limit_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credit Limit Dollars',
                             comment='The customer"s credit limit in currency format, allowing this field to be'
                                     'compared against AR Balance or other dollar amount fields.'),
                      Column('Credit_Hold_Max_Inv_Days',
                             Integer,
                             nullable=True,
                             doc='Credit Hold Max Invoice Days',
                             comment='The Open Invoice Number of Days that the customer has to pay before the invoice'
                                     'is considered overdue.'),
                      Column('POS_Open_Inv_Days',
                             Integer,
                             nullable=True,
                             doc='POS Open Invoice Days',
                             comment='Credit hold will check this field and compare it against oldest open invoice,'
                                     'and switch the order to POS if necessary. If this value is blank, credit hold'
                                     'will look at Max Open Invoice # of days and set the order on hold.'),
                      Column('POS_AR_Bal_Limit',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='POS AR Balance Limit',
                             comment='The system will check only the open A/R balance. If they exceed this, sales'
                                     'order entry will be marked Point of Sale.'),
                      Column('Print_Stmnt',
                             String(length=15),
                             nullable=True,
                             doc='Print Statement',
                             comment='The setting for the type of statement that will print for the customer: Y'
                                     'Regular, B  Balance Forward, N  No Statement.'),
                      Column('Personal_Guarantee',
                             String(length=18),
                             nullable=True,
                             doc='Personal Guarantee',
                             comment='This Y/N field indicates if you have a Personal Guarantee for the customer"s'
                                     'credit'),
                      Column('Include_On_Aging',
                             String(length=16),
                             nullable=True,
                             doc='Include On Aging',
                             comment='This Y/N field indicates if the customer is set to be suppressed from the A/R'
                                     'aging report.'),
                      Column('Save_Credit_Card_Info',
                             String(length=21),
                             nullable=True,
                             doc='Save Credit Card Info',
                             comment='This Y/N field indicates if the customer"s information will automatically be'
                                     'saved when they pay by credit card.'),
                      Column('Credit_Card_Level_3',
                             String(length=19),
                             nullable=True,
                             doc='Credit Card Level 3',
                             comment='A Y in this field indicates that Level Three Credit Card Processing has been'
                                     'turned on for this customer.'),
                      Column('POS_Acct',
                             String(length=13),
                             nullable=True,
                             doc='POS Account',
                             comment='This Y/N field indicates if the customer is a Point of Sale Cash Account'),
                      Column('Credit_Limit_By_Ship_To',
                             String(length=23),
                             nullable=True,
                             doc='Credit Limit By Ship To',
                             comment='This Y/N field determines if the ship to will have credit limit.'),
                      Column('Tax_Code',
                             String(length=8),
                             nullable=True,
                             doc='Tax Code',
                             comment='The customer"s default Tax Code. For the description and additional tax'
                                     'information , link the report to the Tax file.'),
                      Column('Tax_Exempt_Num',
                             String(length=20),
                             nullable=True,
                             doc='Tax Exempt Number',
                             comment='The customer"s tax exempt number'),
                      Column('Taxable',
                             String(length=7),
                             nullable=True,
                             doc='Taxable',
                             comment='This Y/N field indicates if the customer is taxable'),
                      Column('Chrg_Acct',
                             String(length=14),
                             nullable=True,
                             doc='Charge Account',
                             comment='This Y/N field indicates if the customer"s account is a sales order charge'
                                     'account'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_freight_01_current(server_utils.mysql_base):
    __table__ = Table('cust_freight_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Freight_Terms',
                             String(length=13),
                             nullable=True,
                             doc='Freight Terms',
                             comment='The customer"s default freight terms.'),
                      Column('Freight_Min_Order_Weight',
                             Integer,
                             nullable=True,
                             doc='Freight Minimum Order Weight',
                             comment='The minimum total weight that an order must meet for the customer to be charged'
                                     'freight.'),
                      Column('UPS_Acct',
                             String(length=255),
                             nullable=True,
                             doc='UPS Account',
                             comment='The customer"s UPS Account Number'),
                      Column('Fedex_Acct_Num',
                             String(length=255),
                             nullable=True,
                             doc='Fedex Account Number',
                             comment='The company"s FedEx account number'),
                      Column('Freight_Terms_Dflt',
                             String(length=21),
                             nullable=True,
                             doc='Freight Terms Default',
                             comment='The default setting in the Prepaid or Collect field, that applies if the'
                                     'customer is set to Prepaid and Bill'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_freight_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_freight_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Freight_Terms',
                             String(length=13),
                             nullable=True,
                             doc='Freight Terms',
                             comment='The customer"s default freight terms.'),
                      Column('Freight_Min_Order_Weight',
                             Integer,
                             nullable=True,
                             doc='Freight Minimum Order Weight',
                             comment='The minimum total weight that an order must meet for the customer to be charged'
                                     'freight.'),
                      Column('UPS_Acct',
                             String(length=255),
                             nullable=True,
                             doc='UPS Account',
                             comment='The customer"s UPS Account Number'),
                      Column('Fedex_Acct_Num',
                             String(length=255),
                             nullable=True,
                             doc='Fedex Account Number',
                             comment='The company"s FedEx account number'),
                      Column('Freight_Terms_Dflt',
                             String(length=21),
                             nullable=True,
                             doc='Freight Terms Default',
                             comment='The default setting in the Prepaid or Collect field, that applies if the'
                                     'customer is set to Prepaid and Bill'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_indices_01_current(server_utils.mysql_base):
    __table__ = Table('cust_indices_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Cust_Indices',
                             String(length=30),
                             nullable=True,
                             doc='Customer Indices',
                             comment='Index entries that are used when searching for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_indices_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_indices_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Cust_Indices',
                             String(length=30),
                             nullable=True,
                             doc='Customer Indices',
                             comment='Index entries that are used when searching for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_inv_message_01_current(server_utils.mysql_base):
    __table__ = Table('cust_inv_message_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Inv_Message',
                             String(length=30),
                             nullable=True,
                             doc='Invoice Message',
                             comment='The default invoice message for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_inv_message_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_inv_message_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Inv_Message',
                             String(length=30),
                             nullable=True,
                             doc='Invoice Message',
                             comment='The default invoice message for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_master_01_current(server_utils.mysql_base):
    __table__ = Table('cust_master_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Cust_Name',
                             String(length=30),
                             nullable=True,
                             index=True,
                             doc='Cust Name',
                             comment='The name of the customer. This will display in all capital letters.'),
                      Column('Bill_To_Attn',
                             String(length=255),
                             nullable=True,
                             doc='Attention Bill To',
                             comment='The individual listed in the Attention field.'),
                      Column('Credit_Status',
                             String(length=13),
                             nullable=True,
                             doc='Credit Status',
                             comment='The customer"s credit status: G = Active/GoodW = WatchC = C.O.D.L = LegalH ='
                                     'HoldA = Cash in AdvanceI = InactiveR = Credit CardS = Point of SaleP = Prospect'),
                      Column('Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Email Address',
                             comment='The main company email address'),
                      Column('Cust_Website',
                             String(length=255),
                             nullable=True,
                             doc='Customer Website',
                             comment='The customer"s website address.'),
                      Column('Fax_Num',
                             String(length=17),
                             nullable=True,
                             doc='Fax Number',
                             comment='The customer"s main tax number.'),
                      Column('Fax_Num_Alt',
                             String(length=20),
                             nullable=True,
                             doc='Alternate Fax Number',
                             comment='The company"s main fax number. It will display as entered in the field, without'
                                     'including the 1, even If it is set to be included when a fax is sent.'),
                      Column('Fax_Num_Formatted',
                             String(length=20),
                             nullable=True,
                             doc='Fax Number Formatted',
                             comment='The company"s main fax number. It will display with the 1 and area code, if'
                                     'they are set to be included.'),
                      Column('Fax_Incl_Area_Code',
                             String(length=18),
                             nullable=True,
                             doc='Fax Incl Area Code',
                             comment='This Y/N field indicates if the customer is set to have the area code included'
                                     'when faxing.'),
                      Column('AR_Contact',
                             String(length=20),
                             nullable=True,
                             doc='AR Contact',
                             comment='The A/R Contact listed for the customer'),
                      Column('AR_Contact_Name',
                             String(length=30),
                             nullable=True,
                             doc='AR Contact Name',
                             comment='The A/R Contact for the customer.'),
                      Column('AR_Phone_Num',
                             String(length=17),
                             nullable=True,
                             doc='AR Phone Number',
                             comment='The A/R Phone listed for the customer.'),
                      Column('Purch_Contact',
                             String(length=20),
                             nullable=True,
                             doc='Purchasing Contact',
                             comment='The name of the Purchasing Contact for the customer, as it will appear on your'
                                     'faxes and emails. Customers without a Purchasing Contact entered will have'
                                     'Customer entered in its place.'),
                      Column('Purch_Contact_Phone',
                             String(length=24),
                             nullable=True,
                             doc='Purchasing Contact Phone',
                             comment='The phone number of the Purchasing Contact for the customer'),
                      Column('Contact_First_Name',
                             String(length=18),
                             nullable=True,
                             doc='Contact First Name',
                             comment='The first name of the purchasing contact for the customer.'),
                      Column('Contact_Last_Name',
                             String(length=17),
                             nullable=True,
                             doc='Contact Last Name',
                             comment='The last name of the purchasing contact.'),
                      Column('Referred_By',
                             String(length=30),
                             nullable=True,
                             doc='Referred By',
                             comment='The Prospect Referred By field'),
                      Column('Prospect_Rating',
                             String(length=15),
                             nullable=True,
                             doc='Prospect Rating',
                             comment='The rating assigned to the prospect.'),
                      Column('Branch',
                             String(length=6),
                             nullable=True,
                             doc='Branch',
                             comment='The reference code for the default branch that the customer is assigned to. For'
                                     'more branch information, link the report to the BRANCH file.'),
                      Column('Salesperson_Code',
                             String(length=16),
                             nullable=True,
                             doc='Salesperson Code',
                             comment='The customer"s salesperson code. For more Salesperson information, link to the'
                                     'SALESMAN file.'),
                      Column('Ship_Via_Code',
                             String(length=13),
                             nullable=True,
                             doc='Ship Via Code',
                             comment='The customer"s default Ship Via code. For more Ship Via information, link to'
                                     'the SHIP.VIA file.'),
                      Column('Cust_Cat',
                             String(length=17),
                             nullable=True,
                             index=True,
                             doc='Customer Category',
                             comment='The reference code for the Customer Category that the customer is assigned to.'
                                     'For more Customer Category information, link the report to the CUST.CATEGORY'
                                     'file.'),
                      Column('Territory',
                             String(length=9),
                             nullable=True,
                             doc='Territory',
                             comment='The territory code for the customer.'),
                      Column('Dflt_Sales_Order_Type',
                             String(length=24),
                             nullable=True,
                             doc='Default Sales Order Type',
                             comment='The reference code for the customer"s default Order Type. For more Order Type'
                                     'information, link the report to the ORDER.TYPE file.'),
                      Column('Parent_Pricing_Acct',
                             String(length=22),
                             nullable=True,
                             doc='Parent Pricing Account',
                             comment='The Customer Number of the Parent Pricing account.'),
                      Column('Dflt_Ship_To_Num',
                             String(length=21),
                             nullable=True,
                             doc='Default Shipto Number',
                             comment='The Ship To number of the default Ship To location for the customer.'),
                      Column('Keyword',
                             String(length=30),
                             nullable=True,
                             doc='Keyword',
                             comment='The customer keyword.'),
                      Column('Cust_Type',
                             String(length=13),
                             nullable=True,
                             doc='Customer Type',
                             comment='The customer type'),
                      Column('Sort_Code',
                             String(length=15),
                             nullable=True,
                             doc='Sort Code',
                             comment='The information that is being used to sort the customer when it appears in a'
                                     'list alphabetically. If you have entered information in to the "Sort Code"'
                                     'field (Customer Master > General tab) for the customer, this information'),
                      Column('Alpha_Sort',
                             String(length=30),
                             nullable=True,
                             doc='Alpha Sort',
                             comment='The information that is being used to sort the customer when it appears in a'
                                     'list alphabetically. If you have entered information in the "Sort Code" field'
                                     '(Customer Master > General tab) for the customer, this information wil'),
                      Column('Cust_Sort',
                             String(length=30),
                             nullable=True,
                             doc='Customer Sort',
                             comment='The information that is being used to sort the customer when it appears in a'
                                     'list alphabetically. If you have entered information in to the "Sort Code"'
                                     'field (Customer Master > General tab) for the customer, this information'),
                      Column('Price_Matrix_Markup_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='P/M Markup %',
                             comment='The customer price matrix markup percent field'),
                      Column('EDI_Acct_Num',
                             String(length=18),
                             nullable=True,
                             doc='EDI Account Number',
                             comment='The customer"s EDI Number'),
                      Column('EDI_Start_Date',
                             Date,
                             nullable=True,
                             doc='EDI Start Date',
                             comment='The customer"s EDI Start Date'),
                      Column('Back_Order_Allow',
                             String(length=16),
                             nullable=True,
                             doc='Back Order Allow',
                             comment='This (Y)es/(N)o field indicates if the customer"s orders are allowed to contain'
                                     'backorders.'),
                      Column('Purch_Order_Req',
                             String(length=23),
                             nullable=True,
                             doc='Purchase Order Required',
                             comment='This Y/N field indicates if a Customer P/O Number is required on Sales Orders'
                                     'for the customer.'),
                      Column('Auto_Margin_Update',
                             String(length=18),
                             nullable=True,
                             doc='Auto Margin Update',
                             comment='This Y/N field indicates if the customer is set to automatically update margin'
                                     'prices.'),
                      Column('Save_SO_Sort_Order',
                             String(length=18),
                             nullable=True,
                             doc='Save SO Sort Order',
                             comment='This Y/N field indicates if the customer is set to save the Sales Order Sort'
                                     'Order.'),
                      Column('Ship_Comp',
                             String(length=13),
                             nullable=True,
                             doc='Ship Complete',
                             comment='This Y/N field indicates if the Ship Complete box is checked for the customer.'
                                     'This field may also appear blank if the box is not checked.'),
                      Column('Show_Inv_Disc',
                             String(length=21),
                             nullable=True,
                             doc='Show Invoice Discount',
                             comment='This Y/N field indicates if the customer is set to display the discount on'
                                     'their invoices.'),
                      Column('Auto_BO_Release',
                             String(length=15),
                             nullable=True,
                             doc='Auto BO Release',
                             comment='This Y/N field indicates if the customer is checked to allow Automatic'
                                     'Backorder Release for their Sales Orders.'),
                      Column('Sort_Shipment_Conf',
                             String(length=26),
                             nullable=True,
                             doc='Sort Shipment Confirmation',
                             comment='This Y/N field indicates if the customer is set to have their Shipment'
                                     'Confirmation sorted.'),
                      Column('Save_Sales_History',
                             String(length=18),
                             nullable=True,
                             doc='Save Sales History',
                             comment='This Y/N field indicates if the customer is set to Maintain Sales History'),
                      Column('Sort_Pick_Ticket',
                             String(length=16),
                             nullable=True,
                             doc='Sort Pick Ticket',
                             comment='This Y/N field indicates if the customer is set to have their Sales Orders'
                                     'sorted.'),
                      Column('Sales_Order_Pricing',
                             String(length=19),
                             nullable=True,
                             doc='Sales Order Pricing',
                             comment='This Y/N field indicates if prices will print on the Sales Orders for the'
                                     'customer.'),
                      Column('Ship_Confirm_Pricing',
                             String(length=20),
                             nullable=True,
                             doc='Ship Confirm Pricing',
                             comment='This Y/N field indicates if the customer is set to print prices on their'
                                     'Shipment Confirmations.'),
                      Column('Auto_Print_MSDS',
                             String(length=15),
                             nullable=True,
                             doc='Auto Print MSDS',
                             comment='Automatically print a MSDS sheet when a sales order is printed.'),
                      Column('Multi_Shipment_Inv',
                             String(length=22),
                             nullable=True,
                             doc='Multi Shipment Invoice',
                             comment='When checked yes, this will not print a customer copy invoice for each'
                                     'individual shipment of an order. The very last shipment will print the complete'
                                     'invoice with all line items and all charges using the original invoice num'),
                      Column('Num_Inv_Copies',
                             Integer,
                             nullable=True,
                             doc='Number Invoice Copies',
                             comment='The number of invoice copies that the customer is set to print by default.'),
                      Column('Coop_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Coop Percent',
                             comment='The Coop Percent that the customer is currently set to receive.'),
                      Column('Commission_Rule__Sales_Or_Paid',
                             String(length=15),
                             nullable=True,
                             doc='Commission Rule  Sales Or Paid',
                             comment='This option refers to the Pay Commission field under the General tab of the'
                                     'Customer Master. This field should only have an entry if you are overriding the'
                                     'setting in the Salesman Commissions based on (S)ales/(P)aid Invoices'),
                      Column('Prod_Cert_Codes',
                             String(length=255),
                             nullable=True,
                             doc='Product Certification Codes',
                             comment='Product Certification Codes'),
                      Column('Send_Order_Conf',
                             String(length=23),
                             nullable=True,
                             doc='Send Order Confirmation',
                             comment='The sending method for the custom"s order confirmations; N = None, Y = Fax, E ='
                                     'Email.'),
                      Column('Separate_Email_Per_Inv',
                             String(length=28),
                             nullable=True,
                             doc='Separate Email Per Invoice',
                             comment='This flag will send each invoice as their own email to the customer accounting'
                                     'contacts. With the flag set to nonblank, all invoices posted for the day for'
                                     'the customer consolidate into 1 PDF/1 Email.'),
                      Column('Send_Inv',
                             String(length=12),
                             nullable=True,
                             doc='Send Invoice',
                             comment='The sending method for the customer"s invoices; N = Print, Y = Fax, E = Email,'
                                     'B = Batch Print Later.'),
                      Column('Send_Inv_Time',
                             Time,
                             nullable=True,
                             doc='Send Invoice Time',
                             comment='The time that any invoices will be faxed to the customer, if they are set to'
                                     'receive them by fax.'),
                      Column('Send_Stmnt',
                             String(length=14),
                             nullable=True,
                             doc='Send Statement',
                             comment='The sending method for the customer"s statement: N = None, Y = Fax, E = Email.'),
                      Column('Send_Cust_Margin_Price_Letter',
                             String(length=33),
                             nullable=True,
                             doc='Send Customer Margin Price Letter',
                             comment='The sending method for the customer"s Price Letter; N = None, Y = Fax, E ='
                                     'Email.'),
                      Column('Int_Notes_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes Flat',
                             comment='The complete text of the internal notes for the customer flattened into a'
                                     'single value. Does not include contact notes.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_master_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_master_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Cust_Name',
                             String(length=30),
                             nullable=True,
                             index=True,
                             doc='Cust Name',
                             comment='The name of the customer. This will display in all capital letters.'),
                      Column('Bill_To_Attn',
                             String(length=255),
                             nullable=True,
                             doc='Attention Bill To',
                             comment='The individual listed in the Attention field.'),
                      Column('Credit_Status',
                             String(length=13),
                             nullable=True,
                             doc='Credit Status',
                             comment='The customer"s credit status: G = Active/GoodW = WatchC = C.O.D.L = LegalH ='
                                     'HoldA = Cash in AdvanceI = InactiveR = Credit CardS = Point of SaleP = Prospect'),
                      Column('Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Email Address',
                             comment='The main company email address'),
                      Column('Cust_Website',
                             String(length=255),
                             nullable=True,
                             doc='Customer Website',
                             comment='The customer"s website address.'),
                      Column('Fax_Num',
                             String(length=17),
                             nullable=True,
                             doc='Fax Number',
                             comment='The customer"s main tax number.'),
                      Column('Fax_Num_Alt',
                             String(length=20),
                             nullable=True,
                             doc='Alternate Fax Number',
                             comment='The company"s main fax number. It will display as entered in the field, without'
                                     'including the 1, even If it is set to be included when a fax is sent.'),
                      Column('Fax_Num_Formatted',
                             String(length=20),
                             nullable=True,
                             doc='Fax Number Formatted',
                             comment='The company"s main fax number. It will display with the 1 and area code, if'
                                     'they are set to be included.'),
                      Column('Fax_Incl_Area_Code',
                             String(length=18),
                             nullable=True,
                             doc='Fax Incl Area Code',
                             comment='This Y/N field indicates if the customer is set to have the area code included'
                                     'when faxing.'),
                      Column('AR_Contact',
                             String(length=20),
                             nullable=True,
                             doc='AR Contact',
                             comment='The A/R Contact listed for the customer'),
                      Column('AR_Contact_Name',
                             String(length=30),
                             nullable=True,
                             doc='AR Contact Name',
                             comment='The A/R Contact for the customer.'),
                      Column('AR_Phone_Num',
                             String(length=17),
                             nullable=True,
                             doc='AR Phone Number',
                             comment='The A/R Phone listed for the customer.'),
                      Column('Purch_Contact',
                             String(length=20),
                             nullable=True,
                             doc='Purchasing Contact',
                             comment='The name of the Purchasing Contact for the customer, as it will appear on your'
                                     'faxes and emails. Customers without a Purchasing Contact entered will have'
                                     'Customer entered in its place.'),
                      Column('Purch_Contact_Phone',
                             String(length=24),
                             nullable=True,
                             doc='Purchasing Contact Phone',
                             comment='The phone number of the Purchasing Contact for the customer'),
                      Column('Contact_First_Name',
                             String(length=18),
                             nullable=True,
                             doc='Contact First Name',
                             comment='The first name of the purchasing contact for the customer.'),
                      Column('Contact_Last_Name',
                             String(length=17),
                             nullable=True,
                             doc='Contact Last Name',
                             comment='The last name of the purchasing contact.'),
                      Column('Referred_By',
                             String(length=30),
                             nullable=True,
                             doc='Referred By',
                             comment='The Prospect Referred By field'),
                      Column('Prospect_Rating',
                             String(length=15),
                             nullable=True,
                             doc='Prospect Rating',
                             comment='The rating assigned to the prospect.'),
                      Column('Branch',
                             String(length=6),
                             nullable=True,
                             doc='Branch',
                             comment='The reference code for the default branch that the customer is assigned to. For'
                                     'more branch information, link the report to the BRANCH file.'),
                      Column('Salesperson_Code',
                             String(length=16),
                             nullable=True,
                             doc='Salesperson Code',
                             comment='The customer"s salesperson code. For more Salesperson information, link to the'
                                     'SALESMAN file.'),
                      Column('Ship_Via_Code',
                             String(length=13),
                             nullable=True,
                             doc='Ship Via Code',
                             comment='The customer"s default Ship Via code. For more Ship Via information, link to'
                                     'the SHIP.VIA file.'),
                      Column('Cust_Cat',
                             String(length=17),
                             nullable=True,
                             index=True,
                             doc='Customer Category',
                             comment='The reference code for the Customer Category that the customer is assigned to.'
                                     'For more Customer Category information, link the report to the CUST.CATEGORY'
                                     'file.'),
                      Column('Territory',
                             String(length=9),
                             nullable=True,
                             doc='Territory',
                             comment='The territory code for the customer.'),
                      Column('Dflt_Sales_Order_Type',
                             String(length=24),
                             nullable=True,
                             doc='Default Sales Order Type',
                             comment='The reference code for the customer"s default Order Type. For more Order Type'
                                     'information, link the report to the ORDER.TYPE file.'),
                      Column('Parent_Pricing_Acct',
                             String(length=22),
                             nullable=True,
                             doc='Parent Pricing Account',
                             comment='The Customer Number of the Parent Pricing account.'),
                      Column('Dflt_Ship_To_Num',
                             String(length=21),
                             nullable=True,
                             doc='Default Shipto Number',
                             comment='The Ship To number of the default Ship To location for the customer.'),
                      Column('Keyword',
                             String(length=30),
                             nullable=True,
                             doc='Keyword',
                             comment='The customer keyword.'),
                      Column('Cust_Type',
                             String(length=13),
                             nullable=True,
                             doc='Customer Type',
                             comment='The customer type'),
                      Column('Sort_Code',
                             String(length=15),
                             nullable=True,
                             doc='Sort Code',
                             comment='The information that is being used to sort the customer when it appears in a'
                                     'list alphabetically. If you have entered information in to the "Sort Code"'
                                     'field (Customer Master > General tab) for the customer, this information'),
                      Column('Alpha_Sort',
                             String(length=30),
                             nullable=True,
                             doc='Alpha Sort',
                             comment='The information that is being used to sort the customer when it appears in a'
                                     'list alphabetically. If you have entered information in the "Sort Code" field'
                                     '(Customer Master > General tab) for the customer, this information wil'),
                      Column('Cust_Sort',
                             String(length=30),
                             nullable=True,
                             doc='Customer Sort',
                             comment='The information that is being used to sort the customer when it appears in a'
                                     'list alphabetically. If you have entered information in to the "Sort Code"'
                                     'field (Customer Master > General tab) for the customer, this information'),
                      Column('Price_Matrix_Markup_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='P/M Markup %',
                             comment='The customer price matrix markup percent field'),
                      Column('EDI_Acct_Num',
                             String(length=18),
                             nullable=True,
                             doc='EDI Account Number',
                             comment='The customer"s EDI Number'),
                      Column('EDI_Start_Date',
                             Date,
                             nullable=True,
                             doc='EDI Start Date',
                             comment='The customer"s EDI Start Date'),
                      Column('Back_Order_Allow',
                             String(length=16),
                             nullable=True,
                             doc='Back Order Allow',
                             comment='This (Y)es/(N)o field indicates if the customer"s orders are allowed to contain'
                                     'backorders.'),
                      Column('Purch_Order_Req',
                             String(length=23),
                             nullable=True,
                             doc='Purchase Order Required',
                             comment='This Y/N field indicates if a Customer P/O Number is required on Sales Orders'
                                     'for the customer.'),
                      Column('Auto_Margin_Update',
                             String(length=18),
                             nullable=True,
                             doc='Auto Margin Update',
                             comment='This Y/N field indicates if the customer is set to automatically update margin'
                                     'prices.'),
                      Column('Save_SO_Sort_Order',
                             String(length=18),
                             nullable=True,
                             doc='Save SO Sort Order',
                             comment='This Y/N field indicates if the customer is set to save the Sales Order Sort'
                                     'Order.'),
                      Column('Ship_Comp',
                             String(length=13),
                             nullable=True,
                             doc='Ship Complete',
                             comment='This Y/N field indicates if the Ship Complete box is checked for the customer.'
                                     'This field may also appear blank if the box is not checked.'),
                      Column('Show_Inv_Disc',
                             String(length=21),
                             nullable=True,
                             doc='Show Invoice Discount',
                             comment='This Y/N field indicates if the customer is set to display the discount on'
                                     'their invoices.'),
                      Column('Auto_BO_Release',
                             String(length=15),
                             nullable=True,
                             doc='Auto BO Release',
                             comment='This Y/N field indicates if the customer is checked to allow Automatic'
                                     'Backorder Release for their Sales Orders.'),
                      Column('Sort_Shipment_Conf',
                             String(length=26),
                             nullable=True,
                             doc='Sort Shipment Confirmation',
                             comment='This Y/N field indicates if the customer is set to have their Shipment'
                                     'Confirmation sorted.'),
                      Column('Save_Sales_History',
                             String(length=18),
                             nullable=True,
                             doc='Save Sales History',
                             comment='This Y/N field indicates if the customer is set to Maintain Sales History'),
                      Column('Sort_Pick_Ticket',
                             String(length=16),
                             nullable=True,
                             doc='Sort Pick Ticket',
                             comment='This Y/N field indicates if the customer is set to have their Sales Orders'
                                     'sorted.'),
                      Column('Sales_Order_Pricing',
                             String(length=19),
                             nullable=True,
                             doc='Sales Order Pricing',
                             comment='This Y/N field indicates if prices will print on the Sales Orders for the'
                                     'customer.'),
                      Column('Ship_Confirm_Pricing',
                             String(length=20),
                             nullable=True,
                             doc='Ship Confirm Pricing',
                             comment='This Y/N field indicates if the customer is set to print prices on their'
                                     'Shipment Confirmations.'),
                      Column('Auto_Print_MSDS',
                             String(length=15),
                             nullable=True,
                             doc='Auto Print MSDS',
                             comment='Automatically print a MSDS sheet when a sales order is printed.'),
                      Column('Multi_Shipment_Inv',
                             String(length=22),
                             nullable=True,
                             doc='Multi Shipment Invoice',
                             comment='When checked yes, this will not print a customer copy invoice for each'
                                     'individual shipment of an order. The very last shipment will print the complete'
                                     'invoice with all line items and all charges using the original invoice num'),
                      Column('Num_Inv_Copies',
                             Integer,
                             nullable=True,
                             doc='Number Invoice Copies',
                             comment='The number of invoice copies that the customer is set to print by default.'),
                      Column('Coop_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Coop Percent',
                             comment='The Coop Percent that the customer is currently set to receive.'),
                      Column('Commission_Rule__Sales_Or_Paid',
                             String(length=15),
                             nullable=True,
                             doc='Commission Rule  Sales Or Paid',
                             comment='This option refers to the Pay Commission field under the General tab of the'
                                     'Customer Master. This field should only have an entry if you are overriding the'
                                     'setting in the Salesman Commissions based on (S)ales/(P)aid Invoices'),
                      Column('Prod_Cert_Codes',
                             String(length=255),
                             nullable=True,
                             doc='Product Certification Codes',
                             comment='Product Certification Codes'),
                      Column('Send_Order_Conf',
                             String(length=23),
                             nullable=True,
                             doc='Send Order Confirmation',
                             comment='The sending method for the custom"s order confirmations; N = None, Y = Fax, E ='
                                     'Email.'),
                      Column('Separate_Email_Per_Inv',
                             String(length=28),
                             nullable=True,
                             doc='Separate Email Per Invoice',
                             comment='This flag will send each invoice as their own email to the customer accounting'
                                     'contacts. With the flag set to nonblank, all invoices posted for the day for'
                                     'the customer consolidate into 1 PDF/1 Email.'),
                      Column('Send_Inv',
                             String(length=12),
                             nullable=True,
                             doc='Send Invoice',
                             comment='The sending method for the customer"s invoices; N = Print, Y = Fax, E = Email,'
                                     'B = Batch Print Later.'),
                      Column('Send_Inv_Time',
                             Time,
                             nullable=True,
                             doc='Send Invoice Time',
                             comment='The time that any invoices will be faxed to the customer, if they are set to'
                                     'receive them by fax.'),
                      Column('Send_Stmnt',
                             String(length=14),
                             nullable=True,
                             doc='Send Statement',
                             comment='The sending method for the customer"s statement: N = None, Y = Fax, E = Email.'),
                      Column('Send_Cust_Margin_Price_Letter',
                             String(length=33),
                             nullable=True,
                             doc='Send Customer Margin Price Letter',
                             comment='The sending method for the customer"s Price Letter; N = None, Y = Fax, E ='
                                     'Email.'),
                      Column('Int_Notes_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes Flat',
                             comment='The complete text of the internal notes for the customer flattened into a'
                                     'single value. Does not include contact notes.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_monthly_01_current(server_utils.mysql_base):
    __table__ = Table('cust_monthly_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Month',
                             Integer,
                             nullable=True,
                             doc='Month',
                             comment='Month in the year (112). Use this field in conjunction with fields This Year'
                                     'Monthly Sales and Last Year Monthly Sales'),
                      Column('This_Year_Monthly_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly Sales',
                             comment='The monthly Sales for the customer for each month of the current calendar year.'
                                     'This field should be paired with the Month field.'),
                      Column('This_Year_Monthly_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly Cost',
                             comment='The monthly Cost for the customer for each month of the current calendar year.'
                                     'This field should be paired with the Month field.'),
                      Column('This_Year_Monthly_GP_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly GP Dollars',
                             comment='The monthly Gross Profit Dollars for the customer for each month of the current'
                                     'calendar year. This field should be paired with the Month field.'),
                      Column('This_Year_Monthly_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly GP Percent',
                             comment='The monthly Gross profit Percentage for the customer for each month of the'
                                     'current calendar year. This field should be paired with the month field.'),
                      Column('Last_Year_Monthly_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly Sales',
                             comment='The monthly Sales for the customer for each month of the previous calendar'
                                     'year. This field should be paired with the Month field.'),
                      Column('Last_Year_Monthly_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly Cost',
                             comment='The monthly Cost for the customer for each month of the previous calendar year.'
                                     'This field should be paired wit the month field.'),
                      Column('Last_Year_Monthly_GP_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly GP Dollars',
                             comment='The monthly Gross Profit Dollars for the customer for each month of the'
                                     'previous calendar year. This field should be paired with the month field.'),
                      Column('Last_Year_Monthly_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly GP Percent',
                             comment='The monthly Gross Profit percent for the customer for each month of the'
                                     'previous calendar year. This field should be paired with the month field.'),
                      Column('Last_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly A/R',
                             comment='The last year"s monthly A/R Totals for the customer.'),
                      Column('This_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly A/R',
                             comment='The current year"s Monthly A/R Totals for the customer.'),
                      Column('Two_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Two Year Monthly A/R',
                             comment='The Two year"s Monthly A/R Totals for the customer.'),
                      Column('Three_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Three Year Monthly A/R',
                             comment='The Three year"s monthly A/R totals for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_monthly_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_monthly_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Month',
                             Integer,
                             nullable=True,
                             doc='Month',
                             comment='Month in the year (112). Use this field in conjunction with fields This Year'
                                     'Monthly Sales and Last Year Monthly Sales'),
                      Column('This_Year_Monthly_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly Sales',
                             comment='The monthly Sales for the customer for each month of the current calendar year.'
                                     'This field should be paired with the Month field.'),
                      Column('This_Year_Monthly_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly Cost',
                             comment='The monthly Cost for the customer for each month of the current calendar year.'
                                     'This field should be paired with the Month field.'),
                      Column('This_Year_Monthly_GP_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly GP Dollars',
                             comment='The monthly Gross Profit Dollars for the customer for each month of the current'
                                     'calendar year. This field should be paired with the Month field.'),
                      Column('This_Year_Monthly_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly GP Percent',
                             comment='The monthly Gross profit Percentage for the customer for each month of the'
                                     'current calendar year. This field should be paired with the month field.'),
                      Column('Last_Year_Monthly_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly Sales',
                             comment='The monthly Sales for the customer for each month of the previous calendar'
                                     'year. This field should be paired with the Month field.'),
                      Column('Last_Year_Monthly_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly Cost',
                             comment='The monthly Cost for the customer for each month of the previous calendar year.'
                                     'This field should be paired wit the month field.'),
                      Column('Last_Year_Monthly_GP_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly GP Dollars',
                             comment='The monthly Gross Profit Dollars for the customer for each month of the'
                                     'previous calendar year. This field should be paired with the month field.'),
                      Column('Last_Year_Monthly_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly GP Percent',
                             comment='The monthly Gross Profit percent for the customer for each month of the'
                                     'previous calendar year. This field should be paired with the month field.'),
                      Column('Last_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Monthly A/R',
                             comment='The last year"s monthly A/R Totals for the customer.'),
                      Column('This_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='This Year Monthly A/R',
                             comment='The current year"s Monthly A/R Totals for the customer.'),
                      Column('Two_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Two Year Monthly A/R',
                             comment='The Two year"s Monthly A/R Totals for the customer.'),
                      Column('Three_Year_Monthly_AR',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Three Year Monthly A/R',
                             comment='The Three year"s monthly A/R totals for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_rank_01_current(server_utils.mysql_base):
    __table__ = Table('cust_rank_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Rank',
                             String(length=4),
                             nullable=True,
                             doc='Rank',
                             comment='The Customer"s letter ranking AD based off of the number of points defined in'
                                     'the Customer Ranking Criteria.'),
                      Column('Rank_Breakdown',
                             String(length=16),
                             nullable=True,
                             doc='Rank Breakdown',
                             comment='The individual letter rank for each rank criteria (Recency, Invoices, Sales,'
                                     'Profit, A.P.D., & Lines Shpd). This field should be paired with Rank'
                                     'Description & Rank Points.'),
                      Column('Rank_Desc',
                             String(length=16),
                             nullable=True,
                             doc='Rank Description',
                             comment='The criteria description (Recency, Invoices, Sales, Profit, A.P.D., & Lines'
                                     'Shpd). This field should be paired with Rank Breakdown and Rank Points.'),
                      Column('Rank_Points',
                             String(length=12),
                             nullable=True,
                             doc='Rank Points',
                             comment='The points earned for each ranking criteria (Recency, Invoices, Sales, Profit,'
                                     'A.P.D., & Lines Shpd). This field should be paired with Rank Description & Rank'
                                     'Breakdown.'),
                      Column('Rank_Total',
                             String(length=11),
                             nullable=True,
                             doc='Rank Total',
                             comment='The total amount of points the customer earned as defined in the Customer'
                                     'Ranking Criteria'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_rank_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_rank_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Rank',
                             String(length=4),
                             nullable=True,
                             doc='Rank',
                             comment='The Customer"s letter ranking AD based off of the number of points defined in'
                                     'the Customer Ranking Criteria.'),
                      Column('Rank_Breakdown',
                             String(length=16),
                             nullable=True,
                             doc='Rank Breakdown',
                             comment='The individual letter rank for each rank criteria (Recency, Invoices, Sales,'
                                     'Profit, A.P.D., & Lines Shpd). This field should be paired with Rank'
                                     'Description & Rank Points.'),
                      Column('Rank_Desc',
                             String(length=16),
                             nullable=True,
                             doc='Rank Description',
                             comment='The criteria description (Recency, Invoices, Sales, Profit, A.P.D., & Lines'
                                     'Shpd). This field should be paired with Rank Breakdown and Rank Points.'),
                      Column('Rank_Points',
                             String(length=12),
                             nullable=True,
                             doc='Rank Points',
                             comment='The points earned for each ranking criteria (Recency, Invoices, Sales, Profit,'
                                     'A.P.D., & Lines Shpd). This field should be paired with Rank Description & Rank'
                                     'Breakdown.'),
                      Column('Rank_Total',
                             String(length=11),
                             nullable=True,
                             doc='Rank Total',
                             comment='The total amount of points the customer earned as defined in the Customer'
                                     'Ranking Criteria'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_restk_policy_01_current(server_utils.mysql_base):
    __table__ = Table('cust_restk_policy_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Misc_Chrg_Code',
                             String(length=25),
                             nullable=True,
                             doc='Miscellaneous Charge Code',
                             comment='The Miscellaneous Charge Code Percent and Taxable status of the customer"s'
                                     'restocking policy. Will not display on one line.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_restk_policy_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_restk_policy_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Misc_Chrg_Code',
                             String(length=25),
                             nullable=True,
                             doc='Miscellaneous Charge Code',
                             comment='The Miscellaneous Charge Code Percent and Taxable status of the customer"s'
                                     'restocking policy. Will not display on one line.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_route_01_current(server_utils.mysql_base):
    __table__ = Table('cust_route_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Route_Stop',
                             String(length=10),
                             nullable=True,
                             doc='Route Stop',
                             comment='The stop number for each of the trucks scheduled. This field should b used in'
                                     'conjunction with the Route Truck field.'),
                      Column('Route_Truck',
                             String(length=20),
                             nullable=True,
                             doc='Route Truck',
                             comment='The trucks (listed in order of scheduled day) that the customer"s orders will'
                                     'be delivered on.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_route_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_route_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Route_Stop',
                             String(length=10),
                             nullable=True,
                             doc='Route Stop',
                             comment='The stop number for each of the trucks scheduled. This field should b used in'
                                     'conjunction with the Route Truck field.'),
                      Column('Route_Truck',
                             String(length=20),
                             nullable=True,
                             doc='Route Truck',
                             comment='The trucks (listed in order of scheduled day) that the customer"s orders will'
                                     'be delivered on.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_so_misc_charge_program_01_current(server_utils.mysql_base):
    __table__ = Table('cust_so_misc_charge_program_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Misc_Chrg_Program_Code',
                             String(length=24),
                             nullable=True,
                             doc='Misc Charge Program Code',
                             comment='The miscellaneous charge program code'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_so_misc_charge_program_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_so_misc_charge_program_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Misc_Chrg_Program_Code',
                             String(length=24),
                             nullable=True,
                             doc='Misc Charge Program Code',
                             comment='The miscellaneous charge program code'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_special_instr_01_current(server_utils.mysql_base):
    __table__ = Table('cust_special_instr_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Dflt_SO_Note',
                             String(length=30),
                             nullable=True,
                             doc='Default SO Note',
                             comment='Special instructions for the customer'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_special_instr_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_special_instr_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Dflt_SO_Note',
                             String(length=30),
                             nullable=True,
                             doc='Default SO Note',
                             comment='Special instructions for the customer'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_stats_01_current(server_utils.mysql_base):
    __table__ = Table('cust_stats_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Prev_Month_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Previous Month Sales',
                             comment='Total Sales for the previous month'),
                      Column('Curr_Month_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Current Month Sales',
                             comment='Total Sales for the current month.'),
                      Column('Sales_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Sales YTD',
                             comment='Total Year-to-date sales for the customer.'),
                      Column('YTD_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='YTD Sales',
                             comment='The customer"s total Year to Date Sales'),
                      Column('Credits_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credits YTD',
                             comment='The customer"s total Year-to-date Credits'),
                      Column('YTD_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='YTD Cost',
                             comment='The customer"s total Year-to-date Cost.'),
                      Column('Cost_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost YTD',
                             comment='Total Year-to-date Cost for the customer.'),
                      Column('GP_Dollars_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Dollars YTD',
                             comment='The customer"s total Year-to-date Gross Profit Dollars.'),
                      Column('GP_Pcnt_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Percent YTD',
                             comment='The customer"s total Year-to-date Gross Profit Percent'),
                      Column('Last_Year_Sales_Year_To_Date',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Sales Year To Date',
                             comment='Last Year to Date Sales for the  customer.'),
                      Column('Last_Year_sales_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year sales (YTD)',
                             comment='Total of last year"s sales up to the current month.'),
                      Column('Last_Year_cost_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year cost (YTD)',
                             comment='Total of last year"s cost up to the current month.'),
                      Column('GP_Dollars_LYTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Dollars LYTD',
                             comment='The customer"s total Last Year-to-Date Gross Profit Dollars.'),
                      Column('GP_Pcnt_LYTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Percent LYTD',
                             comment='The customer"s total Last Year-to-Date Gross Profit Percentage.'),
                      Column('Order_Count_12M',
                             Integer,
                             nullable=True,
                             doc='12M Order Count',
                             comment='The total number of orders entered for the last 12 months. This excludes'
                                     'Quotes, Recurring, and Cancelled orders.'),
                      Column('Inv_Count_12M',
                             Integer,
                             nullable=True,
                             doc='12M Invoice Count',
                             comment='The total number of invoices for the last 12 months.'),
                      Column('Sales_12M',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='12M Sales',
                             comment='The total amount of invoiced sales from the last 12 months'),
                      Column('Cost_12M',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='12M Cost',
                             comment='The total amount of invoiced COGS from the last 12 months.'),
                      Column('GPD_12M',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='12M GPD',
                             comment='The total amount of Gross Profit Dollars from the last 12 months.'),
                      Column('Last_Year_Sales_Total',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Sales Total',
                             comment='Total Last Year Sales for the customer.'),
                      Column('Last_Year_Total_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Total Cost',
                             comment='Total Last Year Cost of the items purchased by the customer.'),
                      Column('Last_Year_Total_GP_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Total GP Dollars',
                             comment='Total Last Year Gross Profit Dollars for the customer.'),
                      Column('Last_Year_Total_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Total GP Percent',
                             comment='Total Last Year Gross Profit Percent for the customer.'),
                      Column('Three_Year_Sales_Total',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Three Year Sales Total',
                             comment='A total of the past 3 years of sales.'),
                      Column('Two_Year_Sales_Total',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Two Year Sales Total',
                             comment='The total sales of the previous calendar year from Jan Dec. For example, if'
                                     'running the report in the year 2017, this would show the total sales of 2016.'),
                      Column('Cust_Sales_Mon_1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 1',
                             comment='Sales for the first month of the current year.'),
                      Column('Cust_Sales_Mon_2',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 2',
                             comment='Sales for the second month of the current year.'),
                      Column('Cust_Sales_Mon_3',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 3',
                             comment='Sales for the third month of the current year.'),
                      Column('Cust_Sales_Mon_4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 4',
                             comment='Sales for the fourth month of the current year.'),
                      Column('Cust_Sales_Mon_5',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 5',
                             comment='Sales for the fifth month of the current year.'),
                      Column('Cust_Sales_Mon_6',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 6',
                             comment='Sales for the sixth month of the current year.'),
                      Column('Cust_Sales_Mon_7',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 7',
                             comment='Sales for the seventh month of the current year.'),
                      Column('Cust_Sales_Mon_8',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 8',
                             comment='Sales for the eighth month of the current year.'),
                      Column('Cust_Sales_Mon_9',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 9',
                             comment='Sales for the ninth month of the current year.'),
                      Column('Cust_Sales_Mon_10',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 10',
                             comment='Sales for the tenth month of the current year.'),
                      Column('Cust_Sales_Mon_11',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 11',
                             comment='Sales for the eleventh month of the current year.'),
                      Column('Cust_Sales_Mon_12',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 12',
                             comment='Sales for the twelfth month of the current year.'),
                      Column('Cust_LYR_Sales_Mon_1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 1',
                             comment='Sales for the first month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_2',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 2',
                             comment='Sales for the second month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_3',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 3',
                             comment='Sales for the third month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 4',
                             comment='Sales for the fourth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_5',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 5',
                             comment='Sales for the fifth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_6',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 6',
                             comment='Sales for the sixth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_7',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 7',
                             comment='Sales for the seventh month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_8',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 8',
                             comment='Sales for the eighth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_9',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 9',
                             comment='Sales for the ninth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_10',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 10',
                             comment='Sales for the tenth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_11',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 11',
                             comment='Sales for the eleventh month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_12',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 12',
                             comment='Sales for the twelfth month of the last year.'),
                      Column('Days_Since_Last_Inv',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Invoice',
                             comment='Number of days since the last time the customer was invoiced.'),
                      Column('Highest_AR_Bal',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Highest AR Balance',
                             comment='The highest A/R balance that the customer had had with you at any point in'
                                     'time.'),
                      Column('Highest_AR_Bal_Date',
                             Date,
                             nullable=True,
                             doc='Highest AR Balance Date',
                             comment='The date of the highest A/R balance for the customer.'),
                      Column('Last_Event_Date',
                             Date,
                             nullable=True,
                             doc='Last Event Date',
                             comment='The most recent event that is linked to the customer (across all contacts).'
                                     'This is based on the events Start Date.'),
                      Column('Last_Inv_Date_1',
                             Date,
                             nullable=True,
                             doc='Last Invoice Date',
                             comment='The invoice date of the customer"s most recent invoice.'),
                      Column('Last_Inv_Date_2',
                             Date,
                             nullable=True,
                             doc='Last Invoice Date',
                             comment='The invoice date of the customer"s most recent invoice.'),
                      Column('Last_Pmnt_Amount',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Payment Amount',
                             comment='The total amount of the customer"s most recent payment.'),
                      Column('Last_Pmnt_Date',
                             Date,
                             nullable=True,
                             doc='Last Payment Date',
                             comment='The date of the customer"s most recent payment.'),
                      Column('Oldest_Inv_Date',
                             Date,
                             nullable=True,
                             doc='Oldest Invoice Date',
                             comment='The date of the oldest current open invoice'),
                      Column('Oldest_Inv_Days',
                             Integer,
                             nullable=True,
                             doc='Oldest Invoice Days',
                             comment='The number of days of the oldest invoice open for this customer.'),
                      Column('AR_Average_Pay_Days',
                             Integer,
                             nullable=True,
                             doc='AR Average Pay Days',
                             comment='The average number of days that it takes the customer to pay an invoice.'),
                      Column('AR_Bal',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AR Balance',
                             comment='The total open A/R balance'),
                      Column('Date_Of_First_Sale',
                             Date,
                             nullable=True,
                             doc='Date Of First Sale',
                             comment='The date of the customer"s first invoice.'),
                      Column('Entered_By_User',
                             String(length=15),
                             nullable=True,
                             doc='Entered By User',
                             comment='The system initials of the user who entered the customer"s account.'),
                      Column('Entered_On_Date',
                             Date,
                             nullable=True,
                             doc='Entered On Date',
                             comment='The date that the customer account was entered into the system.'),
                      Column('Time_Stamp',
                             Time,
                             nullable=True,
                             doc='Time Stamp',
                             comment='Time Stamp'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_stats_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_stats_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Prev_Month_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Previous Month Sales',
                             comment='Total Sales for the previous month'),
                      Column('Curr_Month_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Current Month Sales',
                             comment='Total Sales for the current month.'),
                      Column('Sales_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Sales YTD',
                             comment='Total Year-to-date sales for the customer.'),
                      Column('YTD_Sales',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='YTD Sales',
                             comment='The customer"s total Year to Date Sales'),
                      Column('Credits_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credits YTD',
                             comment='The customer"s total Year-to-date Credits'),
                      Column('YTD_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='YTD Cost',
                             comment='The customer"s total Year-to-date Cost.'),
                      Column('Cost_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost YTD',
                             comment='Total Year-to-date Cost for the customer.'),
                      Column('GP_Dollars_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Dollars YTD',
                             comment='The customer"s total Year-to-date Gross Profit Dollars.'),
                      Column('GP_Pcnt_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Percent YTD',
                             comment='The customer"s total Year-to-date Gross Profit Percent'),
                      Column('Last_Year_Sales_Year_To_Date',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Sales Year To Date',
                             comment='Last Year to Date Sales for the  customer.'),
                      Column('Last_Year_sales_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year sales (YTD)',
                             comment='Total of last year"s sales up to the current month.'),
                      Column('Last_Year_cost_YTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year cost (YTD)',
                             comment='Total of last year"s cost up to the current month.'),
                      Column('GP_Dollars_LYTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Dollars LYTD',
                             comment='The customer"s total Last Year-to-Date Gross Profit Dollars.'),
                      Column('GP_Pcnt_LYTD',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='GP Percent LYTD',
                             comment='The customer"s total Last Year-to-Date Gross Profit Percentage.'),
                      Column('Order_Count_12M',
                             Integer,
                             nullable=True,
                             doc='12M Order Count',
                             comment='The total number of orders entered for the last 12 months. This excludes'
                                     'Quotes, Recurring, and Cancelled orders.'),
                      Column('Inv_Count_12M',
                             Integer,
                             nullable=True,
                             doc='12M Invoice Count',
                             comment='The total number of invoices for the last 12 months.'),
                      Column('Sales_12M',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='12M Sales',
                             comment='The total amount of invoiced sales from the last 12 months'),
                      Column('Cost_12M',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='12M Cost',
                             comment='The total amount of invoiced COGS from the last 12 months.'),
                      Column('GPD_12M',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='12M GPD',
                             comment='The total amount of Gross Profit Dollars from the last 12 months.'),
                      Column('Last_Year_Sales_Total',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Sales Total',
                             comment='Total Last Year Sales for the customer.'),
                      Column('Last_Year_Total_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Total Cost',
                             comment='Total Last Year Cost of the items purchased by the customer.'),
                      Column('Last_Year_Total_GP_Dollars',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Total GP Dollars',
                             comment='Total Last Year Gross Profit Dollars for the customer.'),
                      Column('Last_Year_Total_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Year Total GP Percent',
                             comment='Total Last Year Gross Profit Percent for the customer.'),
                      Column('Three_Year_Sales_Total',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Three Year Sales Total',
                             comment='A total of the past 3 years of sales.'),
                      Column('Two_Year_Sales_Total',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Two Year Sales Total',
                             comment='The total sales of the previous calendar year from Jan Dec. For example, if'
                                     'running the report in the year 2017, this would show the total sales of 2016.'),
                      Column('Cust_Sales_Mon_1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 1',
                             comment='Sales for the first month of the current year.'),
                      Column('Cust_Sales_Mon_2',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 2',
                             comment='Sales for the second month of the current year.'),
                      Column('Cust_Sales_Mon_3',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 3',
                             comment='Sales for the third month of the current year.'),
                      Column('Cust_Sales_Mon_4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 4',
                             comment='Sales for the fourth month of the current year.'),
                      Column('Cust_Sales_Mon_5',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 5',
                             comment='Sales for the fifth month of the current year.'),
                      Column('Cust_Sales_Mon_6',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 6',
                             comment='Sales for the sixth month of the current year.'),
                      Column('Cust_Sales_Mon_7',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 7',
                             comment='Sales for the seventh month of the current year.'),
                      Column('Cust_Sales_Mon_8',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 8',
                             comment='Sales for the eighth month of the current year.'),
                      Column('Cust_Sales_Mon_9',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 9',
                             comment='Sales for the ninth month of the current year.'),
                      Column('Cust_Sales_Mon_10',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 10',
                             comment='Sales for the tenth month of the current year.'),
                      Column('Cust_Sales_Mon_11',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 11',
                             comment='Sales for the eleventh month of the current year.'),
                      Column('Cust_Sales_Mon_12',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Customer Sales Mon 12',
                             comment='Sales for the twelfth month of the current year.'),
                      Column('Cust_LYR_Sales_Mon_1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 1',
                             comment='Sales for the first month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_2',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 2',
                             comment='Sales for the second month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_3',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 3',
                             comment='Sales for the third month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 4',
                             comment='Sales for the fourth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_5',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 5',
                             comment='Sales for the fifth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_6',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 6',
                             comment='Sales for the sixth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_7',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 7',
                             comment='Sales for the seventh month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_8',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 8',
                             comment='Sales for the eighth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_9',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 9',
                             comment='Sales for the ninth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_10',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 10',
                             comment='Sales for the tenth month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_11',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 11',
                             comment='Sales for the eleventh month of the last year.'),
                      Column('Cust_LYR_Sales_Mon_12',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cust LYR Sales Mon 12',
                             comment='Sales for the twelfth month of the last year.'),
                      Column('Days_Since_Last_Inv',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Invoice',
                             comment='Number of days since the last time the customer was invoiced.'),
                      Column('Highest_AR_Bal',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Highest AR Balance',
                             comment='The highest A/R balance that the customer had had with you at any point in'
                                     'time.'),
                      Column('Highest_AR_Bal_Date',
                             Date,
                             nullable=True,
                             doc='Highest AR Balance Date',
                             comment='The date of the highest A/R balance for the customer.'),
                      Column('Last_Event_Date',
                             Date,
                             nullable=True,
                             doc='Last Event Date',
                             comment='The most recent event that is linked to the customer (across all contacts).'
                                     'This is based on the events Start Date.'),
                      Column('Last_Inv_Date_1',
                             Date,
                             nullable=True,
                             doc='Last Invoice Date',
                             comment='The invoice date of the customer"s most recent invoice.'),
                      Column('Last_Inv_Date_2',
                             Date,
                             nullable=True,
                             doc='Last Invoice Date',
                             comment='The invoice date of the customer"s most recent invoice.'),
                      Column('Last_Pmnt_Amount',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Last Payment Amount',
                             comment='The total amount of the customer"s most recent payment.'),
                      Column('Last_Pmnt_Date',
                             Date,
                             nullable=True,
                             doc='Last Payment Date',
                             comment='The date of the customer"s most recent payment.'),
                      Column('Oldest_Inv_Date',
                             Date,
                             nullable=True,
                             doc='Oldest Invoice Date',
                             comment='The date of the oldest current open invoice'),
                      Column('Oldest_Inv_Days',
                             Integer,
                             nullable=True,
                             doc='Oldest Invoice Days',
                             comment='The number of days of the oldest invoice open for this customer.'),
                      Column('AR_Average_Pay_Days',
                             Integer,
                             nullable=True,
                             doc='AR Average Pay Days',
                             comment='The average number of days that it takes the customer to pay an invoice.'),
                      Column('AR_Bal',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AR Balance',
                             comment='The total open A/R balance'),
                      Column('Date_Of_First_Sale',
                             Date,
                             nullable=True,
                             doc='Date Of First Sale',
                             comment='The date of the customer"s first invoice.'),
                      Column('Entered_By_User',
                             String(length=15),
                             nullable=True,
                             doc='Entered By User',
                             comment='The system initials of the user who entered the customer"s account.'),
                      Column('Entered_On_Date',
                             Date,
                             nullable=True,
                             doc='Entered On Date',
                             comment='The date that the customer account was entered into the system.'),
                      Column('Time_Stamp',
                             Time,
                             nullable=True,
                             doc='Time Stamp',
                             comment='Time Stamp'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_subaccounts_01_current(server_utils.mysql_base):
    __table__ = Table('cust_subaccounts_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Sub_Accts',
                             String(length=12),
                             nullable=True,
                             doc='Sub Accounts',
                             comment='Any sub accounts that are listed for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_subaccounts_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_subaccounts_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Sub_Accts',
                             String(length=12),
                             nullable=True,
                             doc='Sub Accounts',
                             comment='Any sub accounts that are listed for the customer.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_vend_ids_01_current(server_utils.mysql_base):
    __table__ = Table('cust_vend_ids_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Vend_Cust_ID',
                             String(length=255),
                             nullable=True,
                             doc='VendCust ID',
                             comment='The Vendor"s account number for the customer'),
                      Column('Vend_Num_Num',
                             String(length=16),
                             nullable=True,
                             doc='Vendor ID Number',
                             comment='The vendor number for any vendors listed under the Vendor ID tab in the'
                                     'Customer Master.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_vend_ids_02_archive(server_utils.mysql_base):
    __table__ = Table('cust_vend_ids_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=15),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The Customer Number for the  customer"s account'),
                      Column('Vend_Cust_ID',
                             String(length=255),
                             nullable=True,
                             doc='VendCust ID',
                             comment='The Vendor"s account number for the customer'),
                      Column('Vend_Num_Num',
                             String(length=16),
                             nullable=True,
                             doc='Vendor ID Number',
                             comment='The vendor number for any vendors listed under the Vendor ID tab in the'
                                     'Customer Master.'),
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class po_04_rec_detail_01_current(server_utils.mysql_base):
    __table__ = Table('po_04_rec_detail_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('PO_Rcving_Num',
                             String(length=30),
                             nullable=True,
                             doc='Purchase Order Receiving Number',
                             comment='This will display the purchase order and receiving number. For example, 0010060'),
                      Column('PO_Num',
                             String(length=30),
                             nullable=True,
                             index=True,
                             doc='Purchase Order Number',
                             comment='The purchase order number'),
                      Column('Rcving_Num',
                             Integer,
                             doc='Receiving Number',
                             comment='This is the receiving number only. For example, you will see 8 when the'
                                     'purchase order receiving is 0010068'),
                      Column('Rcving_Date',
                             Date,
                             nullable=True,
                             doc='Receiving Date',
                             comment='The receiving date on the stock receipt'),
                      Column('Rcving_Time',
                             Time,
                             nullable=True,
                             doc='Receiving Time Stamp',
                             comment='The time of product receiving.'),
                      Column('Whse',
                             String(length=30),
                             nullable=True,
                             doc='Warehouse',
                             comment='The stock receipts warehouse'),
                      Column('Rcved_By',
                             String(length=30),
                             nullable=True,
                             doc='Received By',
                             comment='The initials of the user who received the order'),
                      Column('Acct_Period',
                             String(length=30),
                             nullable=True,
                             doc='Accounting Period yy/mm',
                             comment='This is the general ledger period the receipt took place. This field outputs as'
                                     'Year and Month. Consider using field General Ledger Receipt Month to output as'
                                     'Month & Year'),
                      Column('GL_Rcpt_Month',
                             String(length=30),
                             nullable=True,
                             doc='General Ledger Receipt Month',
                             comment='This is the general ledger period the receipt took place. This field outputs as'
                                     'month and year. Consider using accounting period yy/mm to output as year and'
                                     'month'),
                      Column('AP_Inv_Num',
                             String(length=300),
                             nullable=True,
                             doc='AP Invoice#',
                             comment='Vendor Invoice Number from PO File'),
                      Column('Line_Num',
                             Integer,
                             nullable=True,
                             doc='Line Number',
                             comment='The sequence number of each item on the purchase order'),
                      Column('Prod_Num',
                             String(length=50),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Vend_Part_Num',
                             String(length=500),
                             nullable=True,
                             index=True,
                             doc='Vendor Part Number',
                             comment='The product vendor part number'),
                      Column('Desc_SP',
                             String(length=500),
                             nullable=True,
                             doc='Description SP',
                             comment='If an SP item is used on the purchase order, this will print the freeform'
                                     'description'),
                      Column('Disc_Pcnt',
                             Numeric(precision=13, scale=2),
                             doc='Discount Percent',
                             comment='The purchase order line item discount percent amount'),
                      Column('Qty_Open_by_Rcving',
                             Numeric(precision=13, scale=3),
                             doc='Quantity Open by Receiving',
                             comment='The quantity that was open (balance due) per stock receipt'),
                      Column('Qty_Rcved',
                             Numeric(precision=13, scale=3),
                             doc='Quantity Received',
                             comment='The quantity received on the stock receipt'),
                      Column('Rcving_Dollar_Ext',
                             Numeric(precision=13, scale=2),
                             doc='Receiving Dollar Extended',
                             comment='The total dollar value of the line item receiving'),
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_04_rec_detail_02_archive(server_utils.mysql_base):
    __table__ = Table('po_04_rec_detail_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('PO_Rcving_Num',
                             String(length=30),
                             nullable=True,
                             doc='Purchase Order Receiving Number',
                             comment='This will display the purchase order and receiving number. For example, 0010060'),
                      Column('PO_Num',
                             String(length=30),
                             nullable=True,
                             index=True,
                             doc='Purchase Order Number',
                             comment='The purchase order number'),
                      Column('Rcving_Num',
                             Integer,
                             doc='Receiving Number',
                             comment='This is the receiving number only. For example, you will see 8 when the'
                                     'purchase order receiving is 0010068'),
                      Column('Rcving_Date',
                             Date,
                             nullable=True,
                             doc='Receiving Date',
                             comment='The receiving date on the stock receipt'),
                      Column('Rcving_Time',
                             Time,
                             nullable=True,
                             doc='Receiving Time Stamp',
                             comment='The time of product receiving.'),
                      Column('Whse',
                             String(length=30),
                             nullable=True,
                             doc='Warehouse',
                             comment='The stock receipts warehouse'),
                      Column('Rcved_By',
                             String(length=30),
                             nullable=True,
                             doc='Received By',
                             comment='The initials of the user who received the order'),
                      Column('Acct_Period',
                             String(length=30),
                             nullable=True,
                             doc='Accounting Period yy/mm',
                             comment='This is the general ledger period the receipt took place. This field outputs as'
                                     'Year and Month. Consider using field General Ledger Receipt Month to output as'
                                     'Month & Year'),
                      Column('GL_Rcpt_Month',
                             String(length=30),
                             nullable=True,
                             doc='General Ledger Receipt Month',
                             comment='This is the general ledger period the receipt took place. This field outputs as'
                                     'month and year. Consider using accounting period yy/mm to output as year and'
                                     'month'),
                      Column('AP_Inv_Num',
                             String(length=300),
                             nullable=True,
                             doc='AP Invoice#',
                             comment='Vendor Invoice Number from PO File'),
                      Column('Line_Num',
                             Integer,
                             nullable=True,
                             doc='Line Number',
                             comment='The sequence number of each item on the purchase order'),
                      Column('Prod_Num',
                             String(length=50),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Vend_Part_Num',
                             String(length=500),
                             nullable=True,
                             index=True,
                             doc='Vendor Part Number',
                             comment='The product vendor part number'),
                      Column('Desc_SP',
                             String(length=500),
                             nullable=True,
                             doc='Description SP',
                             comment='If an SP item is used on the purchase order, this will print the freeform'
                                     'description'),
                      Column('Disc_Pcnt',
                             Numeric(precision=13, scale=2),
                             doc='Discount Percent',
                             comment='The purchase order line item discount percent amount'),
                      Column('Qty_Open_by_Rcving',
                             Numeric(precision=13, scale=3),
                             doc='Quantity Open by Receiving',
                             comment='The quantity that was open (balance due) per stock receipt'),
                      Column('Qty_Rcved',
                             Numeric(precision=13, scale=3),
                             doc='Quantity Received',
                             comment='The quantity received on the stock receipt'),
                      Column('Rcving_Dollar_Ext',
                             Numeric(precision=13, scale=2),
                             doc='Receiving Dollar Extended',
                             comment='The total dollar value of the line item receiving'),
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_05_rec_lot_01_current(server_utils.mysql_base):
    __table__ = Table('po_05_rec_lot_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('PO_Rcving_Num',
                             String(length=30),
                             nullable=True,
                             doc='Purchase Order Receiving Number',
                             comment='This will display the purchase order and receiving number. For example, 0010060'),
                      Column('Line_Num',
                             Integer,
                             nullable=True,
                             doc='Line Number',
                             comment='The sequence number of each item on the purchase order'),
                      Column('Prod_Num',
                             String(length=50),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Lot_Qty',
                             Integer,
                             nullable=True,
                             doc='Lot Quantity',
                             comment='The lot receiving quantity'),
                      Column('Lot_Num',
                             String(length=255),
                             nullable=True,
                             doc='Lot Number',
                             comment='The line item lot number in receiving'),
                      Column('Lot_Mfg_Date',
                             Date,
                             nullable=True,
                             doc='Lot Manufacturing Date',
                             comment='The lot manufacturing date'),
                      Column('Lot_Exp_Date',
                             Date,
                             nullable=True,
                             doc='Lot Expiration Date',
                             comment='The lot expiration date'),
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_05_rec_lot_02_archive(server_utils.mysql_base):
    __table__ = Table('po_05_rec_lot_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('PO_Rcving_Num',
                             String(length=30),
                             nullable=True,
                             doc='Purchase Order Receiving Number',
                             comment='This will display the purchase order and receiving number. For example, 0010060'),
                      Column('Line_Num',
                             Integer,
                             nullable=True,
                             doc='Line Number',
                             comment='The sequence number of each item on the purchase order'),
                      Column('Prod_Num',
                             String(length=50),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Lot_Qty',
                             Integer,
                             nullable=True,
                             doc='Lot Quantity',
                             comment='The lot receiving quantity'),
                      Column('Lot_Num',
                             String(length=255),
                             nullable=True,
                             doc='Lot Number',
                             comment='The line item lot number in receiving'),
                      Column('Lot_Mfg_Date',
                             Date,
                             nullable=True,
                             doc='Lot Manufacturing Date',
                             comment='The lot manufacturing date'),
                      Column('Lot_Exp_Date',
                             Date,
                             nullable=True,
                             doc='Lot Expiration Date',
                             comment='The lot expiration date'),
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_06_rec_serial_01_current(server_utils.mysql_base):
    __table__ = Table('po_06_rec_serial_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('PO_Rcving_Num',
                             String(length=30),
                             nullable=True,
                             doc='Purchase Order Receiving Number',
                             comment='This will display the purchase order and receiving number. For example, 0010060'),
                      Column('Line_Num',
                             Integer,
                             nullable=True,
                             doc='Line Number',
                             comment='The sequence number of each item on the purchase order'),
                      Column('Prod_Num',
                             String(length=50),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Serial_Num',
                             String(length=255),
                             nullable=True,
                             doc='Serial Number',
                             comment='The serial number linked to the product receiving'),
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_06_rec_serial_02_archive(server_utils.mysql_base):
    __table__ = Table('po_06_rec_serial_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('PO_Rcving_Num',
                             String(length=30),
                             nullable=True,
                             doc='Purchase Order Receiving Number',
                             comment='This will display the purchase order and receiving number. For example, 0010060'),
                      Column('Line_Num',
                             Integer,
                             nullable=True,
                             doc='Line Number',
                             comment='The sequence number of each item on the purchase order'),
                      Column('Prod_Num',
                             String(length=50),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Serial_Num',
                             String(length=255),
                             nullable=True,
                             doc='Serial Number',
                             comment='The serial number linked to the product receiving'),
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class price_matrix_future_01_current(server_utils.mysql_base):
    __table__ = Table('price_matrix_future_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Level_Num',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Level Number',
                             comment='The matrix level number. Use the levels button in the Price Matrix for a'
                                     'complete list.'),
                      Column('Branch_Code',
                             String(length=6),
                             nullable=True,
                             doc='Branch Code',
                             comment='If blank, this price matrix applies to all orders. Otherwise, this matrix will'
                                     'only be used for the specified branch.'),
                      Column('All_Cust_Cntr',
                             String(length=17),
                             nullable=True,
                             doc='All Customer Contract',
                             comment='This flag says every customer is eligible for this contract.'),
                      Column('Cust_Cat',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Customer Category Code',
                             comment='The customer category code that is linked to a price matrix.'),
                      Column('Cust_Num',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number.'),
                      Column('Ship_To_Code',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Ship To Code',
                             comment='The Ship To code number'),
                      Column('Major_Group',
                             String(length=5),
                             nullable=True,
                             doc='Major Group',
                             comment='The product Major Group.'),
                      Column('Prod_Line',
                             String(length=10),
                             nullable=True,
                             doc='Product Line',
                             comment='The product line code. Use this to display price matrices directly linked to a'
                                     'product line.'),
                      Column('Price_Group_Code',
                             String(length=8),
                             nullable=True,
                             doc='Price Group Code',
                             comment='The Price Group code.'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Qty_Break',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Quantity Break',
                             comment='The quantity break value.'),
                      Column('Qty_Break_Count',
                             Integer,
                             nullable=True,
                             doc='Quantity Break Count',
                             comment='The number of quantity breaks for the price matrix.'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor Number',
                             comment='The vendor number field.'),
                      Column('Cntr_Num',
                             String(length=15),
                             nullable=True,
                             doc='Contract Number',
                             comment='The contract number.'),
                      Column('Price_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Net Factor Price Amount',
                             comment='This is the value found in the Amount field for price'),
                      Column('Price_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Percent / Dollar Sign',
                             comment='This field will show a % or a $ sign based on the type of formula used.'),
                      Column('Price_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Plus / Minus Sign',
                             comment='This field will show a + or  sign based on the type of formula used'),
                      Column('Price_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Price C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining sales price. This is cost,'
                                     'list, net, or calculated cost'),
                      Column('Cost_Amount',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Amount',
                             comment='The cost that is displayed in the amount field of the price matrix.'),
                      Column('Cost_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Cost C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining cost. This is cost, list,'
                                     'or net'),
                      Column('Cost_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Net Factor',
                             comment='Cost net factor'),
                      Column('Cost_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Cost Percent / Dollar',
                             comment='This field will show a % or a $ sign based on the type of cost formula used.'),
                      Column('Cost_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Cost Plus / Minus',
                             comment='Cost Plus/Minus'),
                      Column('Load_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Load Percent',
                             comment='The load percent used on the rebate cost.'),
                      Column('Mixed_Breaks',
                             String(length=12),
                             nullable=True,
                             doc='Mixed Breaks',
                             comment='This is a Y or N value'),
                      Column('Mixed_Breaks_Method',
                             String(length=10),
                             nullable=True,
                             doc='Mixed Breaks Method',
                             comment='When using mixed breaks, will show (Q) Quantity, ($) Dollar Breaks, or (W)'
                                     'Weight'),
                      Column('Purchase_Cntr',
                             String(length=8),
                             nullable=True,
                             doc='Purchase Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Salesman',
                             String(length=4),
                             nullable=True,
                             doc='Salesman',
                             comment='The salesperson assigned to the customer, for a customer"s price matrix.'),
                      Column('Web_Cntr',
                             String(length=12),
                             nullable=True,
                             doc='Web Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Co_Op_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Co Op Percent',
                             comment='The Co Op Percent amount'),
                      Column('Eff_Date',
                             Date,
                             nullable=True,
                             doc='Effective Date',
                             comment='The start date for the price matrix'),
                      Column('Exp_Date',
                             Date,
                             nullable=True,
                             doc='Expiration Date',
                             comment='The expiration date for the price matrix.'),
                      Column('Future_Price_Date',
                             Date,
                             nullable=True,
                             doc='Future Price Date',
                             comment='The date in which the future price matrix will take effect'),
                      Column('Date_Stamp',
                             Date,
                             nullable=True,
                             doc='Date Stamp',
                             comment='The date stamp for the price matrix.'),
                      Column('Time_Stamp',
                             Time,
                             nullable=True,
                             doc='Time Stamp',
                             comment='The time stamp for the price matrix. This only shows the time (i.e. 5:09pm)'),
                      Column('Last_Update_Date',
                             Date,
                             nullable=True,
                             doc='Last Update Date',
                             comment='The last date the price matrix was updated. "'),
                      Column('Last_Update_Initials',
                             String(length=3),
                             nullable=True,
                             doc='Last Update Initials',
                             comment='The user who last updated the price matrix'),
                      Column('Entered_By',
                             String(length=6),
                             nullable=True,
                             doc='Entered By',
                             comment='The user who entered the price matrix.'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date the price matrix was created.'),
                      schema='future.price.matrix')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))

    @hybrid_property
    def Price_Net_Plus_Minus(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Price_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Price_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Price_Net_Factor * -1
            else:
                return self.__table__.c.Price_Net_Factor
    
    # noinspection PyMethodParameters
    @Price_Net_Plus_Minus.expression
    def Price_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Plus_Minus) == "-",
                                (cls.__table__.c.Price_Net_Factor * -1))
                           ], else_=cls.__table__.c.Price_Net_Factor
                       )
                       )

    @hybrid_property
    def Price_Net_Pct_Dollar(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Price_Net_Plus_Minus / 100
            else:
                return self.Price_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Price_Net_Pct_Dollar.expression
    def Price_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%", (cls.Price_Net_Plus_Minus / 100))
    
                           ], else_=cls.Price_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Price_Reference(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Price_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Price_Reference.expression
    def Price_Reference(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Price_Net(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Price_Net_Pct_Dollar) * self.Price_Reference
            else:
                return self.Price_Net_Pct_Dollar + self.Price_Reference
    
    # noinspection PyMethodParameters
    @Price_Net.expression
    def Price_Net(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%",
                                ((1 + cls.Price_Net_Pct_Dollar) * cls.Price_Reference))
                           ], else_=(cls.Price_Net_Pct_Dollar + cls.Price_Reference)
                       )
                       )

    @hybrid_property
    def Cost_Net_Plus_Minus(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Cost_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Cost_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Cost_Net_Factor * -1
            else:
                return self.__table__.c.Cost_Net_Factor
    
    # noinspection PyMethodParameters
    @Cost_Net_Plus_Minus.expression
    def Cost_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Plus_Minus) == "-",
                                (cls.__table__.c.Cost_Net_Factor * -1))
                           ], else_=cls.__table__.c.Cost_Net_Factor
                       )
                       )

    @hybrid_property
    def Cost_Net_Pct_Dollar(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Cost_Net_Plus_Minus / 100
            else:
                return self.Cost_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Cost_Net_Pct_Dollar.expression
    def Cost_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%", (cls.Cost_Net_Plus_Minus / 100))
    
                           ], else_=cls.Cost_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Cost_Reference(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Cost_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Cost_Reference.expression
    def Cost_Reference(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Cost_Net(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Cost_Net_Pct_Dollar) * self.Cost_Reference
            else:
                return self.Cost_Net_Pct_Dollar + self.Cost_Reference
    
    # noinspection PyMethodParameters
    @Cost_Net.expression
    def Cost_Net(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%",
                                ((1 + cls.Cost_Net_Pct_Dollar) * cls.Cost_Reference))
                           ], else_=(cls.Cost_Net_Pct_Dollar + cls.Cost_Reference)
                       )
                       )


# noinspection PyPep8Naming
class price_matrix_future_02_archive(server_utils.mysql_base):
    __table__ = Table('price_matrix_future_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Level_Num',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Level Number',
                             comment='The matrix level number. Use the levels button in the Price Matrix for a'
                                     'complete list.'),
                      Column('Branch_Code',
                             String(length=6),
                             nullable=True,
                             doc='Branch Code',
                             comment='If blank, this price matrix applies to all orders. Otherwise, this matrix will'
                                     'only be used for the specified branch.'),
                      Column('All_Cust_Cntr',
                             String(length=17),
                             nullable=True,
                             doc='All Customer Contract',
                             comment='This flag says every customer is eligible for this contract.'),
                      Column('Cust_Cat',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Customer Category Code',
                             comment='The customer category code that is linked to a price matrix.'),
                      Column('Cust_Num',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number.'),
                      Column('Ship_To_Code',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Ship To Code',
                             comment='The Ship To code number'),
                      Column('Major_Group',
                             String(length=5),
                             nullable=True,
                             doc='Major Group',
                             comment='The product Major Group.'),
                      Column('Prod_Line',
                             String(length=10),
                             nullable=True,
                             doc='Product Line',
                             comment='The product line code. Use this to display price matrices directly linked to a'
                                     'product line.'),
                      Column('Price_Group_Code',
                             String(length=8),
                             nullable=True,
                             doc='Price Group Code',
                             comment='The Price Group code.'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Qty_Break',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Quantity Break',
                             comment='The quantity break value.'),
                      Column('Qty_Break_Count',
                             Integer,
                             nullable=True,
                             doc='Quantity Break Count',
                             comment='The number of quantity breaks for the price matrix.'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor Number',
                             comment='The vendor number field.'),
                      Column('Cntr_Num',
                             String(length=15),
                             nullable=True,
                             doc='Contract Number',
                             comment='The contract number.'),
                      Column('Price_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Net Factor Price Amount',
                             comment='This is the value found in the Amount field for price'),
                      Column('Price_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Percent / Dollar Sign',
                             comment='This field will show a % or a $ sign based on the type of formula used.'),
                      Column('Price_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Plus / Minus Sign',
                             comment='This field will show a + or  sign based on the type of formula used'),
                      Column('Price_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Price C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining sales price. This is cost,'
                                     'list, net, or calculated cost'),
                      Column('Cost_Amount',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Amount',
                             comment='The cost that is displayed in the amount field of the price matrix.'),
                      Column('Cost_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Cost C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining cost. This is cost, list,'
                                     'or net'),
                      Column('Cost_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Net Factor',
                             comment='Cost net factor'),
                      Column('Cost_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Cost Percent / Dollar',
                             comment='This field will show a % or a $ sign based on the type of cost formula used.'),
                      Column('Cost_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Cost Plus / Minus',
                             comment='Cost Plus/Minus'),
                      Column('Load_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Load Percent',
                             comment='The load percent used on the rebate cost.'),
                      Column('Mixed_Breaks',
                             String(length=12),
                             nullable=True,
                             doc='Mixed Breaks',
                             comment='This is a Y or N value'),
                      Column('Mixed_Breaks_Method',
                             String(length=10),
                             nullable=True,
                             doc='Mixed Breaks Method',
                             comment='When using mixed breaks, will show (Q) Quantity, ($) Dollar Breaks, or (W)'
                                     'Weight'),
                      Column('Purchase_Cntr',
                             String(length=8),
                             nullable=True,
                             doc='Purchase Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Salesman',
                             String(length=4),
                             nullable=True,
                             doc='Salesman',
                             comment='The salesperson assigned to the customer, for a customer"s price matrix.'),
                      Column('Web_Cntr',
                             String(length=12),
                             nullable=True,
                             doc='Web Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Co_Op_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Co Op Percent',
                             comment='The Co Op Percent amount'),
                      Column('Eff_Date',
                             Date,
                             nullable=True,
                             doc='Effective Date',
                             comment='The start date for the price matrix'),
                      Column('Exp_Date',
                             Date,
                             nullable=True,
                             doc='Expiration Date',
                             comment='The expiration date for the price matrix.'),
                      Column('Future_Price_Date',
                             Date,
                             nullable=True,
                             doc='Future Price Date',
                             comment='The date in which the future price matrix will take effect'),
                      Column('Date_Stamp',
                             Date,
                             nullable=True,
                             doc='Date Stamp',
                             comment='The date stamp for the price matrix.'),
                      Column('Time_Stamp',
                             Time,
                             nullable=True,
                             doc='Time Stamp',
                             comment='The time stamp for the price matrix. This only shows the time (i.e. 5:09pm)'),
                      Column('Last_Update_Date',
                             Date,
                             nullable=True,
                             doc='Last Update Date',
                             comment='The last date the price matrix was updated. "'),
                      Column('Last_Update_Initials',
                             String(length=3),
                             nullable=True,
                             doc='Last Update Initials',
                             comment='The user who last updated the price matrix'),
                      Column('Entered_By',
                             String(length=6),
                             nullable=True,
                             doc='Entered By',
                             comment='The user who entered the price matrix.'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date the price matrix was created.'),
                      schema='future.price.matrix')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))

    @hybrid_property
    def Price_Net_Plus_Minus(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Price_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Price_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Price_Net_Factor * -1
            else:
                return self.__table__.c.Price_Net_Factor
    
    # noinspection PyMethodParameters
    @Price_Net_Plus_Minus.expression
    def Price_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Plus_Minus) == "-",
                                (cls.__table__.c.Price_Net_Factor * -1))
                           ], else_=cls.__table__.c.Price_Net_Factor
                       )
                       )

    @hybrid_property
    def Price_Net_Pct_Dollar(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Price_Net_Plus_Minus / 100
            else:
                return self.Price_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Price_Net_Pct_Dollar.expression
    def Price_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%", (cls.Price_Net_Plus_Minus / 100))
    
                           ], else_=cls.Price_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Price_Reference(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Price_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Price_Reference.expression
    def Price_Reference(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Price_Net(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Price_Net_Pct_Dollar) * self.Price_Reference
            else:
                return self.Price_Net_Pct_Dollar + self.Price_Reference
    
    # noinspection PyMethodParameters
    @Price_Net.expression
    def Price_Net(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%",
                                ((1 + cls.Price_Net_Pct_Dollar) * cls.Price_Reference))
                           ], else_=(cls.Price_Net_Pct_Dollar + cls.Price_Reference)
                       )
                       )

    @hybrid_property
    def Cost_Net_Plus_Minus(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Cost_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Cost_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Cost_Net_Factor * -1
            else:
                return self.__table__.c.Cost_Net_Factor
    
    # noinspection PyMethodParameters
    @Cost_Net_Plus_Minus.expression
    def Cost_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Plus_Minus) == "-",
                                (cls.__table__.c.Cost_Net_Factor * -1))
                           ], else_=cls.__table__.c.Cost_Net_Factor
                       )
                       )

    @hybrid_property
    def Cost_Net_Pct_Dollar(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Cost_Net_Plus_Minus / 100
            else:
                return self.Cost_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Cost_Net_Pct_Dollar.expression
    def Cost_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%", (cls.Cost_Net_Plus_Minus / 100))
    
                           ], else_=cls.Cost_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Cost_Reference(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Cost_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Cost_Reference.expression
    def Cost_Reference(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Cost_Net(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Cost_Net_Pct_Dollar) * self.Cost_Reference
            else:
                return self.Cost_Net_Pct_Dollar + self.Cost_Reference
    
    # noinspection PyMethodParameters
    @Cost_Net.expression
    def Cost_Net(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%",
                                ((1 + cls.Cost_Net_Pct_Dollar) * cls.Cost_Reference))
                           ], else_=(cls.Cost_Net_Pct_Dollar + cls.Cost_Reference)
                       )
                       )


# noinspection PyPep8Naming
class gl_groups_01_current(server_utils.mysql_base):
    __table__ = Table('gl_groups_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='GL Group Code'),
                      Column('Desc',
                             String(length=255),
                             nullable=True,
                             doc='Description',
                             comment='Description'),
                      Column('Revenue_Group',
                             String(length=255),
                             nullable=True,
                             doc='Revenue Group',
                             comment='General Ledger Numbers'),
                      Column('Summary_Group',
                             String(length=255),
                             nullable=True,
                             doc='Summary Group',
                             comment='GL Account Description'),
                      schema='gl.group')


# noinspection PyPep8Naming
class gl_groups_02_archive(server_utils.mysql_base):
    __table__ = Table('gl_groups_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='GL Group Code'),
                      Column('Desc',
                             String(length=255),
                             nullable=True,
                             doc='Description',
                             comment='Description'),
                      Column('Revenue_Group',
                             String(length=255),
                             nullable=True,
                             doc='Revenue Group',
                             comment='General Ledger Numbers'),
                      Column('Summary_Group',
                             String(length=255),
                             nullable=True,
                             doc='Summary Group',
                             comment='GL Account Description'),
                      schema='gl.group')


# noinspection PyPep8Naming
class gl_groups_rpts_01_current(server_utils.mysql_base):
    __table__ = Table('gl_groups_rpts_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='GL Group Code'),
                      Column('Reports',
                             String(length=255),
                             nullable=True,
                             doc='Reports',
                             comment='Reports'),
                      schema='gl.group')


# noinspection PyPep8Naming
class gl_groups_rpts_02_archive(server_utils.mysql_base):
    __table__ = Table('gl_groups_rpts_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='GL Group Code'),
                      Column('Reports',
                             String(length=255),
                             nullable=True,
                             doc='Reports',
                             comment='Reports'),
                      schema='gl.group')


# noinspection PyPep8Naming
class major_group_01_static(server_utils.mysql_base):
    __table__ = Table('major_group_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='Major Group Code'),
                      schema='major.group')


# noinspection PyPep8Naming
class major_group_main_01_current(server_utils.mysql_base):
    __table__ = Table('major_group_main_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='Major Group Code'),
                      Column('Desc',
                             String(length=30),
                             nullable=True,
                             doc='Description',
                             comment='Major Group Description'),
                      schema='major.group')


# noinspection PyPep8Naming
class major_group_main_02_archive(server_utils.mysql_base):
    __table__ = Table('major_group_main_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Code',
                             comment='Major Group Code'),
                      Column('Desc',
                             String(length=30),
                             nullable=True,
                             doc='Description',
                             comment='Major Group Description'),
                      schema='major.group')


# noinspection PyPep8Naming
class cntr_01_static(server_utils.mysql_base):
    __table__ = Table('cntr_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Desc',
                             String(length=30),
                             nullable=True,
                             doc='Description',
                             comment='The description of this contract'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_category_01_current(server_utils.mysql_base):
    __table__ = Table('cntr_category_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Cust_Cat',
                             String(length=8),
                             nullable=True,
                             doc='Customer Categories',
                             comment='A list of Customer Categories assigned to this contract.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_category_02_archive(server_utils.mysql_base):
    __table__ = Table('cntr_category_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Cust_Cat',
                             String(length=8),
                             nullable=True,
                             doc='Customer Categories',
                             comment='A list of Customer Categories assigned to this contract.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_cmnts_01_current(server_utils.mysql_base):
    __table__ = Table('cntr_cmnts_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Comments',
                             String(length=50),
                             nullable=True,
                             doc='Comments',
                             comment='This is the data that is displayed in the Remarks box.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_cmnts_02_archive(server_utils.mysql_base):
    __table__ = Table('cntr_cmnts_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Comments',
                             String(length=50),
                             nullable=True,
                             doc='Comments',
                             comment='This is the data that is displayed in the Remarks box.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_header_01_current(server_utils.mysql_base):
    __table__ = Table('cntr_header_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Desc',
                             String(length=30),
                             nullable=True,
                             doc='Description',
                             comment='The description of this contract'),
                      Column('Eff_Date',
                             Date,
                             nullable=True,
                             doc='Effective Date',
                             comment='The date this contract becomes effective. If blank, date check is not used.'),
                      Column('Exp_Date',
                             Date,
                             nullable=True,
                             doc='Expiration Date',
                             comment='The date that this contract ends. If blank, this date check is not used and the'
                                     'contract will never expire.'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor Number',
                             comment='The vendor number that is associated with this contract'),
                      Column('Vend_Cntr_Num',
                             String(length=500),
                             nullable=True,
                             index=True,
                             doc='Vendor Contract Number',
                             comment='The vendor assigned contract number .'),
                      Column('Special_Pricing_Cntr',
                             String(length=16),
                             nullable=True,
                             doc='Special Pricing Contract',
                             comment='A Y/N Field to show "Above Item is on Special" for prices sales orders, ship'
                                     'confirmation, order confirmation, and invoice copies.'),
                      Column('Fut_Vend_Num',
                             String(length=14),
                             nullable=True,
                             doc='Future Vendor Number',
                             comment='The future contract number assigned by the vendor.'),
                      Column('Fut_Vend_Cntr_Eff_Date',
                             Date,
                             nullable=True,
                             doc='Future Vender Contract Number Date',
                             comment='The date the future vendor contract number becomes effective.'),
                      Column('All_Cust_Flag',
                             String(length=13),
                             nullable=True,
                             doc='All Customer Flag',
                             comment='This will contain a Y if this contract applies to all customers.'),
                      Column('Web_Cntr',
                             String(length=12),
                             nullable=True,
                             doc='Web Contract',
                             comment='This field will contain a Y if this contract is used in Inform E-Commerce to'
                                     'limit the products a customer can order.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_header_02_archive(server_utils.mysql_base):
    __table__ = Table('cntr_header_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Desc',
                             String(length=30),
                             nullable=True,
                             doc='Description',
                             comment='The description of this contract'),
                      Column('Eff_Date',
                             Date,
                             nullable=True,
                             doc='Effective Date',
                             comment='The date this contract becomes effective. If blank, date check is not used.'),
                      Column('Exp_Date',
                             Date,
                             nullable=True,
                             doc='Expiration Date',
                             comment='The date that this contract ends. If blank, this date check is not used and the'
                                     'contract will never expire.'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor Number',
                             comment='The vendor number that is associated with this contract'),
                      Column('Vend_Cntr_Num',
                             String(length=500),
                             nullable=True,
                             index=True,
                             doc='Vendor Contract Number',
                             comment='The vendor assigned contract number .'),
                      Column('Special_Pricing_Cntr',
                             String(length=16),
                             nullable=True,
                             doc='Special Pricing Contract',
                             comment='A Y/N Field to show "Above Item is on Special" for prices sales orders, ship'
                                     'confirmation, order confirmation, and invoice copies.'),
                      Column('Fut_Vend_Num',
                             String(length=14),
                             nullable=True,
                             doc='Future Vendor Number',
                             comment='The future contract number assigned by the vendor.'),
                      Column('Fut_Vend_Cntr_Eff_Date',
                             Date,
                             nullable=True,
                             doc='Future Vender Contract Number Date',
                             comment='The date the future vendor contract number becomes effective.'),
                      Column('All_Cust_Flag',
                             String(length=13),
                             nullable=True,
                             doc='All Customer Flag',
                             comment='This will contain a Y if this contract applies to all customers.'),
                      Column('Web_Cntr',
                             String(length=12),
                             nullable=True,
                             doc='Web Contract',
                             comment='This field will contain a Y if this contract is used in Inform E-Commerce to'
                                     'limit the products a customer can order.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_shipto_01_current(server_utils.mysql_base):
    __table__ = Table('cntr_shipto_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Cust_Nums',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Customer Numbers',
                             comment='A list of customers assigned to this contract. If "All Customers" is Y, then'
                                     'this field will be blank.'),
                      Column('Ship_To_Nums',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Ship To Numbers',
                             comment='A list of the ship to numbers that are assigned to this contract. If "All'
                                     'Customers" is Y, or this contract applies to all ship tos, then this field will'
                                     'be blank'),
                      schema='price.contract')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Nums not in (None, ""):
            if self.__table__.c.Ship_To_Nums not in (None, ""):
                return self.__table__.c.Cust_Nums + "_" + self.__table__.c.Ship_To_Nums
            elif self.__table__.c.Ship_To_Nums in (None, ""):
                return self.__table__.c.Cust_Nums + "_" + literal("All")
        elif self.__table__.c.Cust_Nums in (None, ""):
            if self.__table__.c.Ship_To_Nums not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Nums in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Nums.isnot(None), cls.__table__.c.Cust_Nums != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Nums.isnot(None), cls.__table__.c.Ship_To_Nums != ""),
                     func.concat(cls.__table__.c.Cust_Nums, literal("_"), cls.__table__.c.Ship_To_Nums),
                     func.concat(cls.__table__.c.Cust_Nums, literal("_All")))),
            (or_(cls.__table__.c.Cust_Nums.is_(None), cls.__table__.c.Cust_Nums == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Nums.is_(None), cls.__table__.c.Ship_To_Nums == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class cntr_shipto_02_archive(server_utils.mysql_base):
    __table__ = Table('cntr_shipto_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Cust_Nums',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Customer Numbers',
                             comment='A list of customers assigned to this contract. If "All Customers" is Y, then'
                                     'this field will be blank.'),
                      Column('Ship_To_Nums',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Ship To Numbers',
                             comment='A list of the ship to numbers that are assigned to this contract. If "All'
                                     'Customers" is Y, or this contract applies to all ship tos, then this field will'
                                     'be blank'),
                      schema='price.contract')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Nums not in (None, ""):
            if self.__table__.c.Ship_To_Nums not in (None, ""):
                return self.__table__.c.Cust_Nums + "_" + self.__table__.c.Ship_To_Nums
            elif self.__table__.c.Ship_To_Nums in (None, ""):
                return self.__table__.c.Cust_Nums + "_" + literal("All")
        elif self.__table__.c.Cust_Nums in (None, ""):
            if self.__table__.c.Ship_To_Nums not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Nums in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Nums.isnot(None), cls.__table__.c.Cust_Nums != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Nums.isnot(None), cls.__table__.c.Ship_To_Nums != ""),
                     func.concat(cls.__table__.c.Cust_Nums, literal("_"), cls.__table__.c.Ship_To_Nums),
                     func.concat(cls.__table__.c.Cust_Nums, literal("_All")))),
            (or_(cls.__table__.c.Cust_Nums.is_(None), cls.__table__.c.Cust_Nums == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Nums.is_(None), cls.__table__.c.Ship_To_Nums == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class cntr_source_01_current(server_utils.mysql_base):
    __table__ = Table('cntr_source_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Cust_Src',
                             String(length=20),
                             nullable=True,
                             doc='Customer Source',
                             comment='Customer source code field associated with the contract.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_source_02_archive(server_utils.mysql_base):
    __table__ = Table('cntr_source_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cntr_Num',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Contract Number',
                             comment='The key to the contract record.'),
                      Column('Cust_Src',
                             String(length=20),
                             nullable=True,
                             doc='Customer Source',
                             comment='Customer source code field associated with the contract.'),
                      schema='price.contract')


# noinspection PyPep8Naming
class price_matrix_01_current(server_utils.mysql_base):
    __table__ = Table('price_matrix_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Level_Num',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Level Number',
                             comment='The matrix level number. Use the levels button in the Price Matrix for a'
                                     'complete list.'),
                      Column('Branch_Code',
                             String(length=6),
                             nullable=True,
                             doc='Branch Code',
                             comment='If blank, this price matrix applies to all orders. Otherwise, this matrix will'
                                     'only be used for the specified branch.'),
                      Column('All_Cust_Cntr',
                             String(length=17),
                             nullable=True,
                             doc='All Customer Contract',
                             comment='This flag says every customer is eligible for this contract.'),
                      Column('Cust_Cat',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Customer Category Code',
                             comment='The customer category code that is linked to a price matrix.'),
                      Column('Cust_Num',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number.'),
                      Column('Ship_To_Code',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Ship To Code',
                             comment='The Ship To code number'),
                      Column('Major_Group',
                             String(length=5),
                             nullable=True,
                             doc='Major Group',
                             comment='The product Major Group.'),
                      Column('Prod_Line',
                             String(length=10),
                             nullable=True,
                             doc='Product Line',
                             comment='The product line code. Use this to display price matrices directly linked to a'
                                     'product line.'),
                      Column('Price_Group_Code',
                             String(length=8),
                             nullable=True,
                             doc='Price Group Code',
                             comment='The Price Group code.'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Qty_Break',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Quantity Break',
                             comment='The quantity break value.'),
                      Column('Qty_Break_Count',
                             Integer,
                             nullable=True,
                             doc='Quantity Break Count',
                             comment='The number of quantity breaks for the price matrix.'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor Number',
                             comment='The vendor number field.'),
                      Column('Cntr_Num',
                             String(length=15),
                             nullable=True,
                             doc='Contract Number',
                             comment='The contract number.'),
                      Column('Price_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Net Factor Price Amount',
                             comment='This is the value found in the Amount field for price'),
                      Column('Price_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Percent / Dollar Sign',
                             comment='This field will show a % or a $ sign based on the type of formula used.'),
                      Column('Price_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Plus / Minus Sign',
                             comment='This field will show a + or - sign based on the type of formula used'),
                      Column('Price_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Price C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining sales price. This is cost,'
                                     'list, net, or calculated cost'),
                      Column('Cost_Amount',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Amount',
                             comment='The cost that is displayed in the amount field of the price matrix.'),
                      Column('Cost_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Cost C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining cost. This is cost, list,'
                                     'or net'),
                      Column('Cost_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Net Factor',
                             comment='Cost net factor'),
                      Column('Cost_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Cost Percent / Dollar',
                             comment='This field will show a % or a $ sign based on the type of cost formula used.'),
                      Column('Cost_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Cost Plus / Minus',
                             comment='Cost Plus/Minus'),
                      Column('Load_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Load Percent',
                             comment='The load percent used on the rebate cost.'),
                      Column('Mixed_Breaks',
                             String(length=12),
                             nullable=True,
                             doc='Mixed Breaks',
                             comment='This is a Y or N value'),
                      Column('Mixed_Breaks_Method',
                             String(length=10),
                             nullable=True,
                             doc='Mixed Breaks Method',
                             comment='When using mixed breaks, will show (Q) Quantity, ($) Dollar Breaks, or (W)'
                                     'Weight'),
                      Column('Purchase_Cntr',
                             String(length=8),
                             nullable=True,
                             doc='Purchase Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Salesman',
                             String(length=4),
                             nullable=True,
                             doc='Salesman',
                             comment='The salesperson assigned to the customer, for a customer"s price matrix.'),
                      Column('Web_Cntr',
                             String(length=12),
                             nullable=True,
                             doc='Web Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Co_Op_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Co Op Percent',
                             comment='The Co Op Percent amount'),
                      Column('Eff_Date',
                             Date,
                             nullable=True,
                             doc='Effective Date',
                             comment='The start date for the price matrix'),
                      Column('Exp_Date',
                             Date,
                             nullable=True,
                             doc='Expiration Date',
                             comment='The expiration date for the price matrix.'),
                      Column('Future_Price_Date',
                             Date,
                             nullable=True,
                             doc='Future Price Date',
                             comment='The date in which the future price matrix will take effect'),
                      Column('Date_Stamp',
                             Date,
                             nullable=True,
                             doc='Date Stamp',
                             comment='The date stamp for the price matrix.'),
                      Column('Time_Stamp',
                             Time,
                             nullable=True,
                             doc='Time Stamp',
                             comment='The time stamp for the price matrix. This only shows the time (i.e. 5:09pm)'),
                      Column('Last_Update_Date',
                             Date,
                             nullable=True,
                             doc='Last Update Date',
                             comment='The last date the price matrix was updated. "'),
                      Column('Last_Update_Initials',
                             String(length=3),
                             nullable=True,
                             doc='Last Update Initials',
                             comment='The user who last updated the price matrix'),
                      Column('Entered_By',
                             String(length=6),
                             nullable=True,
                             doc='Entered By',
                             comment='The user who entered the price matrix.'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date the price matrix was created.'),
                      schema='price.matrix')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))

    @hybrid_property
    def Price_Net_Plus_Minus(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Price_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Price_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Price_Net_Factor * -1
            else:
                return self.__table__.c.Price_Net_Factor
    
    # noinspection PyMethodParameters
    @Price_Net_Plus_Minus.expression
    def Price_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Plus_Minus) == "-",
                                (cls.__table__.c.Price_Net_Factor * -1))
                           ], else_=cls.__table__.c.Price_Net_Factor
                       )
                       )

    @hybrid_property
    def Price_Net_Pct_Dollar(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Price_Net_Plus_Minus / 100
            else:
                return self.Price_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Price_Net_Pct_Dollar.expression
    def Price_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%", (cls.Price_Net_Plus_Minus / 100))
    
                           ], else_=cls.Price_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Price_Reference(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Price_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Price_Reference.expression
    def Price_Reference(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Price_Net(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Price_Net_Pct_Dollar) * self.Price_Reference
            else:
                return self.Price_Net_Pct_Dollar + self.Price_Reference
    
    # noinspection PyMethodParameters
    @Price_Net.expression
    def Price_Net(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%",
                                ((1 + cls.Price_Net_Pct_Dollar) * cls.Price_Reference))
                           ], else_=(cls.Price_Net_Pct_Dollar + cls.Price_Reference)
                       )
                       )

    @hybrid_property
    def Cost_Net_Plus_Minus(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Cost_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Cost_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Cost_Net_Factor * -1
            else:
                return self.__table__.c.Cost_Net_Factor
    
    # noinspection PyMethodParameters
    @Cost_Net_Plus_Minus.expression
    def Cost_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Plus_Minus) == "-",
                                (cls.__table__.c.Cost_Net_Factor * -1))
                           ], else_=cls.__table__.c.Cost_Net_Factor
                       )
                       )

    @hybrid_property
    def Cost_Net_Pct_Dollar(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Cost_Net_Plus_Minus / 100
            else:
                return self.Cost_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Cost_Net_Pct_Dollar.expression
    def Cost_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%", (cls.Cost_Net_Plus_Minus / 100))
    
                           ], else_=cls.Cost_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Cost_Reference(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Cost_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Cost_Reference.expression
    def Cost_Reference(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Cost_Net(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Cost_Net_Pct_Dollar) * self.Cost_Reference
            else:
                return self.Cost_Net_Pct_Dollar + self.Cost_Reference
    
    # noinspection PyMethodParameters
    @Cost_Net.expression
    def Cost_Net(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%",
                                ((1 + cls.Cost_Net_Pct_Dollar) * cls.Cost_Reference))
                           ], else_=(cls.Cost_Net_Pct_Dollar + cls.Cost_Reference)
                       )
                       )


# noinspection PyPep8Naming
class price_matrix_02_archive(server_utils.mysql_base):
    __table__ = Table('price_matrix_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Level_Num',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Level Number',
                             comment='The matrix level number. Use the levels button in the Price Matrix for a'
                                     'complete list.'),
                      Column('Branch_Code',
                             String(length=6),
                             nullable=True,
                             doc='Branch Code',
                             comment='If blank, this price matrix applies to all orders. Otherwise, this matrix will'
                                     'only be used for the specified branch.'),
                      Column('All_Cust_Cntr',
                             String(length=17),
                             nullable=True,
                             doc='All Customer Contract',
                             comment='This flag says every customer is eligible for this contract.'),
                      Column('Cust_Cat',
                             String(length=5),
                             nullable=True,
                             index=True,
                             doc='Customer Category Code',
                             comment='The customer category code that is linked to a price matrix.'),
                      Column('Cust_Num',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number.'),
                      Column('Ship_To_Code',
                             String(length=8),
                             nullable=True,
                             index=True,
                             doc='Ship To Code',
                             comment='The Ship To code number'),
                      Column('Major_Group',
                             String(length=5),
                             nullable=True,
                             doc='Major Group',
                             comment='The product Major Group.'),
                      Column('Prod_Line',
                             String(length=10),
                             nullable=True,
                             doc='Product Line',
                             comment='The product line code. Use this to display price matrices directly linked to a'
                                     'product line.'),
                      Column('Price_Group_Code',
                             String(length=8),
                             nullable=True,
                             doc='Price Group Code',
                             comment='The Price Group code.'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product Number',
                             comment='The product number'),
                      Column('Qty_Break',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Quantity Break',
                             comment='The quantity break value.'),
                      Column('Qty_Break_Count',
                             Integer,
                             nullable=True,
                             doc='Quantity Break Count',
                             comment='The number of quantity breaks for the price matrix.'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor Number',
                             comment='The vendor number field.'),
                      Column('Cntr_Num',
                             String(length=15),
                             nullable=True,
                             doc='Contract Number',
                             comment='The contract number.'),
                      Column('Price_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Net Factor Price Amount',
                             comment='This is the value found in the Amount field for price'),
                      Column('Price_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Percent / Dollar Sign',
                             comment='This field will show a % or a $ sign based on the type of formula used.'),
                      Column('Price_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Plus / Minus Sign',
                             comment='This field will show a + or - sign based on the type of formula used'),
                      Column('Price_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Price C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining sales price. This is cost,'
                                     'list, net, or calculated cost'),
                      Column('Cost_Amount',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Amount',
                             comment='The cost that is displayed in the amount field of the price matrix.'),
                      Column('Cost_CLN',
                             String(length=3),
                             nullable=True,
                             doc='Cost C/L/N',
                             comment='The C/L/N base field in Price Matrix for determining cost. This is cost, list,'
                                     'or net'),
                      Column('Cost_Net_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Cost Net Factor',
                             comment='Cost net factor'),
                      Column('Cost_Pcnt_Dollar',
                             String(length=1),
                             nullable=True,
                             doc='Cost Percent / Dollar',
                             comment='This field will show a % or a $ sign based on the type of cost formula used.'),
                      Column('Cost_Plus_Minus',
                             String(length=1),
                             nullable=True,
                             doc='Cost Plus / Minus',
                             comment='Cost Plus/Minus'),
                      Column('Load_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Load Percent',
                             comment='The load percent used on the rebate cost.'),
                      Column('Mixed_Breaks',
                             String(length=12),
                             nullable=True,
                             doc='Mixed Breaks',
                             comment='This is a Y or N value'),
                      Column('Mixed_Breaks_Method',
                             String(length=10),
                             nullable=True,
                             doc='Mixed Breaks Method',
                             comment='When using mixed breaks, will show (Q) Quantity, ($) Dollar Breaks, or (W)'
                                     'Weight'),
                      Column('Purchase_Cntr',
                             String(length=8),
                             nullable=True,
                             doc='Purchase Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Salesman',
                             String(length=4),
                             nullable=True,
                             doc='Salesman',
                             comment='The salesperson assigned to the customer, for a customer"s price matrix.'),
                      Column('Web_Cntr',
                             String(length=12),
                             nullable=True,
                             doc='Web Contract',
                             comment='This determines if the price contract is a web contract or not.'),
                      Column('Co_Op_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Co Op Percent',
                             comment='The Co Op Percent amount'),
                      Column('Eff_Date',
                             Date,
                             nullable=True,
                             doc='Effective Date',
                             comment='The start date for the price matrix'),
                      Column('Exp_Date',
                             Date,
                             nullable=True,
                             doc='Expiration Date',
                             comment='The expiration date for the price matrix.'),
                      Column('Future_Price_Date',
                             Date,
                             nullable=True,
                             doc='Future Price Date',
                             comment='The date in which the future price matrix will take effect'),
                      Column('Date_Stamp',
                             Date,
                             nullable=True,
                             doc='Date Stamp',
                             comment='The date stamp for the price matrix.'),
                      Column('Time_Stamp',
                             Time,
                             nullable=True,
                             doc='Time Stamp',
                             comment='The time stamp for the price matrix. This only shows the time (i.e. 5:09pm)'),
                      Column('Last_Update_Date',
                             Date,
                             nullable=True,
                             doc='Last Update Date',
                             comment='The last date the price matrix was updated. "'),
                      Column('Last_Update_Initials',
                             String(length=3),
                             nullable=True,
                             doc='Last Update Initials',
                             comment='The user who last updated the price matrix'),
                      Column('Entered_By',
                             String(length=6),
                             nullable=True,
                             doc='Entered By',
                             comment='The user who entered the price matrix.'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date the price matrix was created.'),
                      schema='price.matrix')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))

    @hybrid_property
    def Price_Net_Plus_Minus(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Price_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Price_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Price_Net_Factor * -1
            else:
                return self.__table__.c.Price_Net_Factor
    
    # noinspection PyMethodParameters
    @Price_Net_Plus_Minus.expression
    def Price_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Plus_Minus) == "-",
                                (cls.__table__.c.Price_Net_Factor * -1))
                           ], else_=cls.__table__.c.Price_Net_Factor
                       )
                       )

    @hybrid_property
    def Price_Net_Pct_Dollar(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Price_Net_Plus_Minus / 100
            else:
                return self.Price_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Price_Net_Pct_Dollar.expression
    def Price_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%", (cls.Price_Net_Plus_Minus / 100))
    
                           ], else_=cls.Price_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Price_Reference(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Price_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Price_Reference.expression
    def Price_Reference(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Price_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Price_Net(self):
        if self.__table__.c.Price_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Price_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Price_Net_Pct_Dollar) * self.Price_Reference
            else:
                return self.Price_Net_Pct_Dollar + self.Price_Reference
    
    # noinspection PyMethodParameters
    @Price_Net.expression
    def Price_Net(cls):
        return func.IF(cls.__table__.c.Price_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Price_Pcnt_Dollar) == "%",
                                ((1 + cls.Price_Net_Pct_Dollar) * cls.Price_Reference))
                           ], else_=(cls.Price_Net_Pct_Dollar + cls.Price_Reference)
                       )
                       )

    @hybrid_property
    def Cost_Net_Plus_Minus(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            if self.__table__.c.Cost_Plus_Minus is None:
                sign = None
            else:
                sign = str(self.__table__.c.Cost_Plus_Minus).strip()
    
            if sign == "-":
                return self.__table__.c.Cost_Net_Factor * -1
            else:
                return self.__table__.c.Cost_Net_Factor
    
    # noinspection PyMethodParameters
    @Cost_Net_Plus_Minus.expression
    def Cost_Net_Plus_Minus(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Plus_Minus) == "-",
                                (cls.__table__.c.Cost_Net_Factor * -1))
                           ], else_=cls.__table__.c.Cost_Net_Factor
                       )
                       )

    @hybrid_property
    def Cost_Net_Pct_Dollar(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == "%":
                return self.Cost_Net_Plus_Minus / 100
            else:
                return self.Cost_Net_Plus_Minus
    
    # noinspection PyMethodParameters
    @Cost_Net_Pct_Dollar.expression
    def Cost_Net_Pct_Dollar(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%", (cls.Cost_Net_Plus_Minus / 100))
    
                           ], else_=cls.Cost_Net_Plus_Minus
                       )
                       )

    @hybrid_property
    def Cost_Reference(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            ref = str(self.__table__.c.Cost_CLN).strip().upper()
            if ref == 'C1':
                return None
            if ref == 'C2':
                return None
            if ref == 'C3':
                return None
            if ref == 'C4':
                return None
            if ref == 'C5':
                return None
            if ref == 'C6':
                return None
            if ref == 'C7':
                return None
            if ref == 'L1':
                return None
            if ref == 'L2':
                return None
            if ref == 'L3':
                return None
            if ref == 'L4':
                return None
            if ref == 'N':
                return None
            else:
                return None
    
    # noinspection PyMethodParameters
    @Cost_Reference.expression
    def Cost_Reference(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C4", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C5", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C6", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "C7", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L1", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L2", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L3", None),
                               (func.upper(func.trim(cls.__table__.c.Cost_CLN)) == "L4", None)
                           ], else_=None
                       )
                       )

    @hybrid_property
    def Cost_Net(self):
        if self.__table__.c.Cost_Net_Factor is None:
            return None
        else:
            sign = str(self.__table__.c.Cost_Pcnt_Dollar).strip()
    
            if sign == '%':
                return (1 + self.Cost_Net_Pct_Dollar) * self.Cost_Reference
            else:
                return self.Cost_Net_Pct_Dollar + self.Cost_Reference
    
    # noinspection PyMethodParameters
    @Cost_Net.expression
    def Cost_Net(cls):
        return func.IF(cls.__table__.c.Cost_Net_Factor.is_(None),
                       None,
                       case(
                           [
                               (func.trim(cls.__table__.c.Cost_Pcnt_Dollar) == "%",
                                ((1 + cls.Cost_Net_Pct_Dollar) * cls.Cost_Reference))
                           ], else_=(cls.Cost_Net_Pct_Dollar + cls.Cost_Reference)
                       )
                       )


# noinspection PyPep8Naming
class prod_line_01_static(server_utils.mysql_base):
    __table__ = Table('prod_line_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=12),
                             nullable=True,
                             doc='Code',
                             comment='Code'),
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_main_01_current(server_utils.mysql_base):
    __table__ = Table('prod_line_main_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=12),
                             nullable=True,
                             doc='Code',
                             comment='Code'),
                      Column('Desc',
                             String(length=255),
                             nullable=True,
                             doc='Description',
                             comment='The description for the Product Line'),
                      Column('Major_Group',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Major Group Code',
                             comment='The  reference code for the Major Group that the Product Line is assigned to'),
                      Column('Consignment_Vend',
                             String(length=9),
                             nullable=True,
                             index=True,
                             doc='Consignment Vendor',
                             comment='The reference code of the Consignment Vendor for the Product Line'),
                      Column('Min_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Minimum GP Percent',
                             comment='The minimum Gross Profit percent expected for the Product Line. Items that fall'
                                     'below this threshold will display a below minimum message during sales order'
                                     'entry.'),
                      Column('Buyers',
                             String(length=255),
                             nullable=True,
                             doc='Buyers',
                             comment='The system initials of all the users who are identified as buyers for the'
                                     'product line"'),
                      Column('Allow_GL_Posting',
                             String(length=2),
                             nullable=True,
                             doc='Allow GL Posting',
                             comment='This Y/N field indicates if the "Allow G/L Posting from A/P and A/R" box is'
                                     'checked for the Product Line'),
                      Column('L1_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L1 Description',
                             comment='The description entered for the L1 price field for the Product Line'),
                      Column('L2_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L2 Description',
                             comment='The description entered for the L2 price field for the Product Line'),
                      Column('L3_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L3 Description',
                             comment='The description entered for the L3 price field for the Product Line'),
                      Column('L4_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L4 Description',
                             comment='The description entered for the L4 price field for the Product Line'),
                      Column('Inventory_GL',
                             Integer,
                             nullable=True,
                             doc='Inventory GL',
                             comment='The General Ledger account number for Inventory postings for the Product Line.'
                                     'If this field is blank, these products will use the default Inventory account'
                                     'set for the Branch or Company.'),
                      Column('Inventory_GL_Num',
                             Integer,
                             nullable=True,
                             doc='Inventory GL Number',
                             comment='Inventory GL Number Override'),
                      Column('Cost_of_Goods_GL',
                             Integer,
                             nullable=True,
                             doc='Cost of Goods GL',
                             comment='The General Ledger account number for Cost of Goods Sold postings for the'
                                     'Product Line. If this field is blank, these products will use the default Cost'
                                     'of Goods Sold account set for the Branch or Company.'),
                      Column('Direct_Ship_Cost_of_Goods_GL',
                             Integer,
                             nullable=True,
                             doc='Direct Ship Cost of Goods GL',
                             comment='The General Ledger account number for Direct Ship Cost of Goods Sold postings'
                                     'for the Product Line. If this field is blank, these products will use the'
                                     'default Direct Ship Cost of Goods Sold account set for the Branch or Comp'),
                      Column('Sales_GL_Num',
                             Integer,
                             nullable=True,
                             doc='Sales GL Number',
                             comment='Sales GL Number Override'),
                      Column('Sales_Returns_GL_Num',
                             Integer,
                             nullable=True,
                             doc='Sales Returns GL Number',
                             comment='Sales Returns GL Number'),
                      Column('Direct_Ship_Sales_GL',
                             Integer,
                             nullable=True,
                             doc='Direct Ship Sales GL',
                             comment='The General Ledger account number for Direct Ship Sales postings for the'
                                     'Product Line. If this field is blank, these products will use the default'
                                     'Direct Ship Sales account set for the Branch or Company.'),
                      Column('Inventory_Change_GL',
                             Integer,
                             nullable=True,
                             doc='Inventory Change GL',
                             comment='The General Ledger account number for Inventory Change postings for the Product'
                                     'Line. If this field is blank, these products will use the default Inventory'
                                     'Change account set for the Branch or Company.'),
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_main_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_line_main_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=12),
                             nullable=True,
                             doc='Code',
                             comment='Code'),
                      Column('Desc',
                             String(length=255),
                             nullable=True,
                             doc='Description',
                             comment='The description for the Product Line'),
                      Column('Major_Group',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Major Group Code',
                             comment='The  reference code for the Major Group that the Product Line is assigned to'),
                      Column('Consignment_Vend',
                             String(length=9),
                             nullable=True,
                             index=True,
                             doc='Consignment Vendor',
                             comment='The reference code of the Consignment Vendor for the Product Line'),
                      Column('Min_GP_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Minimum GP Percent',
                             comment='The minimum Gross Profit percent expected for the Product Line. Items that fall'
                                     'below this threshold will display a below minimum message during sales order'
                                     'entry.'),
                      Column('Buyers',
                             String(length=255),
                             nullable=True,
                             doc='Buyers',
                             comment='The system initials of all the users who are identified as buyers for the'
                                     'product line"'),
                      Column('Allow_GL_Posting',
                             String(length=2),
                             nullable=True,
                             doc='Allow GL Posting',
                             comment='This Y/N field indicates if the "Allow G/L Posting from A/P and A/R" box is'
                                     'checked for the Product Line'),
                      Column('L1_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L1 Description',
                             comment='The description entered for the L1 price field for the Product Line'),
                      Column('L2_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L2 Description',
                             comment='The description entered for the L2 price field for the Product Line'),
                      Column('L3_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L3 Description',
                             comment='The description entered for the L3 price field for the Product Line'),
                      Column('L4_Desc',
                             LONGTEXT,
                             nullable=True,
                             doc='L4 Description',
                             comment='The description entered for the L4 price field for the Product Line'),
                      Column('Inventory_GL',
                             Integer,
                             nullable=True,
                             doc='Inventory GL',
                             comment='The General Ledger account number for Inventory postings for the Product Line.'
                                     'If this field is blank, these products will use the default Inventory account'
                                     'set for the Branch or Company.'),
                      Column('Inventory_GL_Num',
                             Integer,
                             nullable=True,
                             doc='Inventory GL Number',
                             comment='Inventory GL Number Override'),
                      Column('Cost_of_Goods_GL',
                             Integer,
                             nullable=True,
                             doc='Cost of Goods GL',
                             comment='The General Ledger account number for Cost of Goods Sold postings for the'
                                     'Product Line. If this field is blank, these products will use the default Cost'
                                     'of Goods Sold account set for the Branch or Company.'),
                      Column('Direct_Ship_Cost_of_Goods_GL',
                             Integer,
                             nullable=True,
                             doc='Direct Ship Cost of Goods GL',
                             comment='The General Ledger account number for Direct Ship Cost of Goods Sold postings'
                                     'for the Product Line. If this field is blank, these products will use the'
                                     'default Direct Ship Cost of Goods Sold account set for the Branch or Comp'),
                      Column('Sales_GL_Num',
                             Integer,
                             nullable=True,
                             doc='Sales GL Number',
                             comment='Sales GL Number Override'),
                      Column('Sales_Returns_GL_Num',
                             Integer,
                             nullable=True,
                             doc='Sales Returns GL Number',
                             comment='Sales Returns GL Number'),
                      Column('Direct_Ship_Sales_GL',
                             Integer,
                             nullable=True,
                             doc='Direct Ship Sales GL',
                             comment='The General Ledger account number for Direct Ship Sales postings for the'
                                     'Product Line. If this field is blank, these products will use the default'
                                     'Direct Ship Sales account set for the Branch or Company.'),
                      Column('Inventory_Change_GL',
                             Integer,
                             nullable=True,
                             doc='Inventory Change GL',
                             comment='The General Ledger account number for Inventory Change postings for the Product'
                                     'Line. If this field is blank, these products will use the default Inventory'
                                     'Change account set for the Branch or Company.'),
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_notes_01_current(server_utils.mysql_base):
    __table__ = Table('prod_line_notes_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=12),
                             nullable=True,
                             doc='Code',
                             comment='Code'),
                      Column('Int_Notes',
                             String(length=255),
                             nullable=True,
                             doc='Internal Notes',
                             comment='The Internal Notes entered for the Product Line.'),
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_notes_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_line_notes_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Code',
                             String(length=12),
                             nullable=True,
                             doc='Code',
                             comment='Code'),
                      Column('Int_Notes',
                             String(length=255),
                             nullable=True,
                             doc='Internal Notes',
                             comment='The Internal Notes entered for the Product Line.'),
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_01_static(server_utils.mysql_base):
    __table__ = Table('prod_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_01_current(server_utils.mysql_base):
    __table__ = Table('prod_assembly_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Kit_Production',
                             String(length=3),
                             nullable=True,
                             doc='Kit Production',
                             comment='This Y/N field denotes if the product is flagged as a Kit Production assembly'
                                     'item'),
                      Column('Assembly_Print',
                             String(length=14),
                             nullable=True,
                             doc='Assembly Print',
                             comment='This Y/N field indicates if the assembly components will print on a Sales Order'),
                      Column('Disassemble',
                             String(length=15),
                             nullable=True,
                             doc='Disassemble',
                             comment='Disassemble? Y/N. Workflow option in company Masterfile -"Auto Disassemble upon'
                                     'Receiving"'),
                      Column('Assembly_Rollup',
                             String(length=15),
                             nullable=True,
                             doc='Assembly Rollup',
                             comment='The rollup settings on any assembled products (P = Price, C = Cost, B = Both, N'
                                     '= None)'),
                      Column('Assembled_Parent',
                             String(length=8),
                             nullable=True,
                             doc='Assembled Parent',
                             comment='This Y/N field designates whether or not the item is a parent assembly'),
                      Column('Comp_IDs',
                             String(length=14),
                             nullable=True,
                             doc='Component IDs',
                             comment='The product number for all assembly components'),
                      Column('No_of_Comps',
                             Integer,
                             nullable=True,
                             doc='No of Components',
                             comment='The quantity of the Assembly components, per assembly. This field will only'
                                     'display for assembly or kit production items.'),
                      Column('Comp_Prod_Disassemble_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Component Product Disassemble Percent',
                             comment='When using the company master disassemble flag. Total for all components have'
                                     'to equal 100%'),
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_assembly_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Kit_Production',
                             String(length=3),
                             nullable=True,
                             doc='Kit Production',
                             comment='This Y/N field denotes if the product is flagged as a Kit Production assembly'
                                     'item'),
                      Column('Assembly_Print',
                             String(length=14),
                             nullable=True,
                             doc='Assembly Print',
                             comment='This Y/N field indicates if the assembly components will print on a Sales Order'),
                      Column('Disassemble',
                             String(length=15),
                             nullable=True,
                             doc='Disassemble',
                             comment='Disassemble? Y/N. Workflow option in company Masterfile -"Auto Disassemble upon'
                                     'Receiving"'),
                      Column('Assembly_Rollup',
                             String(length=15),
                             nullable=True,
                             doc='Assembly Rollup',
                             comment='The rollup settings on any assembled products (P = Price, C = Cost, B = Both, N'
                                     '= None)'),
                      Column('Assembled_Parent',
                             String(length=8),
                             nullable=True,
                             doc='Assembled Parent',
                             comment='This Y/N field designates whether or not the item is a parent assembly'),
                      Column('Comp_IDs',
                             String(length=14),
                             nullable=True,
                             doc='Component IDs',
                             comment='The product number for all assembly components'),
                      Column('No_of_Comps',
                             Integer,
                             nullable=True,
                             doc='No of Components',
                             comment='The quantity of the Assembly components, per assembly. This field will only'
                                     'display for assembly or kit production items.'),
                      Column('Comp_Prod_Disassemble_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Component Product Disassemble Percent',
                             comment='When using the company master disassemble flag. Total for all components have'
                                     'to equal 100%'),
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_notes_01_current(server_utils.mysql_base):
    __table__ = Table('prod_assembly_notes_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Comp_IDs',
                             String(length=14),
                             nullable=True,
                             doc='Component IDs',
                             comment='The product number for all assembly components'),
                      Column('Comp_Notes',
                             String(length=30),
                             nullable=True,
                             doc='Component Notes',
                             comment='For a kit production master item, the components can have notes tailored to'
                                     'each specific component.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_notes_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_assembly_notes_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Comp_IDs',
                             String(length=14),
                             nullable=True,
                             doc='Component IDs',
                             comment='The product number for all assembly components'),
                      Column('Comp_Notes',
                             String(length=30),
                             nullable=True,
                             doc='Component Notes',
                             comment='For a kit production master item, the components can have notes tailored to'
                                     'each specific component.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_ext_po_cmnts_01_current(server_utils.mysql_base):
    __table__ = Table('prod_ext_po_cmnts_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('PO_Comment',
                             String(length=30),
                             nullable=True,
                             doc='PO Comment',
                             comment='The P/O Comments for the product'),
                      schema='product')


# noinspection PyPep8Naming
class prod_ext_po_cmnts_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_ext_po_cmnts_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('PO_Comment',
                             String(length=30),
                             nullable=True,
                             doc='PO Comment',
                             comment='The P/O Comments for the product'),
                      schema='product')


# noinspection PyPep8Naming
class prod_general_01_current(server_utils.mysql_base):
    __table__ = Table('prod_general_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Sort_Seq_Num',
                             String(length=15),
                             nullable=True,
                             doc='Sort Sequence Number',
                             comment='The Sort Sequence Number'),
                      Column('AR_Inv_Disc',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AR Invoice Discount',
                             comment='The override Cash Receipt Discount % for this product'),
                      Column('MFG_Class_Code',
                             String(length=255),
                             nullable=True,
                             doc='MFG Class Code',
                             comment='The manufacturer"s Class Code for the product'),
                      Column('Catalog_Page',
                             String(length=255),
                             nullable=True,
                             doc='Catalog Page',
                             comment='The Catalog Page Number for the product'),
                      Column('Catalog_Section',
                             String(length=255),
                             nullable=True,
                             doc='Catalog Section',
                             comment='The catalog section for the product'),
                      Column('Pricing_Srvc_Velocity',
                             String(length=255),
                             nullable=True,
                             doc='Pricing Service Velocity',
                             comment='The Pricing Service Velocity code'),
                      Column('Pricing_Srvc_Template',
                             String(length=255),
                             nullable=True,
                             doc='Pricing Service Template',
                             comment='The Pricing Service custom mapping template'),
                      Column('Prod_Tax_Group_Code',
                             String(length=14),
                             nullable=True,
                             doc='Product Tax Group Code',
                             comment='The reference code for the Product Tax Group. For more information, link to the'
                                     'Product  Tax Group file.'),
                      Column('Cycle_Group_Code',
                             String(length=11),
                             nullable=True,
                             doc='Cycle Group Code',
                             comment='The reference code for the Cycle  Group for the product.'),
                      Column('Recvd_Label_ID',
                             String(length=15),
                             nullable=True,
                             doc='Recvd Label ID',
                             comment='The Product Label Code for the product - when the product is received, this'
                                     'label will print for it.'),
                      Column('MSDS_Code',
                             String(length=10),
                             nullable=True,
                             doc='MSDS Code',
                             comment='The ID code for the M.S.D.S.'),
                      Column('MSDS_Code_Date',
                             Date,
                             nullable=True,
                             doc='MSDS Code Date',
                             comment='The date that the M.S.D.S. information was last updated.'),
                      Column('Cert_Code',
                             String(length=255),
                             nullable=True,
                             doc='Certification Code',
                             comment='The Certification Code for the product as entered under the general tab'),
                      Column('Commisionable',
                             String(length=14),
                             nullable=True,
                             doc='Commisionable',
                             comment='The commissionable status: Y = Yes, N = No, S = Split'),
                      Column('Taxable',
                             String(length=7),
                             nullable=True,
                             doc='Taxable',
                             comment='This Y/N field indicates if the Taxable box is checked for the product. This is'
                                     'a default setting and may be overridden on orders by settings in the customer"s'
                                     'Tax Matrix'),
                      Column('Tax_Freight',
                             String(length=11),
                             nullable=True,
                             doc='Tax Freight',
                             comment='This Y/N field indicates if the Tax Freight box is checked'),
                      Column('Serial_Num_Req',
                             String(length=22),
                             nullable=True,
                             doc='Serial Number Required',
                             comment='This (Y)es/(N)o field indicates if the product requires serial numbers'),
                      Column('Lot_Control',
                             String(length=11),
                             nullable=True,
                             doc='Lot Control',
                             comment='This Y/N field indicates if the product is tracked by lot'),
                      Column('Vend_Returnable',
                             String(length=17),
                             nullable=True,
                             doc='Vendor Returnable',
                             comment='Is the product returnable to vendor? Y/N'),
                      Column('Whse_Pick',
                             String(length=9),
                             nullable=True,
                             doc='Whse Pick',
                             comment='This Y/N field indicates if the product has the Warehouse Pick box checked'),
                      Column('Display_Item',
                             String(length=19),
                             nullable=True,
                             doc='Display Item',
                             comment='This (Y)es/(N)o field indicates if the Showroom Display box is checked.'),
                      Column('Repair',
                             String(length=11),
                             nullable=True,
                             doc='Repair',
                             comment='This Y/N field indicates if the product is designated as a repair item.'),
                      Column('Disable_Margin_Price',
                             String(length=20),
                             nullable=True,
                             doc='Disable Margin Price',
                             comment='This Y/N field indicates if the product is set to disable margin pricing.'),
                      Column('Coop_Item',
                             String(length=13),
                             nullable=True,
                             doc='Coop Item',
                             comment='This Y/N field indicates if this product is eligible for co-op percent"s to be'
                                     'taken in Sales Orders for customers enrolled in the Customer Rewards Program.'),
                      Column('Disable_SO_Cost_Change',
                             String(length=22),
                             nullable=True,
                             doc='Disable S/O Cost Change',
                             comment='This Y/N field indicates if the check box to disable cost change in the Sales'
                                     'Order is checked.'),
                      Column('End_User_Rebate',
                             String(length=18),
                             nullable=True,
                             doc='End User Rebate',
                             comment='End User Rebate'),
                      schema='product')


# noinspection PyPep8Naming
class prod_general_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_general_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Sort_Seq_Num',
                             String(length=15),
                             nullable=True,
                             doc='Sort Sequence Number',
                             comment='The Sort Sequence Number'),
                      Column('AR_Inv_Disc',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AR Invoice Discount',
                             comment='The override Cash Receipt Discount % for this product'),
                      Column('MFG_Class_Code',
                             String(length=255),
                             nullable=True,
                             doc='MFG Class Code',
                             comment='The manufacturer"s Class Code for the product'),
                      Column('Catalog_Page',
                             String(length=255),
                             nullable=True,
                             doc='Catalog Page',
                             comment='The Catalog Page Number for the product'),
                      Column('Catalog_Section',
                             String(length=255),
                             nullable=True,
                             doc='Catalog Section',
                             comment='The catalog section for the product'),
                      Column('Pricing_Srvc_Velocity',
                             String(length=255),
                             nullable=True,
                             doc='Pricing Service Velocity',
                             comment='The Pricing Service Velocity code'),
                      Column('Pricing_Srvc_Template',
                             String(length=255),
                             nullable=True,
                             doc='Pricing Service Template',
                             comment='The Pricing Service custom mapping template'),
                      Column('Prod_Tax_Group_Code',
                             String(length=14),
                             nullable=True,
                             doc='Product Tax Group Code',
                             comment='The reference code for the Product Tax Group. For more information, link to the'
                                     'Product  Tax Group file.'),
                      Column('Cycle_Group_Code',
                             String(length=11),
                             nullable=True,
                             doc='Cycle Group Code',
                             comment='The reference code for the Cycle  Group for the product.'),
                      Column('Recvd_Label_ID',
                             String(length=15),
                             nullable=True,
                             doc='Recvd Label ID',
                             comment='The Product Label Code for the product - when the product is received, this'
                                     'label will print for it.'),
                      Column('MSDS_Code',
                             String(length=10),
                             nullable=True,
                             doc='MSDS Code',
                             comment='The ID code for the M.S.D.S.'),
                      Column('MSDS_Code_Date',
                             Date,
                             nullable=True,
                             doc='MSDS Code Date',
                             comment='The date that the M.S.D.S. information was last updated.'),
                      Column('Cert_Code',
                             String(length=255),
                             nullable=True,
                             doc='Certification Code',
                             comment='The Certification Code for the product as entered under the general tab'),
                      Column('Commisionable',
                             String(length=14),
                             nullable=True,
                             doc='Commisionable',
                             comment='The commissionable status: Y = Yes, N = No, S = Split'),
                      Column('Taxable',
                             String(length=7),
                             nullable=True,
                             doc='Taxable',
                             comment='This Y/N field indicates if the Taxable box is checked for the product. This is'
                                     'a default setting and may be overridden on orders by settings in the customer"s'
                                     'Tax Matrix'),
                      Column('Tax_Freight',
                             String(length=11),
                             nullable=True,
                             doc='Tax Freight',
                             comment='This Y/N field indicates if the Tax Freight box is checked'),
                      Column('Serial_Num_Req',
                             String(length=22),
                             nullable=True,
                             doc='Serial Number Required',
                             comment='This (Y)es/(N)o field indicates if the product requires serial numbers'),
                      Column('Lot_Control',
                             String(length=11),
                             nullable=True,
                             doc='Lot Control',
                             comment='This Y/N field indicates if the product is tracked by lot'),
                      Column('Vend_Returnable',
                             String(length=17),
                             nullable=True,
                             doc='Vendor Returnable',
                             comment='Is the product returnable to vendor? Y/N'),
                      Column('Whse_Pick',
                             String(length=9),
                             nullable=True,
                             doc='Whse Pick',
                             comment='This Y/N field indicates if the product has the Warehouse Pick box checked'),
                      Column('Display_Item',
                             String(length=19),
                             nullable=True,
                             doc='Display Item',
                             comment='This (Y)es/(N)o field indicates if the Showroom Display box is checked.'),
                      Column('Repair',
                             String(length=11),
                             nullable=True,
                             doc='Repair',
                             comment='This Y/N field indicates if the product is designated as a repair item.'),
                      Column('Disable_Margin_Price',
                             String(length=20),
                             nullable=True,
                             doc='Disable Margin Price',
                             comment='This Y/N field indicates if the product is set to disable margin pricing.'),
                      Column('Coop_Item',
                             String(length=13),
                             nullable=True,
                             doc='Coop Item',
                             comment='This Y/N field indicates if this product is eligible for co-op percent"s to be'
                                     'taken in Sales Orders for customers enrolled in the Customer Rewards Program.'),
                      Column('Disable_SO_Cost_Change',
                             String(length=22),
                             nullable=True,
                             doc='Disable S/O Cost Change',
                             comment='This Y/N field indicates if the check box to disable cost change in the Sales'
                                     'Order is checked.'),
                      Column('End_User_Rebate',
                             String(length=18),
                             nullable=True,
                             doc='End User Rebate',
                             comment='End User Rebate'),
                      schema='product')


# noinspection PyPep8Naming
class prod_int_po_cmnts_01_current(server_utils.mysql_base):
    __table__ = Table('prod_int_po_cmnts_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('PO_Int_Comment',
                             String(length=30),
                             nullable=True,
                             doc='PO Internal Comment',
                             comment='The PO Internal Comment field.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_int_po_cmnts_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_int_po_cmnts_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('PO_Int_Comment',
                             String(length=30),
                             nullable=True,
                             doc='PO Internal Comment',
                             comment='The PO Internal Comment field.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_keywords_01_current(server_utils.mysql_base):
    __table__ = Table('prod_keywords_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('All_Keywords',
                             String(length=255),
                             nullable=True,
                             doc='All Keywords',
                             comment='Lists all of the keywords entered for the product.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_keywords_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_keywords_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('All_Keywords',
                             String(length=255),
                             nullable=True,
                             doc='All Keywords',
                             comment='Lists all of the keywords entered for the product.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_main_01_current(server_utils.mysql_base):
    __table__ = Table('prod_main_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Status',
                             String(length=2),
                             nullable=True,
                             doc='Status',
                             comment='The Special Status of the Product Blank or A = Active, N = Non-Stock, D ='
                                     'Disconnected, I = Inactive, C = Consumable'),
                      Column('Entered_By',
                             String(length=6),
                             nullable=True,
                             doc='Entered By',
                             comment='The system initials of the user who created the product'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date that the product file was created'),
                      Column('Desc_Full',
                             LONGTEXT,
                             nullable=True,
                             doc='Description Full',
                             comment='The complete product description'),
                      Column('Quote_Desc_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Quote Description Flat',
                             comment='The Product Quote description flattened into a single value.'),
                      Column('Catalog_Desc',
                             String(length=30),
                             nullable=True,
                             doc='Catalog Description',
                             comment='The catalog description for the product.'),
                      Column('Prod_Line',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Product Line Code',
                             comment='The Product Line Code'),
                      Column('Price_Group_Code',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Price Group Code',
                             comment='The reference code for the product"s price group. For more information, link to'
                                     'the Price Group file.'),
                      Column('Buy_Line_Code',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Buy Line Code',
                             comment='The reference code for the product"s Buy Line. For more Buy Line information,'
                                     'link to the Buy Line file.'),
                      Column('Consignment_Vend_Num',
                             String(length=10),
                             nullable=True,
                             doc='Consignment Vendor Number',
                             comment='The Vendor Number for the product"s consignment vendor.'),
                      Column('HazMat_Code',
                             String(length=8),
                             nullable=True,
                             doc='HazMat Code',
                             comment='The Haz Mat code for the product.'),
                      Column('Mfg_No',
                             String(length=255),
                             nullable=True,
                             doc='Manufacturer No',
                             comment='The default manufacturer"s number'),
                      Column('UPC',
                             String(length=12),
                             nullable=True,
                             index=True,
                             doc='UPC',
                             comment='The UPC Code for the product'),
                      Column('UPC_14',
                             String(length=30),
                             nullable=True,
                             index=True,
                             doc='UPC (14)',
                             comment='The UPC code limited to a column 12 characters wide'),
                      Column('Pricing_Srvc_Num',
                             String(length=30),
                             nullable=True,
                             doc='Pricing Service Number',
                             comment='The Pricing Service Number for the product'),
                      Column('Display_UOM',
                             String(length=3),
                             nullable=True,
                             doc='Display UOM',
                             comment='The display or default selling Unit of Measure'),
                      Column('UOM_Qty_Factor',
                             Integer,
                             nullable=True,
                             doc='UOM Qty Factor',
                             comment='The Unit of Measure factor for the default Selling Unit of Measure.'),
                      Column('Price_UOM',
                             String(length=9),
                             nullable=True,
                             doc='Price UOM',
                             comment='The default Pricing Unit of Measure'),
                      Column('UOM_Price_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='UOM Price Factor',
                             comment='The quantity factor between the Price UOM and the display UOM'),
                      Column('Purch_UOM',
                             String(length=12),
                             nullable=True,
                             doc='Purchase UOM',
                             comment='The default Purchasing Unit of Measure'),
                      Column('UOM_Purch_Qty_Factor',
                             Integer,
                             nullable=True,
                             doc='UOM Purchase Qty Factor',
                             comment='The Unit of Measure factor for the default purchasing Unit of Measure'),
                      Column('UOM_Units',
                             Integer,
                             nullable=True,
                             doc='UOM Units',
                             comment='The total number of units of measure on the product'),
                      Column('C1_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C1 Cost',
                             comment='The current C1 Standard Cost for the product. C1 is a user-maintained field,'
                                     'typically representing the replacement cost or product base cost. C1 may be'
                                     'calculated by a price rollup formula and may be changed by hand entry, m'),
                      Column('C1_Date',
                             Date,
                             nullable=True,
                             doc='C1 Date',
                             comment='the date that the C1 Cost field was last changed'),
                      Column('C2_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C2 Cost',
                             comment='The current C2 Weighted Average cost for the product. C2 is calculated by stock'
                                     'receiving. Weighted average cost is based on the value of existing inventory,'
                                     'plus the value of newly received inventory, divided by the total qu'),
                      Column('C2_Date',
                             Date,
                             nullable=True,
                             doc='C2 Date',
                             comment='The date that the C2 Cost field was last changed.'),
                      Column('C3_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C3 Cost',
                             comment='The current C3 Landed cost for the product. C3 includes all freight costs from'
                                     'the stock receipt or account payable invoice, and is calculated by stock'
                                     'receiving or accounts payable entry. Landed weighted average cost is base'),
                      Column('C3_Date',
                             Date,
                             nullable=True,
                             doc='C3 Date',
                             comment='The date that the C3 Cost field was last changed.'),
                      Column('C4_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C4 Cost',
                             comment='The current C4 Cost for the product. C4 is a user-maintained field, typically'
                                     'representing the loaded salespersons cost other formula derived cost. C4 may be'
                                     'calculated by a Price Rollup formula, and may be edited by hand ent'),
                      Column('C4_Date',
                             Date,
                             nullable=True,
                             doc='C4 Date',
                             comment='The most recent date that the C4 Cost was changed'),
                      Column('C5_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C5 Cost',
                             comment='The current C5 last Purchase Order Cost for the product. C5 is a system'
                                     'calculated cost derived from the purchase order / stock receiving cost. It is'
                                     'updated from Stock Receipts at the time of purchase order receiving. C5 cos'),
                      Column('C5_Date',
                             Date,
                             nullable=True,
                             doc='C5 Date',
                             comment='The date of the most recent purchase order.'),
                      Column('C6_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C6 Cost',
                             comment='The current C6 Cost for the product. C6 is a user-maintained field, typically'
                                     'derived from a formula based on C1, C2, or C5. C6 can be calculated by a Price'
                                     'Rollup formula, and may be edited by hand entry or mass change.'),
                      Column('C6_Date',
                             Date,
                             nullable=True,
                             doc='C6 Date',
                             comment='The most recent date that the C6 Cost was changed'),
                      Column('C7_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C7 Cost',
                             comment='The current C7 Cost for the product. C7 is a user-maintained field, typically'
                                     'derived from a formula based on C1, C2, or C5. C7 may be calculated by a Price'
                                     'Rollup formula and may be edited by hand entry or mass change.'),
                      Column('C7_Date',
                             Date,
                             nullable=True,
                             doc='C7 Date',
                             comment='The most recent date that the C7 Cost was changed'),
                      Column('L1_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 1',
                             comment='The L1 List Price'),
                      Column('L1_Date',
                             Date,
                             nullable=True,
                             doc='L1 Date',
                             comment='The date that the L1 List price field was last changed'),
                      Column('L2_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 2',
                             comment='The L2 Price'),
                      Column('L2_Date',
                             Date,
                             nullable=True,
                             doc='L2 Date',
                             comment='The date that the L2 was most recently updated'),
                      Column('L3_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 3',
                             comment='The L3 Price'),
                      Column('L3_Date',
                             Date,
                             nullable=True,
                             doc='L3 Date',
                             comment='The date that L3 was most recently updated'),
                      Column('L4_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 4',
                             comment='The L4 Price'),
                      Column('L4_Date',
                             Date,
                             nullable=True,
                             doc='L4 Date',
                             comment='The date that L4 was last updated'),
                      Column('Fut_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Future Price',
                             comment='The future price of cost for the product. This field should be paired with the'
                                     'future price column field to indicate which cost or price field the value'
                                     'applies to.'),
                      Column('Fut_Price_Column',
                             String(length=3),
                             nullable=True,
                             doc='Future Price Column',
                             comment='The price or cost column of the future price.'),
                      Column('Fut_Price_Date',
                             Date,
                             nullable=True,
                             doc='Future Price Date',
                             comment='The date that the future cost or price will become effective.'),
                      Column('Int_Notes_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes Flat',
                             comment='The internal notes of the product flattened into a single value.'),
                      Column('Primary_Vend',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Primary Vendor',
                             comment='Primary Vendor ID'),
                      Column('Primary_Vend_AP',
                             String(length=9),
                             nullable=True,
                             doc='Primary Vendor (AP)',
                             comment='The Primary Vendor used for purchasing & A.P.'),
                      Column('Primary_Vend_BI',
                             String(length=9),
                             nullable=True,
                             doc='Primary Vendor (BI)',
                             comment='The Primary Vendor found in Pivot Views'),
                      Column('Primary_Vend_Part_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Primary Vendor Part Number',
                             comment='Primary Vendor Part Number'),
                      Column('Fast_Prod',
                             String(length=9),
                             nullable=True,
                             doc='Fast Product',
                             comment='This Y/N field indicates if the product was added as a fast product.'),
                      Column('Rank',
                             String(length=7),
                             nullable=True,
                             doc='Rank',
                             comment='The product"s overall rank. For Rank by Warehouse, use 01.RANK, 02.RANK, etc.'
                                     'fields.'),
                      Column('Rank_Pct',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rank Pct',
                             comment='The percent of the total number of sales orders that the product appears on.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_main_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_main_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Status',
                             String(length=2),
                             nullable=True,
                             doc='Status',
                             comment='The Special Status of the Product Blank or A = Active, N = Non-Stock, D ='
                                     'Disconnected, I = Inactive, C = Consumable'),
                      Column('Entered_By',
                             String(length=6),
                             nullable=True,
                             doc='Entered By',
                             comment='The system initials of the user who created the product'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date that the product file was created'),
                      Column('Desc_Full',
                             LONGTEXT,
                             nullable=True,
                             doc='Description Full',
                             comment='The complete product description'),
                      Column('Quote_Desc_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Quote Description Flat',
                             comment='The Product Quote description flattened into a single value.'),
                      Column('Catalog_Desc',
                             String(length=30),
                             nullable=True,
                             doc='Catalog Description',
                             comment='The catalog description for the product.'),
                      Column('Prod_Line',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Product Line Code',
                             comment='The Product Line Code'),
                      Column('Price_Group_Code',
                             String(length=11),
                             nullable=True,
                             index=True,
                             doc='Price Group Code',
                             comment='The reference code for the product"s price group. For more information, link to'
                                     'the Price Group file.'),
                      Column('Buy_Line_Code',
                             String(length=10),
                             nullable=True,
                             index=True,
                             doc='Buy Line Code',
                             comment='The reference code for the product"s Buy Line. For more Buy Line information,'
                                     'link to the Buy Line file.'),
                      Column('Consignment_Vend_Num',
                             String(length=10),
                             nullable=True,
                             doc='Consignment Vendor Number',
                             comment='The Vendor Number for the product"s consignment vendor.'),
                      Column('HazMat_Code',
                             String(length=8),
                             nullable=True,
                             doc='HazMat Code',
                             comment='The Haz Mat code for the product.'),
                      Column('Mfg_No',
                             String(length=255),
                             nullable=True,
                             doc='Manufacturer No',
                             comment='The default manufacturer"s number'),
                      Column('UPC',
                             String(length=12),
                             nullable=True,
                             index=True,
                             doc='UPC',
                             comment='The UPC Code for the product'),
                      Column('UPC_14',
                             String(length=30),
                             nullable=True,
                             index=True,
                             doc='UPC (14)',
                             comment='The UPC code limited to a column 12 characters wide'),
                      Column('Pricing_Srvc_Num',
                             String(length=30),
                             nullable=True,
                             doc='Pricing Service Number',
                             comment='The Pricing Service Number for the product'),
                      Column('Display_UOM',
                             String(length=3),
                             nullable=True,
                             doc='Display UOM',
                             comment='The display or default selling Unit of Measure'),
                      Column('UOM_Qty_Factor',
                             Integer,
                             nullable=True,
                             doc='UOM Qty Factor',
                             comment='The Unit of Measure factor for the default Selling Unit of Measure.'),
                      Column('Price_UOM',
                             String(length=9),
                             nullable=True,
                             doc='Price UOM',
                             comment='The default Pricing Unit of Measure'),
                      Column('UOM_Price_Factor',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='UOM Price Factor',
                             comment='The quantity factor between the Price UOM and the display UOM'),
                      Column('Purch_UOM',
                             String(length=12),
                             nullable=True,
                             doc='Purchase UOM',
                             comment='The default Purchasing Unit of Measure'),
                      Column('UOM_Purch_Qty_Factor',
                             Integer,
                             nullable=True,
                             doc='UOM Purchase Qty Factor',
                             comment='The Unit of Measure factor for the default purchasing Unit of Measure'),
                      Column('UOM_Units',
                             Integer,
                             nullable=True,
                             doc='UOM Units',
                             comment='The total number of units of measure on the product'),
                      Column('C1_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C1 Cost',
                             comment='The current C1 Standard Cost for the product. C1 is a user-maintained field,'
                                     'typically representing the replacement cost or product base cost. C1 may be'
                                     'calculated by a price rollup formula and may be changed by hand entry, m'),
                      Column('C1_Date',
                             Date,
                             nullable=True,
                             doc='C1 Date',
                             comment='the date that the C1 Cost field was last changed'),
                      Column('C2_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C2 Cost',
                             comment='The current C2 Weighted Average cost for the product. C2 is calculated by stock'
                                     'receiving. Weighted average cost is based on the value of existing inventory,'
                                     'plus the value of newly received inventory, divided by the total qu'),
                      Column('C2_Date',
                             Date,
                             nullable=True,
                             doc='C2 Date',
                             comment='The date that the C2 Cost field was last changed.'),
                      Column('C3_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C3 Cost',
                             comment='The current C3 Landed cost for the product. C3 includes all freight costs from'
                                     'the stock receipt or account payable invoice, and is calculated by stock'
                                     'receiving or accounts payable entry. Landed weighted average cost is base'),
                      Column('C3_Date',
                             Date,
                             nullable=True,
                             doc='C3 Date',
                             comment='The date that the C3 Cost field was last changed.'),
                      Column('C4_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C4 Cost',
                             comment='The current C4 Cost for the product. C4 is a user-maintained field, typically'
                                     'representing the loaded salespersons cost other formula derived cost. C4 may be'
                                     'calculated by a Price Rollup formula, and may be edited by hand ent'),
                      Column('C4_Date',
                             Date,
                             nullable=True,
                             doc='C4 Date',
                             comment='The most recent date that the C4 Cost was changed'),
                      Column('C5_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C5 Cost',
                             comment='The current C5 last Purchase Order Cost for the product. C5 is a system'
                                     'calculated cost derived from the purchase order / stock receiving cost. It is'
                                     'updated from Stock Receipts at the time of purchase order receiving. C5 cos'),
                      Column('C5_Date',
                             Date,
                             nullable=True,
                             doc='C5 Date',
                             comment='The date of the most recent purchase order.'),
                      Column('C6_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C6 Cost',
                             comment='The current C6 Cost for the product. C6 is a user-maintained field, typically'
                                     'derived from a formula based on C1, C2, or C5. C6 can be calculated by a Price'
                                     'Rollup formula, and may be edited by hand entry or mass change.'),
                      Column('C6_Date',
                             Date,
                             nullable=True,
                             doc='C6 Date',
                             comment='The most recent date that the C6 Cost was changed'),
                      Column('C7_Cost',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='C7 Cost',
                             comment='The current C7 Cost for the product. C7 is a user-maintained field, typically'
                                     'derived from a formula based on C1, C2, or C5. C7 may be calculated by a Price'
                                     'Rollup formula and may be edited by hand entry or mass change.'),
                      Column('C7_Date',
                             Date,
                             nullable=True,
                             doc='C7 Date',
                             comment='The most recent date that the C7 Cost was changed'),
                      Column('L1_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 1',
                             comment='The L1 List Price'),
                      Column('L1_Date',
                             Date,
                             nullable=True,
                             doc='L1 Date',
                             comment='The date that the L1 List price field was last changed'),
                      Column('L2_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 2',
                             comment='The L2 Price'),
                      Column('L2_Date',
                             Date,
                             nullable=True,
                             doc='L2 Date',
                             comment='The date that the L2 was most recently updated'),
                      Column('L3_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 3',
                             comment='The L3 Price'),
                      Column('L3_Date',
                             Date,
                             nullable=True,
                             doc='L3 Date',
                             comment='The date that L3 was most recently updated'),
                      Column('L4_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='List 4',
                             comment='The L4 Price'),
                      Column('L4_Date',
                             Date,
                             nullable=True,
                             doc='L4 Date',
                             comment='The date that L4 was last updated'),
                      Column('Fut_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Future Price',
                             comment='The future price of cost for the product. This field should be paired with the'
                                     'future price column field to indicate which cost or price field the value'
                                     'applies to.'),
                      Column('Fut_Price_Column',
                             String(length=3),
                             nullable=True,
                             doc='Future Price Column',
                             comment='The price or cost column of the future price.'),
                      Column('Fut_Price_Date',
                             Date,
                             nullable=True,
                             doc='Future Price Date',
                             comment='The date that the future cost or price will become effective.'),
                      Column('Int_Notes_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes Flat',
                             comment='The internal notes of the product flattened into a single value.'),
                      Column('Primary_Vend',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Primary Vendor',
                             comment='Primary Vendor ID'),
                      Column('Primary_Vend_AP',
                             String(length=9),
                             nullable=True,
                             doc='Primary Vendor (AP)',
                             comment='The Primary Vendor used for purchasing & A.P.'),
                      Column('Primary_Vend_BI',
                             String(length=9),
                             nullable=True,
                             doc='Primary Vendor (BI)',
                             comment='The Primary Vendor found in Pivot Views'),
                      Column('Primary_Vend_Part_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Primary Vendor Part Number',
                             comment='Primary Vendor Part Number'),
                      Column('Fast_Prod',
                             String(length=9),
                             nullable=True,
                             doc='Fast Product',
                             comment='This Y/N field indicates if the product was added as a fast product.'),
                      Column('Rank',
                             String(length=7),
                             nullable=True,
                             doc='Rank',
                             comment='The product"s overall rank. For Rank by Warehouse, use 01.RANK, 02.RANK, etc.'
                                     'fields.'),
                      Column('Rank_Pct',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rank Pct',
                             comment='The percent of the total number of sales orders that the product appears on.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_option_01_current(server_utils.mysql_base):
    __table__ = Table('prod_option_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Option_ID',
                             String(length=6),
                             nullable=True,
                             doc='Option ID',
                             comment='The option code for the product option. This field may have multiple values for'
                                     'a single product number if the item has multiple options and accessories.'),
                      Column('Prod_Options_Desc',
                             String(length=30),
                             nullable=True,
                             doc='Product Options Description',
                             comment='The Product Options Description'),
                      Column('Option_Auto_Add_SO',
                             String(length=19),
                             nullable=True,
                             doc='Option Auto Add S/O',
                             comment='Product Option to Auto Add to a Sales Order'),
                      schema='product')


# noinspection PyPep8Naming
class prod_option_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_option_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Option_ID',
                             String(length=6),
                             nullable=True,
                             doc='Option ID',
                             comment='The option code for the product option. This field may have multiple values for'
                                     'a single product number if the item has multiple options and accessories.'),
                      Column('Prod_Options_Desc',
                             String(length=30),
                             nullable=True,
                             doc='Product Options Description',
                             comment='The Product Options Description'),
                      Column('Option_Auto_Add_SO',
                             String(length=19),
                             nullable=True,
                             doc='Option Auto Add S/O',
                             comment='Product Option to Auto Add to a Sales Order'),
                      schema='product')


# noinspection PyPep8Naming
class prod_purch_01_current(server_utils.mysql_base):
    __table__ = Table('prod_purch_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Seasonal',
                             String(length=8),
                             nullable=True,
                             doc='Seasonal',
                             comment='This Y/N field indicates if the Seasonal box is checked. Seasonal items use the'
                                     'upcoming three months of demand when projecting order quantities.'),
                      Column('Purch_History_Link_Prod',
                             String(length=20),
                             nullable=True,
                             doc='Purchase History Link Product',
                             comment='The product ID that is linked for purchase history. Projected Purchase order'
                                     'adds the demand from this superseded item to the parent.'),
                      Column('Weight',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Weight',
                             comment='The product weight, generally entered in pounds.'),
                      Column('Volume',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Volume',
                             comment='Cubic Volume'),
                      Column('Length',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Length',
                             comment='The product"s length value'),
                      Column('Width',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Width',
                             comment='The product"s width value.'),
                      Column('Height',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Height',
                             comment='The product"s height value'),
                      Column('Box_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Box Qty',
                             comment='The box quantity for the product'),
                      Column('Carton_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Carton Quantity',
                             comment='The Carton Quantity for the product.'),
                      Column('Pallet_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Pallet Quantity',
                             comment='The pallet quantity for the product, as set on the purchasing tab.'),
                      Column('Pallet_Layer',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Pallet Layer',
                             comment='The pallet layer for the product, as set on the purchasing tab.'),
                      Column('Min_PO_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Minimum PO Quantity',
                             comment='The minimum Purchase Order quantity'),
                      Column('Min_Stock_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Minimum Stock Qty',
                             comment='The Minimum Stock Quantity. Usually blank, unless a user override to the'
                                     'automatically calculated minimum, (reorder point, as viewed in the Product'
                                     'Analysis) is entered in this field.'),
                      Column('Max_Stock_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Maximum Stock Quantity',
                             comment='The maximum stock quantity. Generally not used. The purchasing system projects'
                                     'a maximum based on lead time, demand, and desired inventory turns for the'
                                     'vendor.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_purch_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_purch_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Seasonal',
                             String(length=8),
                             nullable=True,
                             doc='Seasonal',
                             comment='This Y/N field indicates if the Seasonal box is checked. Seasonal items use the'
                                     'upcoming three months of demand when projecting order quantities.'),
                      Column('Purch_History_Link_Prod',
                             String(length=20),
                             nullable=True,
                             doc='Purchase History Link Product',
                             comment='The product ID that is linked for purchase history. Projected Purchase order'
                                     'adds the demand from this superseded item to the parent.'),
                      Column('Weight',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Weight',
                             comment='The product weight, generally entered in pounds.'),
                      Column('Volume',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Volume',
                             comment='Cubic Volume'),
                      Column('Length',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Length',
                             comment='The product"s length value'),
                      Column('Width',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Width',
                             comment='The product"s width value.'),
                      Column('Height',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Height',
                             comment='The product"s height value'),
                      Column('Box_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Box Qty',
                             comment='The box quantity for the product'),
                      Column('Carton_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Carton Quantity',
                             comment='The Carton Quantity for the product.'),
                      Column('Pallet_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Pallet Quantity',
                             comment='The pallet quantity for the product, as set on the purchasing tab.'),
                      Column('Pallet_Layer',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Pallet Layer',
                             comment='The pallet layer for the product, as set on the purchasing tab.'),
                      Column('Min_PO_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Minimum PO Quantity',
                             comment='The minimum Purchase Order quantity'),
                      Column('Min_Stock_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Minimum Stock Qty',
                             comment='The Minimum Stock Quantity. Usually blank, unless a user override to the'
                                     'automatically calculated minimum, (reorder point, as viewed in the Product'
                                     'Analysis) is entered in this field.'),
                      Column('Max_Stock_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Maximum Stock Quantity',
                             comment='The maximum stock quantity. Generally not used. The purchasing system projects'
                                     'a maximum based on lead time, demand, and desired inventory turns for the'
                                     'vendor.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_replenishments_01_current(server_utils.mysql_base):
    __table__ = Table('prod_replenishments_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Whse_Num',
                             Integer,
                             nullable=True,
                             doc='Whse',
                             comment='The two digit reference code for the warehouse that the information pertains'
                                     'to. Use this field in conjunction with fields such as Avail, On PO, COMM, etc.'
                                     'that present data pertaining to multiple warehouses'),
                      Column('AWR_Whse',
                             String(length=14),
                             nullable=True,
                             doc='AWR Whse',
                             comment='This field indicates which warehouse the product is set to be replenished from'),
                      Column('AWR_Min',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AWR Min',
                             comment='The minimum number of weeks that should be replenished from one warehouse to'
                                     'another for the product.'),
                      Column('AWR_Max',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AWR Max',
                             comment='The maximum number of weeks that should be replenished from one warehouse to'
                                     'another for the product.'),
                      Column('AWR_Break_Case',
                             String(length=15),
                             nullable=True,
                             doc='AWR Break Case',
                             comment='This Y/N field indicates if the product is designated to break cases when'
                                     'transferring between warehouses in a warehouse replenishment setup'),
                      schema='product')


# noinspection PyPep8Naming
class prod_replenishments_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_replenishments_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Whse_Num',
                             Integer,
                             nullable=True,
                             doc='Whse',
                             comment='The two digit reference code for the warehouse that the information pertains'
                                     'to. Use this field in conjunction with fields such as Avail, On PO, COMM, etc.'
                                     'that present data pertaining to multiple warehouses'),
                      Column('AWR_Whse',
                             String(length=14),
                             nullable=True,
                             doc='AWR Whse',
                             comment='This field indicates which warehouse the product is set to be replenished from'),
                      Column('AWR_Min',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AWR Min',
                             comment='The minimum number of weeks that should be replenished from one warehouse to'
                                     'another for the product.'),
                      Column('AWR_Max',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='AWR Max',
                             comment='The maximum number of weeks that should be replenished from one warehouse to'
                                     'another for the product.'),
                      Column('AWR_Break_Case',
                             String(length=15),
                             nullable=True,
                             doc='AWR Break Case',
                             comment='This Y/N field indicates if the product is designated to break cases when'
                                     'transferring between warehouses in a warehouse replenishment setup'),
                      schema='product')


# noinspection PyPep8Naming
class prod_rollup_01_current(server_utils.mysql_base):
    __table__ = Table('prod_rollup_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Rollup_C1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C1',
                             comment='Lists all historical rollup values for C1. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_C4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C4',
                             comment='Lists all historical rollup values for C4. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_C6',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C6',
                             comment='Lists all historical rollup values for C6. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_C7',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C7',
                             comment='Lists all historical rollup values for C7. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L1',
                             comment='Lists all historical rollup values for L1. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L2',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L2',
                             comment='Lists all historical rollup values for L2. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L3',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L3',
                             comment='Lists all historical rollup values for L3. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L4',
                             comment='Lists all historical rollup values for L4. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_Date',
                             Date,
                             nullable=True,
                             doc='Rollup Date',
                             comment='The date that the rollup change occurred.'),
                      Column('Rollup_Seq_1',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 1',
                             comment='The first sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_2',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 2',
                             comment='The second sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_3',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 3',
                             comment='The third sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_4',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 4',
                             comment='The fourth sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_5',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 5',
                             comment='The fifth sequence of an item"s Price Rollup Schedule'),
                      schema='product')


# noinspection PyPep8Naming
class prod_rollup_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_rollup_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Rollup_C1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C1',
                             comment='Lists all historical rollup values for C1. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_C4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C4',
                             comment='Lists all historical rollup values for C4. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_C6',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C6',
                             comment='Lists all historical rollup values for C6. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_C7',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup C7',
                             comment='Lists all historical rollup values for C7. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L1',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L1',
                             comment='Lists all historical rollup values for L1. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L2',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L2',
                             comment='Lists all historical rollup values for L2. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L3',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L3',
                             comment='Lists all historical rollup values for L3. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_L4',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Rollup L4',
                             comment='Lists all historical rollup values for L4. This is the total amount of the'
                                     'field after the rollup, no the formula. Pair this field with the ROLLUP.Date'
                                     'field.'),
                      Column('Rollup_Date',
                             Date,
                             nullable=True,
                             doc='Rollup Date',
                             comment='The date that the rollup change occurred.'),
                      Column('Rollup_Seq_1',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 1',
                             comment='The first sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_2',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 2',
                             comment='The second sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_3',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 3',
                             comment='The third sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_4',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 4',
                             comment='The fourth sequence of an item"s Price Rollup Schedule'),
                      Column('Rollup_Seq_5',
                             String(length=20),
                             nullable=True,
                             doc='Rollup Sequence 5',
                             comment='The fifth sequence of an item"s Price Rollup Schedule'),
                      schema='product')


# noinspection PyPep8Naming
class prod_so_ext_cmnts_01_current(server_utils.mysql_base):
    __table__ = Table('prod_so_ext_cmnts_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('SO_Ext_Comments',
                             String(length=30),
                             nullable=True,
                             doc='S/O External Comments',
                             comment='Sales Order External Comments'),
                      schema='product')


# noinspection PyPep8Naming
class prod_so_ext_cmnts_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_so_ext_cmnts_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('SO_Ext_Comments',
                             String(length=30),
                             nullable=True,
                             doc='S/O External Comments',
                             comment='Sales Order External Comments'),
                      schema='product')


# noinspection PyPep8Naming
class prod_stats_01_current(server_utils.mysql_base):
    __table__ = Table('prod_stats_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Open_Trans',
                             String(length=18),
                             nullable=True,
                             doc='Open Transaction',
                             comment='A Y/N field that indicates if a product is currently on an open transaction'
                                     '(Sales Order, Price Quote, Purchase Order, Request for Quote, Work Order, or'
                                     'Stock Transfer) in any warehouse.'),
                      Column('Total_On_Hand',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='OnHand',
                             comment='The sum total On-Hand quantity of the product for all warehouses, in the'
                                     'default unit of measure.'),
                      Column('Total_Committed',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Committed',
                             comment='The sum total committed quantity in all warehouses in the display/default unit'
                                     'of measure. Sales order line items with the "Commit Inventory" field (under the'
                                     'Item Details tab) unchecked are not included in this Committed num'),
                      Column('Total_Avail',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Available',
                             comment='The total quantity available in all warehouses, calculated as inventory On Hand'
                                     'minus inventory Committed to Sales Orders'),
                      Column('Total_On_PO',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='On PO',
                             comment='The quantity of the product that has currently been ordered from a vendor, but'
                                     'has not yet been received.'),
                      Column('Total_Staged_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Staged Qty',
                             comment='The current quantity staged.'),
                      Column('Total_On_SO',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Total on SO',
                             comment='The total on Sales Orders (including uncommitted)'),
                      Column('Total_On_Transfer',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='On Transfer',
                             comment='The quantity of the product that is currently on open stock transfer(s)'),
                      Column('Total_Hits',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Hits',
                             comment='The total number of hits in the past 12 months for the product in all'
                                     'warehouses.'),
                      Column('Months_Units_Sold_12',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Units Sold',
                             comment='The number of units sold in the past 12 months'),
                      Column('Last_Sold_Date',
                             Date,
                             nullable=True,
                             doc='Last Sold Date',
                             comment='The date of the most recent sale'),
                      Column('Days_Since_Last_Sale',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Sale',
                             comment='The number of days since the product was last sold. This field is calculated by'
                                     'comparing the Last Sold Date with the current date'),
                      Column('Last_Rcved_Date',
                             Date,
                             nullable=True,
                             doc='Last Received Date',
                             comment='The date of the most recent receiving'),
                      Column('Days_Since_Last_Rcpt',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Receipt',
                             comment='The number of days since the product was last received. This field is'
                                     'calculated by comparing the Last Sold Date with the current date.'),
                      Column('Last_Vend_Num',
                             String(length=11),
                             nullable=True,
                             doc='Last Vendor Number',
                             comment='The reference code of the vendor that the product was most recently purchased'
                                     'from'),
                      Column('Import_Date',
                             Date,
                             nullable=True,
                             doc='Import Date',
                             comment='The date of the most recent product import that updated the product'),
                      Column('Mon_1_Units',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Mon 1 Units',
                             comment='The number of units sold in the month 1s.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_stats_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_stats_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Open_Trans',
                             String(length=18),
                             nullable=True,
                             doc='Open Transaction',
                             comment='A Y/N field that indicates if a product is currently on an open transaction'
                                     '(Sales Order, Price Quote, Purchase Order, Request for Quote, Work Order, or'
                                     'Stock Transfer) in any warehouse.'),
                      Column('Total_On_Hand',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='OnHand',
                             comment='The sum total On-Hand quantity of the product for all warehouses, in the'
                                     'default unit of measure.'),
                      Column('Total_Committed',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Committed',
                             comment='The sum total committed quantity in all warehouses in the display/default unit'
                                     'of measure. Sales order line items with the "Commit Inventory" field (under the'
                                     'Item Details tab) unchecked are not included in this Committed num'),
                      Column('Total_Avail',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Available',
                             comment='The total quantity available in all warehouses, calculated as inventory On Hand'
                                     'minus inventory Committed to Sales Orders'),
                      Column('Total_On_PO',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='On PO',
                             comment='The quantity of the product that has currently been ordered from a vendor, but'
                                     'has not yet been received.'),
                      Column('Total_Staged_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Staged Qty',
                             comment='The current quantity staged.'),
                      Column('Total_On_SO',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Total on SO',
                             comment='The total on Sales Orders (including uncommitted)'),
                      Column('Total_On_Transfer',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='On Transfer',
                             comment='The quantity of the product that is currently on open stock transfer(s)'),
                      Column('Total_Hits',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Hits',
                             comment='The total number of hits in the past 12 months for the product in all'
                                     'warehouses.'),
                      Column('Months_Units_Sold_12',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Units Sold',
                             comment='The number of units sold in the past 12 months'),
                      Column('Last_Sold_Date',
                             Date,
                             nullable=True,
                             doc='Last Sold Date',
                             comment='The date of the most recent sale'),
                      Column('Days_Since_Last_Sale',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Sale',
                             comment='The number of days since the product was last sold. This field is calculated by'
                                     'comparing the Last Sold Date with the current date'),
                      Column('Last_Rcved_Date',
                             Date,
                             nullable=True,
                             doc='Last Received Date',
                             comment='The date of the most recent receiving'),
                      Column('Days_Since_Last_Rcpt',
                             Integer,
                             nullable=True,
                             doc='Days Since Last Receipt',
                             comment='The number of days since the product was last received. This field is'
                                     'calculated by comparing the Last Sold Date with the current date.'),
                      Column('Last_Vend_Num',
                             String(length=11),
                             nullable=True,
                             doc='Last Vendor Number',
                             comment='The reference code of the vendor that the product was most recently purchased'
                                     'from'),
                      Column('Import_Date',
                             Date,
                             nullable=True,
                             doc='Import Date',
                             comment='The date of the most recent product import that updated the product'),
                      Column('Mon_1_Units',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Mon 1 Units',
                             comment='The number of units sold in the month 1s.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_substitute_01_current(server_utils.mysql_base):
    __table__ = Table('prod_substitute_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Substitute_1',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 1',
                             comment='The first substitute item ID'),
                      Column('Substitute_2',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 2',
                             comment='The second substitute item ID'),
                      Column('Substitute_3',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 3',
                             comment='The third substitute Item ID'),
                      Column('Substitute_4',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 4',
                             comment='The fourth substitute item ID'),
                      Column('Substitute_5',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 5',
                             comment='The fifth substitute item ID'),
                      schema='product')


# noinspection PyPep8Naming
class prod_substitute_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_substitute_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Substitute_1',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 1',
                             comment='The first substitute item ID'),
                      Column('Substitute_2',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 2',
                             comment='The second substitute item ID'),
                      Column('Substitute_3',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 3',
                             comment='The third substitute Item ID'),
                      Column('Substitute_4',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 4',
                             comment='The fourth substitute item ID'),
                      Column('Substitute_5',
                             String(length=15),
                             nullable=True,
                             doc='Substitute 5',
                             comment='The fifth substitute item ID'),
                      schema='product')


# noinspection PyPep8Naming
class prod_uom_v2_01_current(server_utils.mysql_base):
    __table__ = Table('prod_uom_v2_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('UOM',
                             String(length=5),
                             nullable=True,
                             doc='Units of Measure',
                             comment='Lists multiple units of measure, if more than one UOM exists'),
                      Column('UOM_Qty',
                             Numeric(precision=60, scale=30),
                             nullable=True,
                             doc='UOM Quantity',
                             comment='The quantity for each unit of measure set up'),
                      Column('Base_UOM_Factor',
                             String(length=5),
                             nullable=True,
                             doc='Base_UOM_Factor',
                             comment='N/A'),
                      Column('Base_UOM_Qty',
                             Numeric(precision=60, scale=30),
                             nullable=True,
                             doc='Base_UOM_Qty',
                             comment='N/A'),
                      Column('UOM_Factor_Desc',
                             String(length=21),
                             nullable=True,
                             doc='UOM Factor Description',
                             comment='This combines the Quantity and Of UOM fields into one, making it possible to'
                                     'view breakdown of the factor quantities.'),
                      Column('UOM_Pricing_UOM',
                             String(length=16),
                             nullable=True,
                             doc='Pricing UOM',
                             comment='The default pricing unit of measure for the product'),
                      Column('UOM_Markup',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Units Markup',
                             comment='The Markup % for each unit of measure'),
                      Column('UOM_UPC_Code',
                             String(length=255),
                             nullable=True,
                             doc='UOM UPC Code',
                             comment='The UPC code for each unit of measure'),
                      Column('UOM_Disable_Sales',
                             String(length=19),
                             nullable=True,
                             doc='UOM Disable Sales',
                             comment='This Y/N field indicates if the Disable Sales box is checked for the Unit of'
                                     'Measure. Checking this box prevents the Unit of Measure from displaying in the'
                                     'Sales Order screen'),
                      schema='product')

    @hybrid_property
    def Of_UOM(self):
        str_rep = str(self.__table__.c.UOM_Factor_Desc)
        if str_rep == "1":
            return self.__table__.c.UOM
        else:
            str_split = str_rep.split()
            str_split_len = len(str_split)
            return str_split[str_split_len - 1].strip()
    
    # noinspection PyMethodParameters
    @Of_UOM.expression
    def Of_UOM(cls):
        return func.IF(cls.__table__.c.UOM_Factor_Desc == "1",
                       cls.__table__.c.UOM,
                       func.substring_index(cls.__table__.c.UOM_Factor_Desc, " ", -1))


# noinspection PyPep8Naming
class prod_uom_v2_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_uom_v2_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('UOM',
                             String(length=5),
                             nullable=True,
                             doc='Units of Measure',
                             comment='Lists multiple units of measure, if more than one UOM exists'),
                      Column('UOM_Qty',
                             Numeric(precision=60, scale=30),
                             nullable=True,
                             doc='UOM Quantity',
                             comment='The quantity for each unit of measure set up'),
                      Column('Base_UOM_Factor',
                             String(length=5),
                             nullable=True,
                             doc='Base_UOM_Factor',
                             comment='N/A'),
                      Column('Base_UOM_Qty',
                             Numeric(precision=60, scale=30),
                             nullable=True,
                             doc='Base_UOM_Qty',
                             comment='N/A'),
                      Column('UOM_Factor_Desc',
                             String(length=21),
                             nullable=True,
                             doc='UOM Factor Description',
                             comment='This combines the Quantity and Of UOM fields into one, making it possible to'
                                     'view breakdown of the factor quantities.'),
                      Column('UOM_Pricing_UOM',
                             String(length=16),
                             nullable=True,
                             doc='Pricing UOM',
                             comment='The default pricing unit of measure for the product'),
                      Column('UOM_Markup',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Units Markup',
                             comment='The Markup % for each unit of measure'),
                      Column('UOM_UPC_Code',
                             String(length=255),
                             nullable=True,
                             doc='UOM UPC Code',
                             comment='The UPC code for each unit of measure'),
                      Column('UOM_Disable_Sales',
                             String(length=19),
                             nullable=True,
                             doc='UOM Disable Sales',
                             comment='This Y/N field indicates if the Disable Sales box is checked for the Unit of'
                                     'Measure. Checking this box prevents the Unit of Measure from displaying in the'
                                     'Sales Order screen'),
                      schema='product')

    @hybrid_property
    def Of_UOM(self):
        str_rep = str(self.__table__.c.UOM_Factor_Desc)
        if str_rep == "1":
            return self.__table__.c.UOM
        else:
            str_split = str_rep.split()
            str_split_len = len(str_split)
            return str_split[str_split_len - 1].strip()
    
    # noinspection PyMethodParameters
    @Of_UOM.expression
    def Of_UOM(cls):
        return func.IF(cls.__table__.c.UOM_Factor_Desc == "1",
                       cls.__table__.c.UOM,
                       func.substring_index(cls.__table__.c.UOM_Factor_Desc, " ", -1))


# noinspection PyPep8Naming
class prod_vend_01_current(server_utils.mysql_base):
    __table__ = Table('prod_vend_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor ID',
                             comment='All of the linked vendors for the product'),
                      Column('Vend_Part_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Vendor Part Number',
                             comment='The Vendor Part Number for the product'),
                      Column('Vends_Prod_Desc',
                             String(length=30),
                             nullable=True,
                             doc='Vendors Product Description',
                             comment='The vendor-specific description for the product'),
                      Column('Vend_UPC_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Vendor UPC Number',
                             comment='The UPC Code of the product for the vendor.'),
                      Column('Vend_Last_PO_Num',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Last PO Number (Whse)',
                             comment='The most recent PO Number(s) that the product was purchased form the vendor(s).'
                                     'The last warehouse to receive is the warehouse shown. Consider using "Vendor'
                                     'Last PO Number" to see a PO Number for each warehouse.'),
                      Column('Vend_Last_PO_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Vendor Last PO Qty (Whse)',
                             comment='The most recent Qtys(s) that the product was purchased from the vendor(s). The'
                                     'last warehouse to receive is the warehouse shown. Consider using "Vendor Last'
                                     'PO Qty" to see a qty for each warehouse.'),
                      Column('Vend_Last_PO_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Vendor Last PO Price (Whse)',
                             comment='The most recent price(s) that the product was purchased from the vendor(s). The'
                                     'last warehouse to receive is the warehouse shown. Consider using "vendor Last'
                                     'PO Price" to see a price for each warehouse.'),
                      Column('Vend_Last_PO_Date',
                             Date,
                             nullable=True,
                             doc='Vendor Last PO Date (Whse)',
                             comment='The most recent date(s) that the product was purchased from the vendor(s). The'
                                     'last warehouse to receive is the warehouse shown. Consider using "Vendor Last'
                                     'P/O Date" to see a date for each warehouse.'),
                      Column('Vend_PO_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Vendor Purchase Order Price',
                             comment='The current Purchase Price for the vendor'),
                      schema='product')


# noinspection PyPep8Naming
class prod_vend_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_vend_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             index=True,
                             doc='Vendor ID',
                             comment='All of the linked vendors for the product'),
                      Column('Vend_Part_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Vendor Part Number',
                             comment='The Vendor Part Number for the product'),
                      Column('Vends_Prod_Desc',
                             String(length=30),
                             nullable=True,
                             doc='Vendors Product Description',
                             comment='The vendor-specific description for the product'),
                      Column('Vend_UPC_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Vendor UPC Number',
                             comment='The UPC Code of the product for the vendor.'),
                      Column('Vend_Last_PO_Num',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Last PO Number (Whse)',
                             comment='The most recent PO Number(s) that the product was purchased form the vendor(s).'
                                     'The last warehouse to receive is the warehouse shown. Consider using "Vendor'
                                     'Last PO Number" to see a PO Number for each warehouse.'),
                      Column('Vend_Last_PO_Qty',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Vendor Last PO Qty (Whse)',
                             comment='The most recent Qtys(s) that the product was purchased from the vendor(s). The'
                                     'last warehouse to receive is the warehouse shown. Consider using "Vendor Last'
                                     'PO Qty" to see a qty for each warehouse.'),
                      Column('Vend_Last_PO_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Vendor Last PO Price (Whse)',
                             comment='The most recent price(s) that the product was purchased from the vendor(s). The'
                                     'last warehouse to receive is the warehouse shown. Consider using "vendor Last'
                                     'PO Price" to see a price for each warehouse.'),
                      Column('Vend_Last_PO_Date',
                             Date,
                             nullable=True,
                             doc='Vendor Last PO Date (Whse)',
                             comment='The most recent date(s) that the product was purchased from the vendor(s). The'
                                     'last warehouse to receive is the warehouse shown. Consider using "Vendor Last'
                                     'P/O Date" to see a date for each warehouse.'),
                      Column('Vend_PO_Price',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Vendor Purchase Order Price',
                             comment='The current Purchase Price for the vendor'),
                      schema='product')


# noinspection PyPep8Naming
class prod_whse_proc_01_current(server_utils.mysql_base):
    __table__ = Table('prod_whse_proc_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Whse_Num',
                             Integer,
                             nullable=True,
                             doc='Whse',
                             comment='The two digit reference code for the warehouse that the information pertains'
                                     'to. Use this field in conjunction with fields such as Avail, On PO, COMM, etc.'
                                     'that present data pertaining to multiple warehouses'),
                      Column('Whse_Stocked',
                             String(length=13),
                             nullable=True,
                             doc='Whse Stocked',
                             comment='This Y/N field indicates if the stock box for the warehouse is checked'),
                      Column('Whse_Mins',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Whse Minimums',
                             comment='The minimum stock quantity overrides for each warehouse'),
                      Column('Whse_Maxs',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Whse Maximums',
                             comment='The maximum stock quantity overrides for each warehouse'),
                      Column('Whse_Min_Stock_Qty_Exp_Date',
                             Date,
                             nullable=True,
                             doc='Whse Min Stock Qty Exp Date',
                             comment='The Warehouse minimum stock quantity expiration date.'),
                      Column('Whse_Forecast_Formula',
                             String(length=30),
                             nullable=True,
                             doc='Whse Forecast Formula',
                             comment='The forecast formula assigned to the product for the warehouse'),
                      Column('Whse_Forecast_Freeze',
                             String(length=21),
                             nullable=True,
                             doc='Whse Forecast Freeze',
                             comment='This Y/N indicates if the freeze forecast? Box is checked'),
                      Column('Lead_Times',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Lead Times',
                             comment='The lead time days by warehouse'),
                      Column('Safety_Stock_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Safety Stock Percent',
                             comment='The Safety Stock Percentage. Used to adjust the automatically calculated'
                                     'reorder point, or minimum higher. Defaults to 20% if the field is blank.'),
                      schema='product')


# noinspection PyPep8Naming
class prod_whse_proc_02_archive(server_utils.mysql_base):
    __table__ = Table('prod_whse_proc_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Prod_Num',
                             String(length=25),
                             nullable=True,
                             index=True,
                             doc='Product (25)',
                             comment='The Product Number limited to a column 25 characters wide'),
                      Column('Whse_Num',
                             Integer,
                             nullable=True,
                             doc='Whse',
                             comment='The two digit reference code for the warehouse that the information pertains'
                                     'to. Use this field in conjunction with fields such as Avail, On PO, COMM, etc.'
                                     'that present data pertaining to multiple warehouses'),
                      Column('Whse_Stocked',
                             String(length=13),
                             nullable=True,
                             doc='Whse Stocked',
                             comment='This Y/N field indicates if the stock box for the warehouse is checked'),
                      Column('Whse_Mins',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Whse Minimums',
                             comment='The minimum stock quantity overrides for each warehouse'),
                      Column('Whse_Maxs',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Whse Maximums',
                             comment='The maximum stock quantity overrides for each warehouse'),
                      Column('Whse_Min_Stock_Qty_Exp_Date',
                             Date,
                             nullable=True,
                             doc='Whse Min Stock Qty Exp Date',
                             comment='The Warehouse minimum stock quantity expiration date.'),
                      Column('Whse_Forecast_Formula',
                             String(length=30),
                             nullable=True,
                             doc='Whse Forecast Formula',
                             comment='The forecast formula assigned to the product for the warehouse'),
                      Column('Whse_Forecast_Freeze',
                             String(length=21),
                             nullable=True,
                             doc='Whse Forecast Freeze',
                             comment='This Y/N indicates if the freeze forecast? Box is checked'),
                      Column('Lead_Times',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Lead Times',
                             comment='The lead time days by warehouse'),
                      Column('Safety_Stock_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Safety Stock Percent',
                             comment='The Safety Stock Percentage. Used to adjust the automatically calculated'
                                     'reorder point, or minimum higher. Defaults to 20% if the field is blank.'),
                      schema='product')


# noinspection PyPep8Naming
class shipto_01_static(server_utils.mysql_base):
    __table__ = Table('shipto_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_budget_01_current(server_utils.mysql_base):
    __table__ = Table('shipto_budget_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Yearly_Budget_Amt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Ship To Yearly Budget Amount',
                             comment='The Budget Amount for the Ship To address'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_budget_02_archive(server_utils.mysql_base):
    __table__ = Table('shipto_budget_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Yearly_Budget_Amt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Ship To Yearly Budget Amount',
                             comment='The Budget Amount for the Ship To address'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_cust_01_current(server_utils.mysql_base):
    __table__ = Table('shipto_cust_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('Cust_Name',
                             String(length=255),
                             nullable=True,
                             doc='Customer Name',
                             comment='The customer"s name'),
                      Column('Cust_Address_1',
                             String(length=255),
                             nullable=True,
                             doc='Customer Address Line 1',
                             comment='The first line of the customer"s main address'),
                      Column('Cust_Address_2',
                             String(length=255),
                             nullable=True,
                             doc='Customer Address Line 2',
                             comment='The second line of the Customer"s main address'),
                      Column('Cust_Address_3',
                             String(length=255),
                             nullable=True,
                             doc='Customer Address Line 3',
                             comment='The third line of the customer"s main address'),
                      Column('Cust_City',
                             String(length=20),
                             nullable=True,
                             doc='Customer City',
                             comment='The city of the customer"s main address'),
                      Column('Cust_State',
                             String(length=10),
                             nullable=True,
                             doc='Customer State',
                             comment='The state of the customer"s main address'),
                      Column('Cust_Zip',
                             String(length=20),
                             nullable=True,
                             doc='Customer Zip',
                             comment='The zip code of the customer"s main address'),
                      Column('Cust_Phone',
                             String(length=50),
                             nullable=True,
                             doc='Customer Phone',
                             comment='The phone number of the customer"s main address'),
                      Column('Cust_Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Customer Email Address',
                             comment='The email address of the customer"s main address'),
                      Column('Cust_Fax',
                             String(length=50),
                             nullable=True,
                             doc='Customer Fax',
                             comment='The fax number of the customer"s main address'),
                      Column('Cust_Salesperson',
                             String(length=10),
                             nullable=True,
                             doc='Customer Salesperson',
                             comment='The salesman code of the customer"s main salesman'),
                      Column('Cust_Credit_Status',
                             String(length=10),
                             nullable=True,
                             doc='Customer Credit Status',
                             comment='The customer"s credit status'),
                      Column('Cust_Credit_Manager',
                             String(length=10),
                             nullable=True,
                             doc='Customer Credit Manager',
                             comment='The credit manager for the customer'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_cust_02_archive(server_utils.mysql_base):
    __table__ = Table('shipto_cust_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('Cust_Name',
                             String(length=255),
                             nullable=True,
                             doc='Customer Name',
                             comment='The customer"s name'),
                      Column('Cust_Address_1',
                             String(length=255),
                             nullable=True,
                             doc='Customer Address Line 1',
                             comment='The first line of the customer"s main address'),
                      Column('Cust_Address_2',
                             String(length=255),
                             nullable=True,
                             doc='Customer Address Line 2',
                             comment='The second line of the Customer"s main address'),
                      Column('Cust_Address_3',
                             String(length=255),
                             nullable=True,
                             doc='Customer Address Line 3',
                             comment='The third line of the customer"s main address'),
                      Column('Cust_City',
                             String(length=20),
                             nullable=True,
                             doc='Customer City',
                             comment='The city of the customer"s main address'),
                      Column('Cust_State',
                             String(length=10),
                             nullable=True,
                             doc='Customer State',
                             comment='The state of the customer"s main address'),
                      Column('Cust_Zip',
                             String(length=20),
                             nullable=True,
                             doc='Customer Zip',
                             comment='The zip code of the customer"s main address'),
                      Column('Cust_Phone',
                             String(length=50),
                             nullable=True,
                             doc='Customer Phone',
                             comment='The phone number of the customer"s main address'),
                      Column('Cust_Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Customer Email Address',
                             comment='The email address of the customer"s main address'),
                      Column('Cust_Fax',
                             String(length=50),
                             nullable=True,
                             doc='Customer Fax',
                             comment='The fax number of the customer"s main address'),
                      Column('Cust_Salesperson',
                             String(length=10),
                             nullable=True,
                             doc='Customer Salesperson',
                             comment='The salesman code of the customer"s main salesman'),
                      Column('Cust_Credit_Status',
                             String(length=10),
                             nullable=True,
                             doc='Customer Credit Status',
                             comment='The customer"s credit status'),
                      Column('Cust_Credit_Manager',
                             String(length=10),
                             nullable=True,
                             doc='Customer Credit Manager',
                             comment='The credit manager for the customer'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_edi_01_current(server_utils.mysql_base):
    __table__ = Table('shipto_edi_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_EDI_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Ship To EDI Number',
                             comment='The EDI number of the ship to address'),
                      Column('ShipTo_EDI_ShipTo_Num',
                             String(length=255),
                             nullable=True,
                             doc='Ship To EDI Shipto Number',
                             comment='The EDI Ship To number of the Ship to Address'),
                      Column('ShipTo_EDI_Vend_Num',
                             String(length=255),
                             nullable=True,
                             doc='Ship To EDI Vendor Number',
                             comment='The EDI Vendor Number of the ShipTo address'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_edi_02_archive(server_utils.mysql_base):
    __table__ = Table('shipto_edi_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_EDI_Num',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Ship To EDI Number',
                             comment='The EDI number of the ship to address'),
                      Column('ShipTo_EDI_ShipTo_Num',
                             String(length=255),
                             nullable=True,
                             doc='Ship To EDI Shipto Number',
                             comment='The EDI Ship To number of the Ship to Address'),
                      Column('ShipTo_EDI_Vend_Num',
                             String(length=255),
                             nullable=True,
                             doc='Ship To EDI Vendor Number',
                             comment='The EDI Vendor Number of the ShipTo address'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_main_01_current(server_utils.mysql_base):
    __table__ = Table('shipto_main_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Name',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Name',
                             comment='The name of the Ship To address'),
                      Column('ShipTo_Attn',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Attention',
                             comment='The individual listed in the attention field'),
                      Column('ShipTo_Address_1',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Address Line 1',
                             comment='The first line of the ship to address'),
                      Column('ShipTo_Address_2',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Address Line 2',
                             comment='The second line of the ship to address'),
                      Column('ShipTo_Address_3',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Address Line 3',
                             comment='The third line of the ship to address'),
                      Column('ShipTo_City',
                             String(length=20),
                             nullable=True,
                             doc='Ship To City',
                             comment='The city of the ship to address'),
                      Column('ShipTo_State',
                             String(length=10),
                             nullable=True,
                             doc='Ship To State',
                             comment='The state of the ship to address'),
                      Column('ShipTo_Zip',
                             String(length=20),
                             nullable=True,
                             doc='Ship To Zip',
                             comment='The Zip Code for the Ship To address'),
                      Column('ShipTo_Country',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Country',
                             comment='The country for the ship to address'),
                      Column('ShipTo_Branch',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Branch',
                             comment='The reference code for the Ship To"s default branch. For more information, link'
                                     'the Branch file.'),
                      Column('ShipTo_Salesperson',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Salesperson',
                             comment='The reference code for the salesperson on the ship to.'),
                      Column('ShipTo_Pricing_Cat',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Pricing Category',
                             comment='The category of the ship to address'),
                      Column('ShipTo_Sales_Territory',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Sales Territory',
                             comment='The reference code for the ship to"s territory'),
                      Column('ShipTo_Ship_Via_Code',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Ship Via Code',
                             comment='The reference code for the default ship via on the ship to'),
                      Column('Print_as_Remit_to',
                             String(length=10),
                             nullable=True,
                             doc='Print as Remit-to',
                             comment='Print ship-to address as remit-to'),
                      Column('ShipTo_Contact',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Contact',
                             comment='The primary contact for the ship to address'),
                      Column('ShipTo_Phone_Num',
                             String(length=50),
                             nullable=True,
                             doc='Ship To Phone Number',
                             comment='The phone number for the Ship To address'),
                      Column('ShipTo_Fax_Num',
                             String(length=50),
                             nullable=True,
                             doc='Ship To Fax Number',
                             comment='The fax number for the ship to address'),
                      Column('ShipTo_Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Email Address',
                             comment='The email address for the ship to address'),
                      Column('ShipTo_UPS_Acct',
                             String(length=255),
                             nullable=True,
                             doc='Ship To UPS Account',
                             comment='The UPS Account Number for the Ship To address'),
                      Column('ShipTo_Fedex_Acct',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Fedex Account',
                             comment='The FedEx Account Number for the Ship To address'),
                      Column('ShipTo_Keyword',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Ship To Keyword',
                             comment='The keyword for the Ship To address'),
                      Column('ShipTo_Reward_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Ship To Reward Percent',
                             comment='The Co-Op percent for the ship to address'),
                      Column('Finance_Chrg_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Finance Charge Percent',
                             comment='The percentage of the total invoice that the shipto will be charged if the'
                                     'invoice is not paid in the number of allotted days'),
                      Column('Credit_Limit',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credit Limit',
                             comment='The ShipTo"s Credit Limit'),
                      Column('ShipTo_Tax_Code',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Tax Code',
                             comment='The reference code for the default tax code on the ship to. For more'
                                     'information, link to the TaxCode file'),
                      Column('ShipTo_Taxable',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Taxable',
                             comment='This Y/N field indicates if the Taxable? Box is checked for the ShipTo address'),
                      Column('ShipTo_Tax_Exempt_Num',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Tax Exempt Number',
                             comment='The tax exempt number for the ship to address'),
                      Column('ShipTo_Type',
                             String(length=20),
                             nullable=True,
                             doc='Ship To Type',
                             comment='The default order type for the ship to address'),
                      Column('Yearly_Budget',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Yearly Budget',
                             comment='The field sums the monthly budgets'),
                      Column('Entry_Date',
                             String(length=50),
                             nullable=True,
                             doc='Entry Date',
                             comment='The ship to entry date'),
                      Column('Inactive',
                             String(length=50),
                             nullable=True,
                             doc='Inactive',
                             comment='Is the ship to inactive?'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_main_02_archive(server_utils.mysql_base):
    __table__ = Table('shipto_main_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Name',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Name',
                             comment='The name of the Ship To address'),
                      Column('ShipTo_Attn',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Attention',
                             comment='The individual listed in the attention field'),
                      Column('ShipTo_Address_1',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Address Line 1',
                             comment='The first line of the ship to address'),
                      Column('ShipTo_Address_2',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Address Line 2',
                             comment='The second line of the ship to address'),
                      Column('ShipTo_Address_3',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Address Line 3',
                             comment='The third line of the ship to address'),
                      Column('ShipTo_City',
                             String(length=20),
                             nullable=True,
                             doc='Ship To City',
                             comment='The city of the ship to address'),
                      Column('ShipTo_State',
                             String(length=10),
                             nullable=True,
                             doc='Ship To State',
                             comment='The state of the ship to address'),
                      Column('ShipTo_Zip',
                             String(length=20),
                             nullable=True,
                             doc='Ship To Zip',
                             comment='The Zip Code for the Ship To address'),
                      Column('ShipTo_Country',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Country',
                             comment='The country for the ship to address'),
                      Column('ShipTo_Branch',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Branch',
                             comment='The reference code for the Ship To"s default branch. For more information, link'
                                     'the Branch file.'),
                      Column('ShipTo_Salesperson',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Salesperson',
                             comment='The reference code for the salesperson on the ship to.'),
                      Column('ShipTo_Pricing_Cat',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Pricing Category',
                             comment='The category of the ship to address'),
                      Column('ShipTo_Sales_Territory',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Sales Territory',
                             comment='The reference code for the ship to"s territory'),
                      Column('ShipTo_Ship_Via_Code',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Ship Via Code',
                             comment='The reference code for the default ship via on the ship to'),
                      Column('Print_as_Remit_to',
                             String(length=10),
                             nullable=True,
                             doc='Print as Remit-to',
                             comment='Print ship-to address as remit-to'),
                      Column('ShipTo_Contact',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Contact',
                             comment='The primary contact for the ship to address'),
                      Column('ShipTo_Phone_Num',
                             String(length=50),
                             nullable=True,
                             doc='Ship To Phone Number',
                             comment='The phone number for the Ship To address'),
                      Column('ShipTo_Fax_Num',
                             String(length=50),
                             nullable=True,
                             doc='Ship To Fax Number',
                             comment='The fax number for the ship to address'),
                      Column('ShipTo_Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Email Address',
                             comment='The email address for the ship to address'),
                      Column('ShipTo_UPS_Acct',
                             String(length=255),
                             nullable=True,
                             doc='Ship To UPS Account',
                             comment='The UPS Account Number for the Ship To address'),
                      Column('ShipTo_Fedex_Acct',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Fedex Account',
                             comment='The FedEx Account Number for the Ship To address'),
                      Column('ShipTo_Keyword',
                             String(length=255),
                             nullable=True,
                             index=True,
                             doc='Ship To Keyword',
                             comment='The keyword for the Ship To address'),
                      Column('ShipTo_Reward_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Ship To Reward Percent',
                             comment='The Co-Op percent for the ship to address'),
                      Column('Finance_Chrg_Pcnt',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Finance Charge Percent',
                             comment='The percentage of the total invoice that the shipto will be charged if the'
                                     'invoice is not paid in the number of allotted days'),
                      Column('Credit_Limit',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Credit Limit',
                             comment='The ShipTo"s Credit Limit'),
                      Column('ShipTo_Tax_Code',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Tax Code',
                             comment='The reference code for the default tax code on the ship to. For more'
                                     'information, link to the TaxCode file'),
                      Column('ShipTo_Taxable',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Taxable',
                             comment='This Y/N field indicates if the Taxable? Box is checked for the ShipTo address'),
                      Column('ShipTo_Tax_Exempt_Num',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Tax Exempt Number',
                             comment='The tax exempt number for the ship to address'),
                      Column('ShipTo_Type',
                             String(length=20),
                             nullable=True,
                             doc='Ship To Type',
                             comment='The default order type for the ship to address'),
                      Column('Yearly_Budget',
                             Numeric(precision=19, scale=4),
                             nullable=True,
                             doc='Yearly Budget',
                             comment='The field sums the monthly budgets'),
                      Column('Entry_Date',
                             String(length=50),
                             nullable=True,
                             doc='Entry Date',
                             comment='The ship to entry date'),
                      Column('Inactive',
                             String(length=50),
                             nullable=True,
                             doc='Inactive',
                             comment='Is the ship to inactive?'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_spec_instr_01_current(server_utils.mysql_base):
    __table__ = Table('shipto_spec_instr_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Special_Instr',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Special Instructions',
                             comment='The special instructions for the ship to address'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_spec_instr_02_archive(server_utils.mysql_base):
    __table__ = Table('shipto_spec_instr_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Special_Instr',
                             String(length=255),
                             nullable=True,
                             doc='Ship To Special Instructions',
                             comment='The special instructions for the ship to address'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_truck_01_current(server_utils.mysql_base):
    __table__ = Table('shipto_truck_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Truck_Route',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Truck Route',
                             comment='The name of the truck on the Ship To"s Truck Route'),
                      Column('ShipTo_Truck_Route_Stop',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Truck Route Stop',
                             comment='The Stop Number for the Ship To"s Truck Route'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class shipto_truck_02_archive(server_utils.mysql_base):
    __table__ = Table('shipto_truck_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Cust_Num',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Customer Number',
                             comment='The customer number'),
                      Column('Ship_To_Code',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='Ship To ID',
                             comment='The reference number for the ship to within the company. These numbers will be'
                                     'duplicated across customers'),
                      Column('ShipTo_Truck_Route',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Truck Route',
                             comment='The name of the truck on the Ship To"s Truck Route'),
                      Column('ShipTo_Truck_Route_Stop',
                             String(length=10),
                             nullable=True,
                             doc='Ship To Truck Route Stop',
                             comment='The Stop Number for the Ship To"s Truck Route'),
                      schema='shipto')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        if self.__table__.c.Cust_Num not in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                return self.__table__.c.Cust_Num + "_" + self.__table__.c.Ship_To_Code
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return self.__table__.c.Cust_Num + "_" + literal("All")
        elif self.__table__.c.Cust_Num in (None, ""):
            if self.__table__.c.Ship_To_Code not in (None, ""):
                raise ValueError
            elif self.__table__.c.Ship_To_Code in (None, ""):
                return None
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return case([
            (and_(cls.__table__.c.Cust_Num.isnot(None), cls.__table__.c.Cust_Num != ""),
             func.IF(and_(cls.__table__.c.Ship_To_Code.isnot(None), cls.__table__.c.Ship_To_Code != ""),
                     func.concat(cls.__table__.c.Cust_Num, literal("_"), cls.__table__.c.Ship_To_Code),
                     func.concat(cls.__table__.c.Cust_Num, literal("_All")))),
            (or_(cls.__table__.c.Cust_Num.is_(None), cls.__table__.c.Cust_Num == ""),
             func.IF(or_(cls.__table__.c.Ship_To_Code.is_(None), cls.__table__.c.Ship_To_Code == ""),
                     literal(""),
                     literal("ERROR")))
        ], else_=literal("ERROR"))


# noinspection PyPep8Naming
class vend_01_static(server_utils.mysql_base):
    __table__ = Table('vend_01_static', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_contact_01_current(server_utils.mysql_base):
    __table__ = Table('vend_contact_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Vend_Contact',
                             Numeric(precision=3, scale=0),
                             nullable=True,
                             doc='Vendor Contact',
                             comment='The Contact Number for each of the vendor"s contacts.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_contact_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_contact_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Vend_Contact',
                             Numeric(precision=3, scale=0),
                             nullable=True,
                             doc='Vendor Contact',
                             comment='The Contact Number for each of the vendor"s contacts.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_general_01_current(server_utils.mysql_base):
    __table__ = Table('vend_general_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Pay_on_Day',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Pay on Day',
                             comment='The Pay on Day for the vendor.'),
                      Column('Cutoff_Day',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Cutoff Day',
                             comment='The Cutoff Day for the vendor.'),
                      Column('Search_Keyword',
                             String(length=255),
                             nullable=True,
                             doc='Search Keyword',
                             comment='The alternate searching keyword for the vendor.'),
                      Column('Tax_ID',
                             String(length=255),
                             nullable=True,
                             doc='Tax ID',
                             comment='The Tax ID Number for the vendor.'),
                      Column('Our_Acct_Num',
                             String(length=255),
                             nullable=True,
                             doc='Our Account Number',
                             comment='Your company"s account number with the vendor.'),
                      Column('High_Access_Level_Req',
                             String(length=1),
                             nullable=True,
                             doc='High Access Level Required',
                             comment='This Y/N field indicates if the vendor master and ledger require a high access'
                                     'level user to see information.'),
                      Column('Vend_1099',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='1099 Vendor',
                             comment='This Y/N field indicates if the Issued 1099 box in the Vendor Master is'
                                     'checked.'),
                      Column('Vend_Cat',
                             String(length=50),
                             nullable=True,
                             doc='Vendor Category',
                             comment='The reference code for the vendor"s Category.'),
                      Column('Terms_Code',
                             String(length=50),
                             nullable=True,
                             doc='Terms Code',
                             comment='The reference code for the vendor"s terms.'),
                      Column('Currency_Code',
                             String(length=30),
                             nullable=True,
                             doc='Currency Code',
                             comment='The Currency Code for the vendor.'),
                      Column('Remit_To_Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Remit To Vendor Number',
                             comment='The number for the Remit to Vendor'),
                      Column('Expense_GL_Code',
                             String(length=50),
                             nullable=True,
                             doc='Expense GL Code',
                             comment='The Expense G/L Code for the vendor.'),
                      Column('Liability_GL_Num',
                             String(length=50),
                             nullable=True,
                             doc='Liability GL Number',
                             comment='The Liability General Ledger account number'),
                      Column('Buyer',
                             String(length=90),
                             nullable=True,
                             doc='Buyer',
                             comment='The system initials of each Buyer listed for the vendor, separated by commas.'),
                      Column('Primary_Buyer',
                             String(length=3),
                             nullable=True,
                             doc='Primary Buyer',
                             comment='The system initials of the first Buyer listed for the vendor.'),
                      Column('AP_Bal',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='AP Balance',
                             comment='Your current open balance with the vendor.'),
                      Column('Purchs_12_Month',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='12 Month Purchases',
                             comment='The total dollar amount of invoiced purchases from the vendor, year to date.'),
                      Column('Entered_By',
                             String(length=3),
                             nullable=True,
                             doc='Entered By',
                             comment='The system initials of the user who entered the vendor into the system'),
                      Column('Last_Check_Amt',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Last Check Amount',
                             comment='The total amount of the most recent payment made to the vendor.'),
                      Column('Last_Check_Date',
                             Date,
                             nullable=True,
                             doc='Last Check Date',
                             comment='The date that the most recent check was issued to the vendor.'),
                      Column('Last_Check_Num',
                             String(length=50),
                             nullable=True,
                             doc='Last Check Number',
                             comment='The reference number of the most recent check written for payment to that'
                                     'vendor.'),
                      Column('Last_Year_Purchs',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Last Year Purchases',
                             comment='The total dollar value of the purchases made from this vendor for the last'
                                     'calendar year.'),
                      Column('Last_YTD_Pmnts',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Last YTD Payments',
                             comment='The total amount paid to the vendor last year.'),
                      Column('YTD_Pmnts',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='YTD Payments',
                             comment='The total amount paid to the vendor this year to date'),
                      Column('YTD_Purchs',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='YTD Purchases',
                             comment='The dollar value of your Year-to-Date purchases from the vendor.'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date that the vendor was entered into the system.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_general_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_general_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Pay_on_Day',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Pay on Day',
                             comment='The Pay on Day for the vendor.'),
                      Column('Cutoff_Day',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Cutoff Day',
                             comment='The Cutoff Day for the vendor.'),
                      Column('Search_Keyword',
                             String(length=255),
                             nullable=True,
                             doc='Search Keyword',
                             comment='The alternate searching keyword for the vendor.'),
                      Column('Tax_ID',
                             String(length=255),
                             nullable=True,
                             doc='Tax ID',
                             comment='The Tax ID Number for the vendor.'),
                      Column('Our_Acct_Num',
                             String(length=255),
                             nullable=True,
                             doc='Our Account Number',
                             comment='Your company"s account number with the vendor.'),
                      Column('High_Access_Level_Req',
                             String(length=1),
                             nullable=True,
                             doc='High Access Level Required',
                             comment='This Y/N field indicates if the vendor master and ledger require a high access'
                                     'level user to see information.'),
                      Column('Vend_1099',
                             String(length=20),
                             nullable=True,
                             index=True,
                             doc='1099 Vendor',
                             comment='This Y/N field indicates if the Issued 1099 box in the Vendor Master is'
                                     'checked.'),
                      Column('Vend_Cat',
                             String(length=50),
                             nullable=True,
                             doc='Vendor Category',
                             comment='The reference code for the vendor"s Category.'),
                      Column('Terms_Code',
                             String(length=50),
                             nullable=True,
                             doc='Terms Code',
                             comment='The reference code for the vendor"s terms.'),
                      Column('Currency_Code',
                             String(length=30),
                             nullable=True,
                             doc='Currency Code',
                             comment='The Currency Code for the vendor.'),
                      Column('Remit_To_Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Remit To Vendor Number',
                             comment='The number for the Remit to Vendor'),
                      Column('Expense_GL_Code',
                             String(length=50),
                             nullable=True,
                             doc='Expense GL Code',
                             comment='The Expense G/L Code for the vendor.'),
                      Column('Liability_GL_Num',
                             String(length=50),
                             nullable=True,
                             doc='Liability GL Number',
                             comment='The Liability General Ledger account number'),
                      Column('Buyer',
                             String(length=90),
                             nullable=True,
                             doc='Buyer',
                             comment='The system initials of each Buyer listed for the vendor, separated by commas.'),
                      Column('Primary_Buyer',
                             String(length=3),
                             nullable=True,
                             doc='Primary Buyer',
                             comment='The system initials of the first Buyer listed for the vendor.'),
                      Column('AP_Bal',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='AP Balance',
                             comment='Your current open balance with the vendor.'),
                      Column('Purchs_12_Month',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='12 Month Purchases',
                             comment='The total dollar amount of invoiced purchases from the vendor, year to date.'),
                      Column('Entered_By',
                             String(length=3),
                             nullable=True,
                             doc='Entered By',
                             comment='The system initials of the user who entered the vendor into the system'),
                      Column('Last_Check_Amt',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Last Check Amount',
                             comment='The total amount of the most recent payment made to the vendor.'),
                      Column('Last_Check_Date',
                             Date,
                             nullable=True,
                             doc='Last Check Date',
                             comment='The date that the most recent check was issued to the vendor.'),
                      Column('Last_Check_Num',
                             String(length=50),
                             nullable=True,
                             doc='Last Check Number',
                             comment='The reference number of the most recent check written for payment to that'
                                     'vendor.'),
                      Column('Last_Year_Purchs',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Last Year Purchases',
                             comment='The total dollar value of the purchases made from this vendor for the last'
                                     'calendar year.'),
                      Column('Last_YTD_Pmnts',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Last YTD Payments',
                             comment='The total amount paid to the vendor last year.'),
                      Column('YTD_Pmnts',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='YTD Payments',
                             comment='The total amount paid to the vendor this year to date'),
                      Column('YTD_Purchs',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='YTD Purchases',
                             comment='The dollar value of your Year-to-Date purchases from the vendor.'),
                      Column('Entry_Date',
                             Date,
                             nullable=True,
                             doc='Entry Date',
                             comment='The date that the vendor was entered into the system.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_hist_01_current(server_utils.mysql_base):
    __table__ = Table('vend_hist_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Historical_Inv_Amt',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Historical Invoice Amount',
                             comment='All of the past and present invoice amounts for the vendor.'),
                      Column('Historical_Inv_Date',
                             Date,
                             nullable=True,
                             doc='Historical Invoice Date',
                             comment='All of the past and present invoice dates for the vendor.'),
                      Column('Historical_Inv_Num',
                             String(length=50),
                             nullable=True,
                             doc='Historical Invoice Number',
                             comment='All of the past and present invoice numbers for the vendor.'),
                      Column('Historical_PO_Comp_Date',
                             Date,
                             nullable=True,
                             doc='Historical PO Complete Date',
                             comment='The date that the purchase order was completed'),
                      Column('Historical_PO_Date',
                             Date,
                             nullable=True,
                             doc='Historical PO Date',
                             comment='The dates of all open purchase orders for the vendor.'),
                      Column('Historical_PO_Num',
                             String(length=50),
                             nullable=True,
                             doc='Historical PO Number',
                             comment='The P/O Numbers of all purchases for the vendor'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_hist_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_hist_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Historical_Inv_Amt',
                             Numeric(precision=38, scale=4),
                             nullable=True,
                             doc='Historical Invoice Amount',
                             comment='All of the past and present invoice amounts for the vendor.'),
                      Column('Historical_Inv_Date',
                             Date,
                             nullable=True,
                             doc='Historical Invoice Date',
                             comment='All of the past and present invoice dates for the vendor.'),
                      Column('Historical_Inv_Num',
                             String(length=50),
                             nullable=True,
                             doc='Historical Invoice Number',
                             comment='All of the past and present invoice numbers for the vendor.'),
                      Column('Historical_PO_Comp_Date',
                             Date,
                             nullable=True,
                             doc='Historical PO Complete Date',
                             comment='The date that the purchase order was completed'),
                      Column('Historical_PO_Date',
                             Date,
                             nullable=True,
                             doc='Historical PO Date',
                             comment='The dates of all open purchase orders for the vendor.'),
                      Column('Historical_PO_Num',
                             String(length=50),
                             nullable=True,
                             doc='Historical PO Number',
                             comment='The P/O Numbers of all purchases for the vendor'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_main_01_current(server_utils.mysql_base):
    __table__ = Table('vend_main_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Vend_Name',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Name',
                             comment='The name of the vendor, displayed in all capital letters in a column 25'
                                     'characters wide. Vendor names exceeding 25 characters will be continued on'
                                     'another line.'),
                      Column('Status',
                             String(length=1),
                             nullable=True,
                             doc='Status',
                             comment='The Status of the vendor. T = Active/Trade, H = Inactive/Hold'),
                      Column('Address_Line_1',
                             String(length=30),
                             nullable=True,
                             doc='Address Line 1',
                             comment='The first line of the vendor"s address.'),
                      Column('Address_Line_2',
                             String(length=40),
                             nullable=True,
                             doc='Address Line 2',
                             comment='The second line of the vendor"s address.'),
                      Column('City',
                             String(length=255),
                             nullable=True,
                             doc='City',
                             comment='The city of the vendor"s remit-to address, displayed in all upper-case letters.'),
                      Column('State',
                             String(length=255),
                             nullable=True,
                             doc='State',
                             comment='The State for the vendor"s Remit To address.'),
                      Column('Zip_Code',
                             String(length=10),
                             nullable=True,
                             doc='Zip Code',
                             comment='The Zip Code of the vendor"s Remit To address'),
                      Column('City_State_Zip',
                             String(length=40),
                             nullable=True,
                             doc='City State Zip',
                             comment='The City, State, and Zip Code of the vendor"s main address. Blank address will'
                                     'display as a comma.'),
                      Column('Vend_Country',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Country',
                             comment='The Country for the vendor"s Order address.'),
                      Column('Vend_Order_Name',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Order Name',
                             comment='The name of the order vendor.'),
                      Column('Order_Address_Line_1',
                             String(length=40),
                             nullable=True,
                             doc='Order Address Line 1',
                             comment='The first line of the vendor"s order address.'),
                      Column('Order_Address_Line_2',
                             String(length=40),
                             nullable=True,
                             doc='Order Address Line 2',
                             comment='The second line of the vendor"s address.'),
                      Column('Order_City',
                             String(length=20),
                             nullable=True,
                             doc='Order City',
                             comment='The city of the vendor"s order address.'),
                      Column('Order_State',
                             String(length=2),
                             nullable=True,
                             doc='Order State',
                             comment='The State for the vendor"s order address'),
                      Column('Order_Zip_Code',
                             String(length=10),
                             nullable=True,
                             doc='Order Zip Code',
                             comment='The Zip Code of the vendor"s order address.'),
                      Column('Vend_Contact',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Contact',
                             comment='The primary contact for the vendor.'),
                      Column('Phone_Num',
                             String(length=255),
                             nullable=True,
                             doc='Phone Number',
                             comment='The main phone number for the vendor.'),
                      Column('Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Email Address',
                             comment='The default email address for the vendor.'),
                      Column('Contact_Email',
                             String(length=255),
                             nullable=True,
                             doc='Contact Email',
                             comment='The primary email address for the vendor.'),
                      Column('Website',
                             String(length=255),
                             nullable=True,
                             doc='Website',
                             comment='The website address for the vendor.'),
                      Column('Fax_Num',
                             String(length=255),
                             nullable=True,
                             doc='Fax Number',
                             comment='The primary Fax Number for the vendor.'),
                      Column('Contact_Fax',
                             String(length=255),
                             nullable=True,
                             doc='Contact Fax',
                             comment='The primary fax number for the vendor.'),
                      Column('Req_Area_Code_To_Dial',
                             String(length=1),
                             nullable=True,
                             doc='Requires Area Code To Dial',
                             comment='This Y/N field indicates if the Fax Include Area Code box is checked'),
                      Column('Int_Notes_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes Flat',
                             comment='The Internal Notes of the vendor flattened into a single value.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_main_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_main_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Vend_Name',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Name',
                             comment='The name of the vendor, displayed in all capital letters in a column 25'
                                     'characters wide. Vendor names exceeding 25 characters will be continued on'
                                     'another line.'),
                      Column('Status',
                             String(length=1),
                             nullable=True,
                             doc='Status',
                             comment='The Status of the vendor. T = Active/Trade, H = Inactive/Hold'),
                      Column('Address_Line_1',
                             String(length=30),
                             nullable=True,
                             doc='Address Line 1',
                             comment='The first line of the vendor"s address.'),
                      Column('Address_Line_2',
                             String(length=40),
                             nullable=True,
                             doc='Address Line 2',
                             comment='The second line of the vendor"s address.'),
                      Column('City',
                             String(length=255),
                             nullable=True,
                             doc='City',
                             comment='The city of the vendor"s remit-to address, displayed in all upper-case letters.'),
                      Column('State',
                             String(length=255),
                             nullable=True,
                             doc='State',
                             comment='The State for the vendor"s Remit To address.'),
                      Column('Zip_Code',
                             String(length=10),
                             nullable=True,
                             doc='Zip Code',
                             comment='The Zip Code of the vendor"s Remit To address'),
                      Column('City_State_Zip',
                             String(length=40),
                             nullable=True,
                             doc='City State Zip',
                             comment='The City, State, and Zip Code of the vendor"s main address. Blank address will'
                                     'display as a comma.'),
                      Column('Vend_Country',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Country',
                             comment='The Country for the vendor"s Order address.'),
                      Column('Vend_Order_Name',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Order Name',
                             comment='The name of the order vendor.'),
                      Column('Order_Address_Line_1',
                             String(length=40),
                             nullable=True,
                             doc='Order Address Line 1',
                             comment='The first line of the vendor"s order address.'),
                      Column('Order_Address_Line_2',
                             String(length=40),
                             nullable=True,
                             doc='Order Address Line 2',
                             comment='The second line of the vendor"s address.'),
                      Column('Order_City',
                             String(length=20),
                             nullable=True,
                             doc='Order City',
                             comment='The city of the vendor"s order address.'),
                      Column('Order_State',
                             String(length=2),
                             nullable=True,
                             doc='Order State',
                             comment='The State for the vendor"s order address'),
                      Column('Order_Zip_Code',
                             String(length=10),
                             nullable=True,
                             doc='Order Zip Code',
                             comment='The Zip Code of the vendor"s order address.'),
                      Column('Vend_Contact',
                             String(length=255),
                             nullable=True,
                             doc='Vendor Contact',
                             comment='The primary contact for the vendor.'),
                      Column('Phone_Num',
                             String(length=255),
                             nullable=True,
                             doc='Phone Number',
                             comment='The main phone number for the vendor.'),
                      Column('Email_Address',
                             String(length=255),
                             nullable=True,
                             doc='Email Address',
                             comment='The default email address for the vendor.'),
                      Column('Contact_Email',
                             String(length=255),
                             nullable=True,
                             doc='Contact Email',
                             comment='The primary email address for the vendor.'),
                      Column('Website',
                             String(length=255),
                             nullable=True,
                             doc='Website',
                             comment='The website address for the vendor.'),
                      Column('Fax_Num',
                             String(length=255),
                             nullable=True,
                             doc='Fax Number',
                             comment='The primary Fax Number for the vendor.'),
                      Column('Contact_Fax',
                             String(length=255),
                             nullable=True,
                             doc='Contact Fax',
                             comment='The primary fax number for the vendor.'),
                      Column('Req_Area_Code_To_Dial',
                             String(length=1),
                             nullable=True,
                             doc='Requires Area Code To Dial',
                             comment='This Y/N field indicates if the Fax Include Area Code box is checked'),
                      Column('Int_Notes_Flat',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes Flat',
                             comment='The Internal Notes of the vendor flattened into a single value.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_notes_01_current(server_utils.mysql_base):
    __table__ = Table('vend_notes_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Int_Notes',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes',
                             comment='The Internal Notes for the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_notes_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_notes_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Int_Notes',
                             LONGTEXT,
                             nullable=True,
                             doc='Internal Notes',
                             comment='The Internal Notes for the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_purch_01_current(server_utils.mysql_base):
    __table__ = Table('vend_purch_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Ship_Via_Code',
                             String(length=3),
                             nullable=True,
                             doc='Ship Via Code',
                             comment='The default Ship Via code for orders from the vendor.'),
                      Column('Lead_Time_Days',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Lead Time Days',
                             comment='The Lead Time Days for the vendor'),
                      Column('Dflt_Turns',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Default Turns',
                             comment='The Projected Inventory Turns for the vendor.'),
                      Column('EDI_Num',
                             String(length=255),
                             nullable=True,
                             doc='EDI Number',
                             comment='The EDI Number for the vendor.'),
                      Column('Sort_PO_By',
                             String(length=1),
                             nullable=True,
                             doc='Sort PO By',
                             comment='The Sort P/O by selection for the vendor. V = Vendor Part Number, P = Product'
                                     'Number, N = None'),
                      Column('Rebate_Cost_Column',
                             String(length=2),
                             nullable=True,
                             doc='Rebate Cost Column',
                             comment='The Rebate Cost Column for the vendor.'),
                      Column('Freight_Terms',
                             String(length=1),
                             nullable=True,
                             doc='Freight Terms',
                             comment='The Freight Terms code for the vendor.'),
                      Column('Min_Freight_PO_Amt',
                             Numeric(precision=38, scale=2),
                             nullable=True,
                             doc='Minimum Freight PO Amount',
                             comment='The minimum Freight Dollar amount for the vendor.'),
                      Column('Min_PO_Amt',
                             Numeric(precision=38, scale=2),
                             nullable=True,
                             doc='Minimum PO Amount',
                             comment='The minimum Order Dollars amount for the vendor.'),
                      Column('Min_PO_Weight',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Minimum PO Weight',
                             comment='The minimum Volume for the vendor'),
                      Column('Min_PO_Qty',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Minimum PO Quantity',
                             comment='The minimum order Quantity for the vendor.'),
                      Column('Min_PO_Volume',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Minimum PO Volume',
                             comment='The minimum Volume for the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_purch_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_purch_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Ship_Via_Code',
                             String(length=3),
                             nullable=True,
                             doc='Ship Via Code',
                             comment='The default Ship Via code for orders from the vendor.'),
                      Column('Lead_Time_Days',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Lead Time Days',
                             comment='The Lead Time Days for the vendor'),
                      Column('Dflt_Turns',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Default Turns',
                             comment='The Projected Inventory Turns for the vendor.'),
                      Column('EDI_Num',
                             String(length=255),
                             nullable=True,
                             doc='EDI Number',
                             comment='The EDI Number for the vendor.'),
                      Column('Sort_PO_By',
                             String(length=1),
                             nullable=True,
                             doc='Sort PO By',
                             comment='The Sort P/O by selection for the vendor. V = Vendor Part Number, P = Product'
                                     'Number, N = None'),
                      Column('Rebate_Cost_Column',
                             String(length=2),
                             nullable=True,
                             doc='Rebate Cost Column',
                             comment='The Rebate Cost Column for the vendor.'),
                      Column('Freight_Terms',
                             String(length=1),
                             nullable=True,
                             doc='Freight Terms',
                             comment='The Freight Terms code for the vendor.'),
                      Column('Min_Freight_PO_Amt',
                             Numeric(precision=38, scale=2),
                             nullable=True,
                             doc='Minimum Freight PO Amount',
                             comment='The minimum Freight Dollar amount for the vendor.'),
                      Column('Min_PO_Amt',
                             Numeric(precision=38, scale=2),
                             nullable=True,
                             doc='Minimum PO Amount',
                             comment='The minimum Order Dollars amount for the vendor.'),
                      Column('Min_PO_Weight',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Minimum PO Weight',
                             comment='The minimum Volume for the vendor'),
                      Column('Min_PO_Qty',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Minimum PO Quantity',
                             comment='The minimum order Quantity for the vendor.'),
                      Column('Min_PO_Volume',
                             Numeric(precision=38, scale=0),
                             nullable=True,
                             doc='Minimum PO Volume',
                             comment='The minimum Volume for the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_remit_vendors_01_current(server_utils.mysql_base):
    __table__ = Table('vend_remit_vendors_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('All_Remitted_Vends',
                             String(length=10),
                             nullable=True,
                             doc='All Remitted Vendors',
                             comment='Lists all of the vendors that are set to remit payments to the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_remit_vendors_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_remit_vendors_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('All_Remitted_Vends',
                             String(length=10),
                             nullable=True,
                             doc='All Remitted Vendors',
                             comment='Lists all of the vendors that are set to remit payments to the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_source_01_current(server_utils.mysql_base):
    __table__ = Table('vend_source_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Src_Code',
                             String(length=10),
                             nullable=True,
                             doc='Source Code VM',
                             comment='Source Code value marked. They will appear vertically.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_source_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_source_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('Src_Code',
                             String(length=10),
                             nullable=True,
                             doc='Source Code VM',
                             comment='Source Code value marked. They will appear vertically.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_spec_inst_01_current(server_utils.mysql_base):
    __table__ = Table('vend_spec_inst_01_current', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('PO_Instructions',
                             String(length=50),
                             nullable=True,
                             doc='PO Instructions',
                             comment='The Special PO Instructions for the vendor.'),
                      schema='vm')


# noinspection PyPep8Naming
class vend_spec_inst_02_archive(server_utils.mysql_base):
    __table__ = Table('vend_spec_inst_02_archive', server_utils.mysql_base.metadata,
                      Column('ID',
                             Integer,
                             primary_key=True,
                             unique=True,
                             index=True,
                             autoincrement=True,
                             doc='ID',
                             comment='N/A'),
                      Column('Date_Time_Stamp',
                             DateTime,
                             nullable=True,
                             doc='Date Time Stamp',
                             comment='N/A'),
                      Column('Vend_Num',
                             String(length=7),
                             nullable=True,
                             doc='Vendor Number',
                             comment='The reference number for the vendor.'),
                      Column('PO_Instructions',
                             String(length=50),
                             nullable=True,
                             doc='PO Instructions',
                             comment='The Special PO Instructions for the vendor.'),
                      schema='vm')


