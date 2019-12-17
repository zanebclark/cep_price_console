from sqlalchemy import Column, Integer, VARCHAR, DATE, DECIMAL, INT, Table
from cep_price_console.utils.log_utils import CustomAdapter
from cep_price_console.db_management.server_utils import mysql_base
import logging

logger = CustomAdapter(logging.getLogger(str(__name__)), None)


class UploadMulti(mysql_base):
    __table__ = Table('upload_multi', mysql_base.metadata,
                      Column('ID', Integer, primary_key=True, doc="ID"),
                      Column('VendCntrNum', VARCHAR(225), doc="Vendor Contract Number"),
                      Column('VendProdNum', VARCHAR(225), doc="Vendor Product Number"),
                      Column('CustProdNum', VARCHAR(225), doc="Customer Product Number"),
                      Column('QBreak', INT, doc="Quantity Break"),
                      Column('UOM', VARCHAR(225), doc="Unit of Measure"),
                      Column('P1_ContrPrice', DECIMAL(19, 4), doc="Contract Price"),
                      Column('P1_ContrCost', DECIMAL(19, 4), doc="Contract Cost"),
                      Column('P1_EffDate', DATE, doc="Period 1: Effective Date"),
                      Column('P1_ExpDate', DATE, doc="Period 1: Expiration Date"),
                      Column('P2_ContrPrice', DECIMAL(19, 4), doc="Contract Price"),
                      Column('P2_ContrCost', DECIMAL(19, 4), doc="Contract Cost"),
                      Column('P2_EffDate', DATE, doc="Period 2: Effective Date"),
                      Column('P2_ExpDate', DATE, doc="Period 2: Expiration Date"),
                      Column('P3_ContrPrice', DECIMAL(19, 4), doc="Contract Price"),
                      Column('P3_ContrCost', DECIMAL(19, 4), doc="Contract Cost"),
                      Column('P3_EffDate', DATE, doc="Period 3: Effective Date"),
                      Column('P3_ExpDate', DATE, doc="Period 3: Expiration Date"),
                      schema='pythontest',
                      # mysql_engine='InnoDB'
                      )

    # logger.info("SQL Alchemy Table Instantiated. Class: {0}, Table: {1}".format(__name__, __table__.__doc__))


class UploadMono(mysql_base):
    __table__ = Table('upload_mono', mysql_base.metadata,
                      Column('UploadMono_ID', Integer, primary_key=True),
                      Column('UploadMulti_ID', Integer),
                      Column('VendCntrNum', VARCHAR(225)),
                      Column('CEPCntrNum', VARCHAR(225)),
                      Column('Vendor_ID', VARCHAR(225)),
                      Column('VendProdNum', VARCHAR(225)),
                      Column('CustProdNum', VARCHAR(225)),
                      Column('QBreak', INT),
                      Column('UOM', VARCHAR(225)),
                      Column('ContrPrice', DECIMAL(19, 4)),
                      Column('ContrCost', DECIMAL(19, 4)),
                      Column('EffDate', DATE),
                      Column('ExpDate', DATE),
                      Column('Period', INT),
                      schema='pythontest',
                      # mysql_engine='InnoDB'
                      )
    # logger.info("SQL Alchemy Table Instantiated. Class: {0}, Table: {1}".format(__name__, __table__.__doc__))


class UploadMatched(mysql_base):
    __table__ = Table('upload_matched', mysql_base.metadata,
                      Column('UploadMatched_ID', Integer, primary_key=True),
                      Column('UploadMono_ID', Integer),
                      Column('UploadMulti_ID', Integer),
                      Column('VendCntrNum', VARCHAR(225)),
                      Column('CEPCntrNum', VARCHAR(225)),
                      Column('Vendor_ID', VARCHAR(225)),
                      Column('VendProdNum', VARCHAR(225)),
                      Column('CEPProdNum', VARCHAR(225)),
                      Column('CustProdNum', VARCHAR(225)),
                      Column('QBreak', INT),
                      Column('UOM', VARCHAR(225)),
                      Column('ContrPrice', DECIMAL(19, 4)),
                      Column('ContrCost', DECIMAL(19, 4)),
                      Column('EffDate', DATE),
                      Column('ExpDate', DATE),
                      Column('Period', INT),
                      Column('Mtrx_Sheet', VARCHAR(225)),
                      Column('Mtrx_Counter', INT),
                      schema='pythontest',
                      # mysql_engine='InnoDB'
                      )
    # logger.info("SQL Alchemy Table Instantiated. Class: {0}, Table: {1}".format(__name__, __table__.__doc__))


class ProductMatching(mysql_base):
    __table__ = Table('cntr_prodmatching', mysql_base.metadata,
                      Column('Prod_Match_ID', Integer, primary_key=True),
                      Column('Vendor_ID', VARCHAR(225)),
                      Column('VendProdNum', VARCHAR(225)),
                      Column('CustProdNum', VARCHAR(225)),
                      Column('CEP_Part_Num', VARCHAR(225)),
                      Column('Count', Integer),
                      schema='pythontest',
                      # mysql_engine='InnoDB'
                      )
    # logger.info("SQL Alchemy Table Instantiated. Class: {0}, Table: {1}".format(__name__, __table__.__doc__))
