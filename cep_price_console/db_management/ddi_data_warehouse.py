from cep_price_console.db_management.server_utils import mysql_base
from sqlalchemy import Column, DECIMAL, DateTime, Integer, Table, Unicode, text
from sqlalchemy.ext.declarative import DeferredReflection


class DDIDataWarehouse(DeferredReflection, mysql_base):
    __abstract__ = True


aging_definition = Table(
    'AGING DEFINITION', DDIDataWarehouse.metadata,
    Column('AGINGCODE', Unicode(100)),
    Column('AGINGDESCRIPTION', Unicode(500)),
    Column('AGINGID', Integer, nullable=False),
    schema="DDIDataWarehouse"
)

ar_history = Table(
    'ARHISTORY', DDIDataWarehouse.metadata,
    Column('SJPERIOD', Unicode(4)),
    Column('CUSTOMERCODE', Unicode(100)),
    Column('CUSTOMERDEFAULTBRANCHCODE', Unicode(100)),
    Column('AREOMVALUE', DECIMAL(14, 4), nullable=False),
    Column('EXTENDEDSALE', DECIMAL(14, 4)),
    Column('CUSTOMERID', Integer),
    Column('CUSTOMERDEFAULTBRANCHID', Integer),
    Column('SJDATE', DateTime),
    Column('ARHISTORYID', Integer, primary_key=True),
    schema="DDIDataWarehouse"
)

