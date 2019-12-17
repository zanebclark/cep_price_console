from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import Table, func
from sqlalchemy.sql import case, and_, or_, literal
from sqlalchemy.ext.hybrid import hybrid_property
import cep_price_console.db_management.server_utils as server_utils


# Workbook Filename: C:\Users\zane\PycharmProjects\cep_price_console\data\ARW_PRF_Mapping\ARW_PRF_Definitions_v1
# _03.xlsm

# Timestamp: 2019-07-18 13:54:25


class InformReflection(DeferredReflection, server_utils.mysql_base):
    __abstract__ = True


# noinspection PyPep8Naming
class days_since_last_sale_01_current(InformReflection):
    __table__ = Table('days_since_last_sale_01_current', server_utils.mysql_base.metadata,
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
class days_since_last_sale_02_archive(InformReflection):
    __table__ = Table('days_since_last_sale_02_archive', server_utils.mysql_base.metadata,
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
class cust_alias_01_current(InformReflection):
    __table__ = Table('cust_alias_01_current', server_utils.mysql_base.metadata,
                      schema='cust.pn.xref')


# noinspection PyPep8Naming
class cust_alias_02_archive(InformReflection):
    __table__ = Table('cust_alias_02_archive', server_utils.mysql_base.metadata,
                      schema='cust.pn.xref')


# noinspection PyPep8Naming
class cust_01_static(InformReflection):
    __table__ = Table('cust_01_static', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_address_01_current(InformReflection):
    __table__ = Table('cust_address_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_address_02_archive(InformReflection):
    __table__ = Table('cust_address_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_attachments_01_current(InformReflection):
    __table__ = Table('cust_attachments_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_attachments_02_archive(InformReflection):
    __table__ = Table('cust_attachments_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_credit_01_current(InformReflection):
    __table__ = Table('cust_credit_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_credit_02_archive(InformReflection):
    __table__ = Table('cust_credit_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_freight_01_current(InformReflection):
    __table__ = Table('cust_freight_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_freight_02_archive(InformReflection):
    __table__ = Table('cust_freight_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_indices_01_current(InformReflection):
    __table__ = Table('cust_indices_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_indices_02_archive(InformReflection):
    __table__ = Table('cust_indices_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_inv_message_01_current(InformReflection):
    __table__ = Table('cust_inv_message_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_inv_message_02_archive(InformReflection):
    __table__ = Table('cust_inv_message_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_master_01_current(InformReflection):
    __table__ = Table('cust_master_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_master_02_archive(InformReflection):
    __table__ = Table('cust_master_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_monthly_01_current(InformReflection):
    __table__ = Table('cust_monthly_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_monthly_02_archive(InformReflection):
    __table__ = Table('cust_monthly_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_rank_01_current(InformReflection):
    __table__ = Table('cust_rank_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_rank_02_archive(InformReflection):
    __table__ = Table('cust_rank_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_restk_policy_01_current(InformReflection):
    __table__ = Table('cust_restk_policy_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_restk_policy_02_archive(InformReflection):
    __table__ = Table('cust_restk_policy_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_route_01_current(InformReflection):
    __table__ = Table('cust_route_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_route_02_archive(InformReflection):
    __table__ = Table('cust_route_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_so_misc_charge_program_01_current(InformReflection):
    __table__ = Table('cust_so_misc_charge_program_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_so_misc_charge_program_02_archive(InformReflection):
    __table__ = Table('cust_so_misc_charge_program_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_special_instr_01_current(InformReflection):
    __table__ = Table('cust_special_instr_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_special_instr_02_archive(InformReflection):
    __table__ = Table('cust_special_instr_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_stats_01_current(InformReflection):
    __table__ = Table('cust_stats_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_stats_02_archive(InformReflection):
    __table__ = Table('cust_stats_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_subaccounts_01_current(InformReflection):
    __table__ = Table('cust_subaccounts_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_subaccounts_02_archive(InformReflection):
    __table__ = Table('cust_subaccounts_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_vend_ids_01_current(InformReflection):
    __table__ = Table('cust_vend_ids_01_current', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class cust_vend_ids_02_archive(InformReflection):
    __table__ = Table('cust_vend_ids_02_archive', server_utils.mysql_base.metadata,
                      schema='customer')

    @hybrid_property
    def Cust_Num_ShipTo_Combo(self):
        return self.__table__.c.Cust_Num + literal("_All")
    
    # noinspection PyMethodParameters
    @Cust_Num_ShipTo_Combo.expression
    def Cust_Num_ShipTo_Combo(cls):
        return func.concat(cls.__table__.c.Cust_Num, literal("_All"))


# noinspection PyPep8Naming
class po_04_rec_detail_01_current(InformReflection):
    __table__ = Table('po_04_rec_detail_01_current', server_utils.mysql_base.metadata,
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_04_rec_detail_02_archive(InformReflection):
    __table__ = Table('po_04_rec_detail_02_archive', server_utils.mysql_base.metadata,
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_05_rec_lot_01_current(InformReflection):
    __table__ = Table('po_05_rec_lot_01_current', server_utils.mysql_base.metadata,
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_05_rec_lot_02_archive(InformReflection):
    __table__ = Table('po_05_rec_lot_02_archive', server_utils.mysql_base.metadata,
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_06_rec_serial_01_current(InformReflection):
    __table__ = Table('po_06_rec_serial_01_current', server_utils.mysql_base.metadata,
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class po_06_rec_serial_02_archive(InformReflection):
    __table__ = Table('po_06_rec_serial_02_archive', server_utils.mysql_base.metadata,
                      schema='daily.rec.rep')

    @hybrid_property
    def PO_Rvcing_Line_Num(self):
        return self.PO_Rcving_Num + "_" + self.Line_Num


# noinspection PyPep8Naming
class price_matrix_future_01_current(InformReflection):
    __table__ = Table('price_matrix_future_01_current', server_utils.mysql_base.metadata,
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
class price_matrix_future_02_archive(InformReflection):
    __table__ = Table('price_matrix_future_02_archive', server_utils.mysql_base.metadata,
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
class gl_groups_01_current(InformReflection):
    __table__ = Table('gl_groups_01_current', server_utils.mysql_base.metadata,
                      schema='gl.group')


# noinspection PyPep8Naming
class gl_groups_02_archive(InformReflection):
    __table__ = Table('gl_groups_02_archive', server_utils.mysql_base.metadata,
                      schema='gl.group')


# noinspection PyPep8Naming
class gl_groups_rpts_01_current(InformReflection):
    __table__ = Table('gl_groups_rpts_01_current', server_utils.mysql_base.metadata,
                      schema='gl.group')


# noinspection PyPep8Naming
class gl_groups_rpts_02_archive(InformReflection):
    __table__ = Table('gl_groups_rpts_02_archive', server_utils.mysql_base.metadata,
                      schema='gl.group')


# noinspection PyPep8Naming
class major_group_01_static(InformReflection):
    __table__ = Table('major_group_01_static', server_utils.mysql_base.metadata,
                      schema='major.group')


# noinspection PyPep8Naming
class major_group_main_01_current(InformReflection):
    __table__ = Table('major_group_main_01_current', server_utils.mysql_base.metadata,
                      schema='major.group')


# noinspection PyPep8Naming
class major_group_main_02_archive(InformReflection):
    __table__ = Table('major_group_main_02_archive', server_utils.mysql_base.metadata,
                      schema='major.group')


# noinspection PyPep8Naming
class cntr_01_static(InformReflection):
    __table__ = Table('cntr_01_static', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_category_01_current(InformReflection):
    __table__ = Table('cntr_category_01_current', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_category_02_archive(InformReflection):
    __table__ = Table('cntr_category_02_archive', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_cmnts_01_current(InformReflection):
    __table__ = Table('cntr_cmnts_01_current', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_cmnts_02_archive(InformReflection):
    __table__ = Table('cntr_cmnts_02_archive', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_header_01_current(InformReflection):
    __table__ = Table('cntr_header_01_current', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_header_02_archive(InformReflection):
    __table__ = Table('cntr_header_02_archive', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_shipto_01_current(InformReflection):
    __table__ = Table('cntr_shipto_01_current', server_utils.mysql_base.metadata,
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
class cntr_shipto_02_archive(InformReflection):
    __table__ = Table('cntr_shipto_02_archive', server_utils.mysql_base.metadata,
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
class cntr_source_01_current(InformReflection):
    __table__ = Table('cntr_source_01_current', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class cntr_source_02_archive(InformReflection):
    __table__ = Table('cntr_source_02_archive', server_utils.mysql_base.metadata,
                      schema='price.contract')


# noinspection PyPep8Naming
class price_matrix_01_current(InformReflection):
    __table__ = Table('price_matrix_01_current', server_utils.mysql_base.metadata,
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
class price_matrix_02_archive(InformReflection):
    __table__ = Table('price_matrix_02_archive', server_utils.mysql_base.metadata,
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
class prod_line_01_static(InformReflection):
    __table__ = Table('prod_line_01_static', server_utils.mysql_base.metadata,
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_main_01_current(InformReflection):
    __table__ = Table('prod_line_main_01_current', server_utils.mysql_base.metadata,
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_main_02_archive(InformReflection):
    __table__ = Table('prod_line_main_02_archive', server_utils.mysql_base.metadata,
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_notes_01_current(InformReflection):
    __table__ = Table('prod_line_notes_01_current', server_utils.mysql_base.metadata,
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_line_notes_02_archive(InformReflection):
    __table__ = Table('prod_line_notes_02_archive', server_utils.mysql_base.metadata,
                      schema='prod.line')


# noinspection PyPep8Naming
class prod_01_static(InformReflection):
    __table__ = Table('prod_01_static', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_01_current(InformReflection):
    __table__ = Table('prod_assembly_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_02_archive(InformReflection):
    __table__ = Table('prod_assembly_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_notes_01_current(InformReflection):
    __table__ = Table('prod_assembly_notes_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_assembly_notes_02_archive(InformReflection):
    __table__ = Table('prod_assembly_notes_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_ext_po_cmnts_01_current(InformReflection):
    __table__ = Table('prod_ext_po_cmnts_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_ext_po_cmnts_02_archive(InformReflection):
    __table__ = Table('prod_ext_po_cmnts_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_general_01_current(InformReflection):
    __table__ = Table('prod_general_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_general_02_archive(InformReflection):
    __table__ = Table('prod_general_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_int_po_cmnts_01_current(InformReflection):
    __table__ = Table('prod_int_po_cmnts_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_int_po_cmnts_02_archive(InformReflection):
    __table__ = Table('prod_int_po_cmnts_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_keywords_01_current(InformReflection):
    __table__ = Table('prod_keywords_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_keywords_02_archive(InformReflection):
    __table__ = Table('prod_keywords_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_main_01_current(InformReflection):
    __table__ = Table('prod_main_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_main_02_archive(InformReflection):
    __table__ = Table('prod_main_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_option_01_current(InformReflection):
    __table__ = Table('prod_option_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_option_02_archive(InformReflection):
    __table__ = Table('prod_option_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_purch_01_current(InformReflection):
    __table__ = Table('prod_purch_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_purch_02_archive(InformReflection):
    __table__ = Table('prod_purch_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_replenishments_01_current(InformReflection):
    __table__ = Table('prod_replenishments_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_replenishments_02_archive(InformReflection):
    __table__ = Table('prod_replenishments_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_rollup_01_current(InformReflection):
    __table__ = Table('prod_rollup_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_rollup_02_archive(InformReflection):
    __table__ = Table('prod_rollup_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_so_ext_cmnts_01_current(InformReflection):
    __table__ = Table('prod_so_ext_cmnts_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_so_ext_cmnts_02_archive(InformReflection):
    __table__ = Table('prod_so_ext_cmnts_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_stats_01_current(InformReflection):
    __table__ = Table('prod_stats_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_stats_02_archive(InformReflection):
    __table__ = Table('prod_stats_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_substitute_01_current(InformReflection):
    __table__ = Table('prod_substitute_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_substitute_02_archive(InformReflection):
    __table__ = Table('prod_substitute_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_uom_v2_01_current(InformReflection):
    __table__ = Table('prod_uom_v2_01_current', server_utils.mysql_base.metadata,
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
class prod_uom_v2_02_archive(InformReflection):
    __table__ = Table('prod_uom_v2_02_archive', server_utils.mysql_base.metadata,
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
class prod_vend_01_current(InformReflection):
    __table__ = Table('prod_vend_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_vend_02_archive(InformReflection):
    __table__ = Table('prod_vend_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_whse_proc_01_current(InformReflection):
    __table__ = Table('prod_whse_proc_01_current', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class prod_whse_proc_02_archive(InformReflection):
    __table__ = Table('prod_whse_proc_02_archive', server_utils.mysql_base.metadata,
                      schema='product')


# noinspection PyPep8Naming
class shipto_01_static(InformReflection):
    __table__ = Table('shipto_01_static', server_utils.mysql_base.metadata,
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
class shipto_budget_01_current(InformReflection):
    __table__ = Table('shipto_budget_01_current', server_utils.mysql_base.metadata,
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
class shipto_budget_02_archive(InformReflection):
    __table__ = Table('shipto_budget_02_archive', server_utils.mysql_base.metadata,
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
class shipto_cust_01_current(InformReflection):
    __table__ = Table('shipto_cust_01_current', server_utils.mysql_base.metadata,
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
class shipto_cust_02_archive(InformReflection):
    __table__ = Table('shipto_cust_02_archive', server_utils.mysql_base.metadata,
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
class shipto_edi_01_current(InformReflection):
    __table__ = Table('shipto_edi_01_current', server_utils.mysql_base.metadata,
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
class shipto_edi_02_archive(InformReflection):
    __table__ = Table('shipto_edi_02_archive', server_utils.mysql_base.metadata,
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
class shipto_main_01_current(InformReflection):
    __table__ = Table('shipto_main_01_current', server_utils.mysql_base.metadata,
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
class shipto_main_02_archive(InformReflection):
    __table__ = Table('shipto_main_02_archive', server_utils.mysql_base.metadata,
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
class shipto_spec_instr_01_current(InformReflection):
    __table__ = Table('shipto_spec_instr_01_current', server_utils.mysql_base.metadata,
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
class shipto_spec_instr_02_archive(InformReflection):
    __table__ = Table('shipto_spec_instr_02_archive', server_utils.mysql_base.metadata,
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
class shipto_truck_01_current(InformReflection):
    __table__ = Table('shipto_truck_01_current', server_utils.mysql_base.metadata,
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
class shipto_truck_02_archive(InformReflection):
    __table__ = Table('shipto_truck_02_archive', server_utils.mysql_base.metadata,
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
class vend_01_static(InformReflection):
    __table__ = Table('vend_01_static', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_contact_01_current(InformReflection):
    __table__ = Table('vend_contact_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_contact_02_archive(InformReflection):
    __table__ = Table('vend_contact_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_general_01_current(InformReflection):
    __table__ = Table('vend_general_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_general_02_archive(InformReflection):
    __table__ = Table('vend_general_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_hist_01_current(InformReflection):
    __table__ = Table('vend_hist_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_hist_02_archive(InformReflection):
    __table__ = Table('vend_hist_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_main_01_current(InformReflection):
    __table__ = Table('vend_main_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_main_02_archive(InformReflection):
    __table__ = Table('vend_main_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_notes_01_current(InformReflection):
    __table__ = Table('vend_notes_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_notes_02_archive(InformReflection):
    __table__ = Table('vend_notes_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_purch_01_current(InformReflection):
    __table__ = Table('vend_purch_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_purch_02_archive(InformReflection):
    __table__ = Table('vend_purch_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_remit_vendors_01_current(InformReflection):
    __table__ = Table('vend_remit_vendors_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_remit_vendors_02_archive(InformReflection):
    __table__ = Table('vend_remit_vendors_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_source_01_current(InformReflection):
    __table__ = Table('vend_source_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_source_02_archive(InformReflection):
    __table__ = Table('vend_source_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_spec_inst_01_current(InformReflection):
    __table__ = Table('vend_spec_inst_01_current', server_utils.mysql_base.metadata,
                      schema='vm')


# noinspection PyPep8Naming
class vend_spec_inst_02_archive(InformReflection):
    __table__ = Table('vend_spec_inst_02_archive', server_utils.mysql_base.metadata,
                      schema='vm')