branch = Table(
    'BRANCH', DDIDataWarehouse.metadata,
    Column('BRANCHCODE', Unicode(100), nullable=False),
    Column('BRANCHDESC', Unicode(500)),
    Column('DIVISIONCODE', Unicode(100)),
    Column('BRANCHID', Integer, primary_key=True),
    Column('DIVISIONID', Integer),
    Column('BRANCHCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

buy_line = Table(
    'BUYLINE', DDIDataWarehouse.metadata,
    Column('BUYLINECODE', Unicode(100)),
    Column('BUYLINEDESC', Unicode(500)),
    Column('BUYLINEID', Integer, primary_key=True),
    Column('BUYLINECODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

cust_category = Table(
    'CUSTCATEGORY', DDIDataWarehouse.metadata,
    Column('CUSTOMERCATCODE', Unicode(100)),
    Column('CUSTOMERCATDESC', Unicode(500)),
    Column('CUSTOMERCATID', Integer, primary_key=True),
    Column('CUSTOMERCATCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

customer = Table(
    'CUSTOMER', DDIDataWarehouse.metadata,
    Column('CUSTOMERCODE', Unicode(100), nullable=False),
    Column('CUSTOMERDESC', Unicode(500)),
    Column('ADD1', Unicode(500)),
    Column('ADD2', Unicode(500)),
    Column('CITY', Unicode(500)),
    Column('STATE', Unicode(500)),
    Column('ZIP', Unicode(100)),
    Column('PHONE', Unicode(20)),
    Column('FAX', Unicode(20)),
    Column('EMAIL', Unicode(100)),
    Column('CONTACT', Unicode(100)),
    Column('SALESMANCODE', Unicode(100)),
    Column('TERRITORYCODE', Unicode(100)),
    Column('TYPE', Unicode(500)),
    Column('CATEGORYCODE', Unicode(100)),
    Column('AGING1', DECIMAL(14, 4)),
    Column('AGING2', DECIMAL(14, 4)),
    Column('AGING3', DECIMAL(14, 4)),
    Column('AGING4', DECIMAL(14, 4)),
    Column('AGING5', DECIMAL(14, 4)),
    Column('AGING6', DECIMAL(14, 4)),
    Column('AGING7', DECIMAL(14, 4)),
    Column('CUSTOMERID', Integer, primary_key=True),
    Column('SALESMANID', Integer),
    Column('TERRITORYID', Integer),
    Column('CATEGORYID', Integer),
    Column('CUSTOMERCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

division = Table(
    'DIVISION', DDIDataWarehouse.metadata,
    Column('DIVISIONCODE', Unicode(100), nullable=False),
    Column('DIVISIONDESC', Unicode(500)),
    Column('DIVISIONID', Integer, primary_key=True),
    Column('DIVISIONCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

inventory = Table(
    'INVENTORY', DDIDataWarehouse.metadata,
    Column('PRODUCTCODE', Unicode(100), nullable=False),
    Column('WAREHOUSECODE', Unicode(100), nullable=False),
    Column('WAREHOUSERANK', Unicode(100)),
    Column('ONHAND', DECIMAL(14, 4), nullable=False),
    Column('ONCOMMIT', DECIMAL(14, 4), nullable=False),
    Column('AVAILABLE', DECIMAL(14, 4), nullable=False),
    Column('ONPO', DECIMAL(14, 4), nullable=False),
    Column('ONTRANSFER', DECIMAL(14, 4), nullable=False),
    Column('STOCKVALUE', DECIMAL(14, 4), nullable=False),
    Column('REORDERPOINT', DECIMAL(14, 4)),
    Column('TWELVEMHITS', DECIMAL(14, 4), nullable=False),
    Column('TWELVEMCOST', DECIMAL(14, 4), nullable=False),
    Column('TWELVEMSALES', DECIMAL(14, 4), nullable=False),
    Column('TWELVEMUNITS', DECIMAL(14, 4), nullable=False),
    Column('TWELVEMDEMAND', DECIMAL(14, 4), nullable=False),
    Column('TWELVEMAVERAGEINVAL', DECIMAL(14, 4), nullable=False),
    Column('ONTRANSFERIN', DECIMAL(14, 4)),
    Column('PRODUCTID', Integer),
    Column('WAREHOUSEID', Integer),
    Column('TWELVEMPROFIT', DECIMAL(15, 4)),
    schema="DDIDataWarehouse"
)

inventory_history = Table(
    'INVENTORYHISTORY', DDIDataWarehouse.metadata,
    Column('PRODUCTCODE', Unicode(100), nullable=False),
    Column('WAREHOUSECODE', Unicode(100)),
    Column('ONHAND0', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE0', DECIMAL(14, 4), nullable=False),
    Column('ONHAND1', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE1', DECIMAL(14, 4), nullable=False),
    Column('ONHAND2', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE2', DECIMAL(14, 4), nullable=False),
    Column('ONHAND3', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE3', DECIMAL(14, 4), nullable=False),
    Column('ONHAND4', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE4', DECIMAL(14, 4), nullable=False),
    Column('ONHAND5', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE5', DECIMAL(14, 4), nullable=False),
    Column('ONHAND6', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE6', DECIMAL(14, 4), nullable=False),
    Column('ONHAND7', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE7', DECIMAL(14, 4), nullable=False),
    Column('ONHAND8', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE8', DECIMAL(14, 4), nullable=False),
    Column('ONHAND9', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE9', DECIMAL(14, 4), nullable=False),
    Column('ONHAND10', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE10', DECIMAL(14, 4), nullable=False),
    Column('ONHAND11', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE11', DECIMAL(14, 4), nullable=False),
    Column('ONHAND12', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE12', DECIMAL(14, 4), nullable=False),
    Column('ONHAND13', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE13', DECIMAL(14, 4), nullable=False),
    Column('ONHAND14', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE14', DECIMAL(14, 4), nullable=False),
    Column('ONHAND15', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE15', DECIMAL(14, 4), nullable=False),
    Column('ONHAND16', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE16', DECIMAL(14, 4), nullable=False),
    Column('ONHAND17', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE17', DECIMAL(14, 4), nullable=False),
    Column('ONHAND18', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE18', DECIMAL(14, 4), nullable=False),
    Column('ONHAND19', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE19', DECIMAL(14, 4), nullable=False),
    Column('ONHAND20', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE20', DECIMAL(14, 4), nullable=False),
    Column('ONHAND21', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE21', DECIMAL(14, 4), nullable=False),
    Column('ONHAND22', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE22', DECIMAL(14, 4), nullable=False),
    Column('ONHAND23', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE23', DECIMAL(14, 4), nullable=False),
    Column('ONHAND24', DECIMAL(14, 4), nullable=False),
    Column('INVENTORYVALUE24', DECIMAL(14, 4), nullable=False),
    Column('PRODUCTID', Integer),
    Column('WAREHOUSEID', Integer),
    schema="DDIDataWarehouse"
)

invoice_detail = Table(
    'INVOICEDETAIL', DDIDataWarehouse.metadata,
    Column('INVOICECODE', Unicode(100), nullable=False),
    Column('LINENUM', DECIMAL(14, 4)),
    Column('PRODUCTCODE', Unicode(100), nullable=False),
    Column('SPDESCRIPTION', Unicode(691)),
    Column('WAREHOUSECODE', Unicode(100)),
    Column('SELLINGUOM', Unicode(10)),
    Column('PRICINGUOM', Unicode(10)),
    Column('COSTMETHOD', Unicode(100)),
    Column('PRICEMETHOD', Unicode(100)),
    Column('FILLSTATUS', Unicode(2)),
    Column('QUANTITYSHIPPED', DECIMAL(14, 4), nullable=False),
    Column('EXTENDEDCOST', DECIMAL(14, 4), nullable=False),
    Column('EXTENDEDGLCOST', DECIMAL(14, 4), nullable=False),
    Column('EXTENDEDSLMNCOST', DECIMAL(14, 4), nullable=False),
    Column('EXTENDEDSALE', DECIMAL(14, 4), nullable=False),
    Column('COMMISSION', DECIMAL(14, 4)),
    Column('ORIGINALQUANTITY', DECIMAL(14, 4)),
    Column('NETPRICE', DECIMAL(14, 4)),
    Column('INVOICEDETAILID', Integer, primary_key=True),
    Column('INVOICEID', Integer),
    Column('PRODUCTID', Integer),
    Column('WAREHOUSEID', Integer),
    Column('VENDORID', Integer),
    Column('VENDORCODE', Unicode(100)),
    Column('EXTENDEDPROFIT', DECIMAL(15, 4)),
    Column('EXTENDEDSLMNPROFIT', DECIMAL(15, 4)),
    Column('EXTENDEDGLPROFIT', DECIMAL(15, 4)),
    schema="DDIDataWarehouse"
)

invoice_header = Table(
    'INVOICEHEADER', DDIDataWarehouse.metadata,
    Column('INVOICECODE', Unicode(100), nullable=False),
    Column('CUSTOMERCODE', Unicode(100)),
    Column('SALESMANCODE', Unicode(100)),
    Column('SHIPTOCODE', Unicode(100)),
    Column('SHIPVIACODE', Unicode(100)),
    Column('BRANCHCODE', Unicode(100)),
    Column('ORDERWRITERCODE', Unicode(100)),
    Column('INVOICEDATE', DateTime),
    Column('ORDERDATE', DateTime),
    Column('FISCALPERIOD', Unicode(4)),
    Column('SJPERIOD', Unicode(4)),
    Column('VOIDED', Unicode(50)),
    Column('JOBID', Unicode(100)),
    Column('CUSTOMERPO', Unicode(231)),
    Column('ORDERTYPE', Unicode(100)),
    Column('FREIGHT', DECIMAL(14, 4)),
    Column('MISC', DECIMAL(14, 4)),
    Column('TAX', DECIMAL(14, 4)),
    Column('INVOICETOTAL', DECIMAL(14, 4)),
    Column('INVOICEBALANCE', DECIMAL(14, 4)),
    Column('SHIPTOCITY', Unicode(100)),
    Column('SHIPTOSTATE', Unicode(100)),
    Column('SHIPTOZIP', Unicode(100)),
    Column('TERRITORYCODE', Unicode(100)),
    Column('CASHSALE', Unicode(1)),
    Column('INVOICEID', Integer, primary_key=True),
    Column('CUSTOMERID', Integer),
    Column('SALESMANID', Integer),
    Column('SHIPTOID', Integer),
    Column('SHIPVIAID', Integer),
    Column('BRANCHID', Integer),
    Column('ORDERWRITERID', Integer),
    Column('TERRITORYID', Integer),
    Column('FISCALDATE', DateTime),
    Column('SJDATE', DateTime),
    Column('ISCASHSALE', Integer, nullable=False),
    schema="DDIDataWarehouse"
)

invoice_summary = Table(
    'INVOICESUMMARY', DDIDataWarehouse.metadata,
    Column('INVOICEDATE', DateTime),
    Column('ORDERDATE', DateTime),
    Column('FISCALPERIOD', Unicode(4)),
    Column('SJPERIOD', Unicode(4)),
    Column('VOIDED', Unicode(1)),
    Column('JOBID', Unicode(10)),
    Column('CUSTOMERPO', Unicode(30)),
    Column('ORDERTYPE', Unicode(8)),
    Column('CUSTOMERID', Integer),
    Column('SALESMANID', Integer),
    Column('SHIPTOID', Integer),
    Column('SHIPVIAID', Integer),
    Column('BRANCHID', Integer),
    Column('PRODUCTID', Integer),
    Column('WAREHOUSEID', Integer),
    Column('FILLED', Integer),
    Column('PTFILLED', Integer),
    Column('QUANTITYSHIPPED', DECIMAL(14, 4)),
    Column('EXTENDEDCOST', DECIMAL(14, 4)),
    Column('EXTENDEDGLCOST', DECIMAL(14, 4)),
    Column('EXTENDEDSLMNCOST', DECIMAL(14, 4)),
    Column('EXTENDEDSALE', DECIMAL(14, 4)),
    Column('COMMISSION', DECIMAL(14, 4)),
    Column('SHIPTOCITY', Unicode(100)),
    Column('SHIPTOSTATE', Unicode(100)),
    Column('SHIPTOZIP', Unicode(100)),
    Column('TERRITORYCODE', Unicode(100)),
    Column('INVOICESUMMARYID', Integer, primary_key=True),
    Column('FISCALDATE', DateTime),
    Column('EXTENDEDPROFIT', DECIMAL(15, 4)),
    Column('EXTENDEDSLMNPROFIT', DECIMAL(15, 4)),
    Column('EXTENDEDGLPROFIT', DECIMAL(15, 4)),
    Column('ORDERWRITERID', Integer),
    Column('TERRITORYID', Integer),
    Column('INVOICEID', Integer),
    Column('INVOICECODE', Unicode(100)),
    Column('SJDATE', DateTime),
    schema="DDIDataWarehouse"
)

invoice_variance = Table(
    'INVOICEVARIANCE', DDIDataWarehouse.metadata,
    Column('CUSTOMERID', Integer),
    Column('SHIPTOID', Integer),
    Column('SHIPVIAID', Integer),
    Column('BRANCHID', Integer),
    Column('ORDERWRITERID', Integer),
    Column('PRODUCTID', Integer),
    Column('WAREHOUSEID', Integer),
    Column('YTDSALES', DECIMAL(14, 4)),
    Column('LYTDSALES', DECIMAL(14, 4)),
    Column('FYTDSALES', DECIMAL(14, 4)),
    Column('LFYTDSALES', DECIMAL(14, 4)),
    Column('YTDCOST', DECIMAL(14, 4)),
    Column('LYTDCOST', DECIMAL(14, 4)),
    Column('FYTDCOST', DECIMAL(14, 4)),
    Column('LFYTDCOST', DECIMAL(14, 4)),
    Column('YTDUNITS', DECIMAL(14, 4)),
    Column('LYTDUNITS', DECIMAL(14, 4)),
    Column('FYTDUNITS', DECIMAL(14, 4)),
    Column('LFYTDUNITS', DECIMAL(14, 4)),
    Column('YTDPROFIT', DECIMAL(15, 4)),
    Column('LYTDPROFIT', DECIMAL(15, 4)),
    Column('FYTDPROFIT', DECIMAL(15, 4)),
    Column('LFYTDPROFIT', DECIMAL(15, 4)),
    Column('SALESVARIANCE', DECIMAL(15, 4)),
    Column('COSTVARIANCE', DECIMAL(15, 4)),
    Column('PROFITVARIANCE', DECIMAL(16, 4)),
    Column('UNITSVARIANCE', DECIMAL(15, 4)),
    Column('FSALESVARIANCE', DECIMAL(15, 4)),
    Column('FCOSTVARIANCE', DECIMAL(15, 4)),
    Column('FPROFITVARIANCE', DECIMAL(16, 4)),
    Column('FUNITSVARIANCE', DECIMAL(15, 4)),
    Column('SALESMANCODE', Unicode(4)),
    schema="DDIDataWarehouse"
)

price_group = Table(
    'PRICEGROUP', DDIDataWarehouse.metadata,
    Column('PRICEGROUPCODE', Unicode(100), nullable=False),
    Column('PRICEGROUPDESC', Unicode(500)),
    Column('PRICEGROUPID', Integer, primary_key=True),
    Column('PRICEGROUPCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

prod_line = Table(
    'PRODLINE', DDIDataWarehouse.metadata,
    Column('PRODUCTLINECODE', Unicode(100), nullable=False),
    Column('PRODUCTLINEDESC', Unicode(500)),
    Column('MAJORGROUP', Unicode(100)),
    Column('PRODUCTLINEBUYERS', Unicode(500)),
    Column('PRODUCTLINEID', Integer, primary_key=True),
    Column('PRODUCTLINECODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

product = Table(
    'PRODUCT', DDIDataWarehouse.metadata,
    Column('PRODUCTCODE', Unicode(100), nullable=False),
    Column('PRODUCTLINECODE', Unicode(100)),
    Column('PRICEGROUPCODE', Unicode(100)),
    Column('BUYLINECODE', Unicode(100)),
    Column('VENDORCODE', Unicode(100)),
    Column('WEBCATCODE', Unicode(100)),
    Column('STATUS', Unicode(1)),
    Column('OVERALLRANK', Unicode(1)),
    Column('PRODUCTDESC', Unicode(500)),
    Column('C1COST', DECIMAL(14, 4)),
    Column('C2COST', DECIMAL(14, 4)),
    Column('C3COST', DECIMAL(14, 4)),
    Column('C4COST', DECIMAL(14, 4)),
    Column('C5COST', DECIMAL(14, 4)),
    Column('C6COST', DECIMAL(14, 4)),
    Column('C7COST', DECIMAL(14, 4)),
    Column('L1PRICE', DECIMAL(14, 4)),
    Column('L2PRICE', DECIMAL(14, 4)),
    Column('L3PRICE', DECIMAL(14, 4)),
    Column('L4PRICE', DECIMAL(14, 4)),
    Column('PRODUCTID', Integer, primary_key=True),
    Column('PRODUCTLINEID', Integer, nullable=False, server_default=text("((0))")),
    Column('PRICEGROUPID', Integer, nullable=False, server_default=text("((0))")),
    Column('BUYLINEID', Integer, nullable=False, server_default=text("((0))")),
    Column('VENDORID', Integer, nullable=False, server_default=text("((0))")),
    Column('WEBCATID', Integer, nullable=False, server_default=text("((0))")),
    Column('PRODUCTCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

purchase_order_detail = Table(
    'PURCHASEORDERDETAIL', DDIDataWarehouse.metadata,
    Column('POCODE', Unicode(100), nullable=False),
    Column('RECEIVINGCODE', Unicode(100), nullable=False),
    Column('PRODUCTCODE', Unicode(100), nullable=False),
    Column('UNITS', DECIMAL(14, 4), nullable=False),
    Column('COST', DECIMAL(14, 4), nullable=False),
    Column('PORECEIVINGID', Integer),
    Column('PRODUCTID', Integer),
    schema="DDIDataWarehouse"
)

purchase_order_header = Table(
    'PURCHASEORDERHEADER', DDIDataWarehouse.metadata,
    Column('POCODE', Unicode(100), nullable=False),
    Column('RECEIVINGCODE', Unicode(100), nullable=False),
    Column('VENDORCODE', Unicode(100)),
    Column('RECEIVINGDATE', DateTime),
    Column('SJPERIOD', Unicode(4)),
    Column('PODATE', DateTime),
    Column('BRANCHCODE', Unicode(100)),
    Column('PORECEIVINGID', Integer, primary_key=True),
    Column('VENDORID', Integer),
    Column('BRANCHID', Integer),
    Column('SJDATE', DateTime),
    schema="DDIDataWarehouse"
)

salesman = Table(
    'SALESMAN', DDIDataWarehouse.metadata,
    Column('SALESMANCODE', Unicode(100), nullable=False),
    Column('SALESMANDESC', Unicode(200)),
    Column('SALESMANID', Integer, primary_key=True),
    Column('SALESMANCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

ship_to = Table(
    'SHIPTO', DDIDataWarehouse.metadata,
    Column('SHIPTOCODE', Unicode(100), nullable=False),
    Column('CUSTOMERCODE', Unicode(100)),
    Column('SHIPTODESC', Unicode(500)),
    Column('ADD1', Unicode(500)),
    Column('ADD2', Unicode(500)),
    Column('CITY', Unicode(500)),
    Column('STATE', Unicode(500)),
    Column('ZIP', Unicode(20)),
    Column('SHIPTOID', Integer, primary_key=True),
    Column('CUSTOMERID', Integer),
    Column('SHIPTOSUBCODE', Unicode(4000)),
    Column('SHIPTOCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

ship_via = Table(
    'SHIPVIA', DDIDataWarehouse.metadata,
    Column('SHIPVIACODE', Unicode(12)),
    Column('SHIPVIADESC', Unicode(500)),
    Column('SHIPVIATYPE', Unicode(20)),
    Column('SHIPVIAID', Integer, primary_key=True),
    Column('SHIPVIACODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

territory = Table(
    'TERRITORY', DDIDataWarehouse.metadata,
    Column('TERRITORYCODE', Unicode(10)),
    Column('TERRITORYDESC', Unicode(500)),
    Column('TERRITORYID', Integer, primary_key=True),
    Column('TERRITORYCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

user = Table(
    'USER', DDIDataWarehouse.metadata,
    Column('USERCODE', Unicode(10), nullable=False),
    Column('USERDESC', Unicode(500)),
    Column('USERID', Integer, primary_key=True),
    Column('USERCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

vm = Table(
    'VM', DDIDataWarehouse.metadata,
    Column('VENDORCODE', Unicode(100), nullable=False),
    Column('VENDORDESC', Unicode(500)),
    Column('ADD1', Unicode(500)),
    Column('ADD2', Unicode(500)),
    Column('CITY', Unicode(500)),
    Column('STATE', Unicode(500)),
    Column('ZIP', Unicode(500)),
    Column('PHONE', Unicode(500)),
    Column('FAX', Unicode(500)),
    Column('EMAIL', Unicode(500)),
    Column('CONTACT', Unicode(500)),
    Column('INVENTORYTURNS', DECIMAL(14, 4)),
    Column('LEADTIMEDAYS', DECIMAL(14, 4)),
    Column('VENDORCATEGORYCODE', Unicode(100)),
    Column('VENDORBUYERS', Unicode(500)),
    Column('VENDORID', Integer, primary_key=True),
    Column('VENDORCATEGORYID', Integer),
    Column('VENDORCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

vm_category = Table(
    'VMCATEGORY', DDIDataWarehouse.metadata,
    Column('VENDORCATCODE', Unicode(100), nullable=False),
    Column('VENDORCATDESC', Unicode(500)),
    Column('VENDORCATID', Integer, primary_key=True),
    Column('VENDORCATCODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

warehouse = Table(
    'WAREHOUSE', DDIDataWarehouse.metadata,
    Column('WAREHOUSECODE', Unicode(100), nullable=False),
    Column('WAREHOUSEDESC', Unicode(500)),
    Column('WAREHOUSETYPE', Unicode(50)),
    Column('WAREHOUSEID', Integer, primary_key=True),
    Column('WAREHOUSECODEDESC', Unicode(500)),
    schema="DDIDataWarehouse"
)

webcat = Table(
    'WEBCAT', DDIDataWarehouse.metadata,
    Column('WEBCATCODE', Unicode(100), nullable=False),
    Column('WEBCATDESC', Unicode(500)),
    Column('WEBCATPARENTCODE', Unicode(100)),
    Column('WEBCATID', Integer, primary_key=True),
    Column('WEBCATPARENTID', Integer),
    schema="DDIDataWarehouse"
)
