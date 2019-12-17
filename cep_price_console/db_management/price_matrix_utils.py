from cep_price_console.utils.log_utils import debug, CustomAdapter
from sqlalchemy import and_, or_, func, literal, select
from sqlalchemy.sql import case, literal_column
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.sql.expression import union_all
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.types import DateTime, String
from cep_price_console.db_management.server_utils import mysql_session_maker
import logging
import datetime
import sqlparse

"""
Allow the user to limit the column output.
Format the header with customer information
Make the report printable with headers and footers and such
Fix the .bat upload that's taking place hourly
Find a solution for csvkit that doesn't require a full python install
Merge the contract upload tool with the unified uploader by adding contract features
Integrate the price matrix sherpa with the upload tool
    
Matrix Health Check Feature:
    Implement an error message if a future matrix entry is past or current.
    Report out expired matrix entries or entries that haven't been sold in some time

Current and Future Price Matrices:
    Right now, I'm lumping the two concepts together. This isn't good.
    Implement an error message if a future matrix entry is past or current.
    Each of these categories will have their own minimum level and price/cost coalesce results. 
 
How to address ShipTo variances?

How do I deal with non-min queries? The price or cost is repeated for each entry of the other row

Separate the output query by customer. I'm not sure if I should run each customer through the list generator separately
    and write the results to a spreadsheet, or filter the results by customer. 

    For each unique customer value:
        Subquery, filter by customer values, sort by product number
        Output to a new tab. 
        Tab name = customer number
        Header information? 
        
Make use of outlining for multiple price/cost entries
"""

logger = CustomAdapter(logging.getLogger(str(__name__)), None)
PY3 = str is not bytes
text = str
int_type = int
str_type = str
reflected = False
cust_shipto_combo_expansion = None

matrix_logic = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
                "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34",
                "35", "36", "37", "38", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63",
                "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75"]


class StringLiteral(String):
    """Teach SA how to literalize various things."""

    def literal_processor(self, dialect):
        super_processor = super(StringLiteral, self).literal_processor(dialect)

        def process(value):
            if isinstance(value, int_type):
                return text(value)
            if not isinstance(value, str_type):
                value = text(value)
            result = super_processor(value)
            if isinstance(result, bytes):
                result = result.decode(dialect.encoding)
            return result

        return process


# noinspection PyAbstractClass
@debug(lvl=logging.NOTSET, prefix='')
class LiteralDialect(DefaultDialect):
    colspecs = {
        # prevent various encoding explosions
        String: StringLiteral,
        # teach SA about how to literalize a datetime
        DateTime: StringLiteral,
        # don't format py2 long integers to NULL
        NullType: StringLiteral,
    }


# @debug(lvl=logging.NOTSET, prefix='')
def literalquery(statement):
    """NOTE: This is entirely insecure. DO NOT execute the resulting strings."""
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        statement = statement.statement
    compiled_statement = statement.compile(
        dialect=LiteralDialect(),
        compile_kwargs={'literal_binds': True},
    ).string
    # compiled_statement.replace("SELECT ", "SELECT\n").replace(", ", ",\n")
    return compiled_statement


# @debug(lvl=logging.NOTSET, prefix='')
def verbose_query(statement):
    for desc in statement.column_descriptions:
        name = desc.get('name').replace("'", "").replace('"', "")
        logger.log(logging.DEBUG, name)
    logger.log(logging.DEBUG, "Literal Query: \n" + sqlparse.format(
        literalquery(statement), reindent=True, keyword_case='upper'))
    logger.log(logging.DEBUG, "Beginning of Results" + "-" * 80)
    for line in statement:
        logger.log(logging.DEBUG, str(list(line)))
    logger.log(logging.DEBUG, "End of Results" + "-" * 80)


class MatrixSherpa(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 min_level=False,  # Retrieve only the max level found. If False, return all matches
                 qty_break=None,  # I don't know what do do about this one yet
                 expired=True,  # Use the eff/exp date to either include or exclude expired entities
                 current=True,  # Use the eff/exp date to either include or exclude current entities
                 future=True,  # Use the eff/exp date to either include or exclude future entities
                 return_mode="matrix",
                 cntr_num_list=None,
                 cust_num_shipto_combo_list=None,
                 cust_cat_list=None,
                 prod_num_list=None,
                 prod_line_list=None,
                 price_group_code_list=None,
                 prim_vend_num_list=None,
                 secondary_vend_num_list=None,
                 major_group_list=None):  # Done
        # start_time = datetime.datetime.now()
        self.session = mysql_session_maker()

        self.min_level = min_level
        self.qty_break = qty_break
        self.expired = expired
        self.current = current
        self.future = future

        if return_mode in ["all", "sales", "matrix", "sales_or_matrix"]:
            self.return_mode = return_mode
        else:
            raise ValueError

        # Step 2: Instantiate Matrix Entities and Factors
        self.cust_entity = CustEntity(session=self.session)
        self.cust_entity.add_factor(
            fact_class=CustShipToFactor,
            value_list=cust_num_shipto_combo_list
        )
        self.cust_entity.add_factor(
            fact_class=CntrNumFactor,
            value_list=cntr_num_list
        )
        self.cust_entity.add_factor(
            fact_class=CustCatFactor,
            value_list=cust_cat_list
        )
        self.cust_entity.set_unified_atomic_value_list()

        self.prod_entity = ProdEntity(session=self.session)
        self.prod_entity.add_factor(
            fact_class=ProdNumFactor,
            value_list=prod_num_list
        )
        self.prod_entity.add_factor(
            fact_class=ProdLineFactor,
            value_list=prod_line_list
        )
        self.prod_entity.add_factor(
            fact_class=PriceGroupFactor,
            value_list=price_group_code_list
        )
        self.prod_entity.add_factor(
            fact_class=PrimVendNumFactor,
            value_list=prim_vend_num_list
        )
        self.prod_entity.add_factor(
            fact_class=VendNumFactor,
            value_list=secondary_vend_num_list + list(set(prim_vend_num_list) - set(secondary_vend_num_list))
        )
        self.prod_entity.add_factor(
            fact_class=MajorGroupFactor,
            value_list=major_group_list
        )
        self.prod_entity.set_unified_atomic_value_list()

        self.price_matrix_query = self.get_matrix_query(price=True)
        self.cost_matrix_query = self.get_matrix_query(cost=True)

    @debug(lvl=logging.DEBUG, prefix='')
    def get_filtered_price_matrix(self, matrix_table, price, cost):
        column_list = None
        filter_list = None
        if matrix_table.__table__.name == "ARW_PRF_Mapping.price_matrix_future_01_current":
            period_str = "Future"
        elif matrix_table.__table__.name == "ARW_PRF_Mapping.price_matrix_01_current":
            period_str = "Current"
        else:
            raise ValueError

        if price:
            column_list = [
                func.concat(matrix_table.__table__.c.ID, literal("_{}".format(period_str))).label("Matrix_Combo_ID"),
                literal("{}".format(period_str)).label("Period"),
                matrix_table.__table__.c.ID.label("Sub_ID"),
                matrix_table.__table__.c.Level_Num.label("Level_Num"),
                matrix_table.__table__.c.Cntr_Num.label("Cntr_Num"),
                matrix_table.__table__.c.Cust_Num.label("Cust_Num"),
                matrix_table.__table__.c.Ship_To_Code.label("Ship_To_Code"),
                matrix_table.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
                matrix_table.__table__.c.Cust_Cat.label("Cust_Cat"),
                matrix_table.__table__.c.Prod_Num.label("Prod_Num"),
                matrix_table.__table__.c.Prod_Line.label("Prod_Line"),
                matrix_table.__table__.c.Price_Group_Code.label("Price_Group_Code"),
                matrix_table.__table__.c.Vend_Num.label("Vend_Num"),
                matrix_table.__table__.c.Major_Group.label("Major_Group"),
                matrix_table.__table__.c.Eff_Date.label("Eff_Date"),
                matrix_table.__table__.c.Exp_Date.label("Exp_Date"),
                matrix_table.__table__.c.Price_Net_Factor.label("Price_Net_Factor"),
                matrix_table.__table__.c.Price_Plus_Minus.label("Price_Plus_Minus"),
                matrix_table.__table__.c.Price_Pcnt_Dollar.label("Price_Pcnt_Dollar"),
                matrix_table.__table__.c.Price_CLN.label("Price_CLN")
            ]
            filter_list = [matrix_table.__table__.c.Price_Net_Factor.isnot(None)]
        elif cost:
            column_list = [
                func.concat(matrix_table.__table__.c.ID, literal("_{}".format(period_str))).label("Matrix_Combo_ID"),
                literal("{}".format(period_str)).label("Period"),
                matrix_table.__table__.c.ID.label("Sub_ID"),
                matrix_table.__table__.c.Level_Num.label("Level_Num"),
                matrix_table.__table__.c.Cntr_Num.label("Cntr_Num"),
                matrix_table.__table__.c.Cust_Num.label("Cust_Num"),
                matrix_table.__table__.c.Ship_To_Code.label("Ship_To_Code"),
                matrix_table.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
                matrix_table.__table__.c.Cust_Cat.label("Cust_Cat"),
                matrix_table.__table__.c.Prod_Num.label("Prod_Num"),
                matrix_table.__table__.c.Prod_Line.label("Prod_Line"),
                matrix_table.__table__.c.Price_Group_Code.label("Price_Group_Code"),
                matrix_table.__table__.c.Vend_Num.label("Vend_Num"),
                matrix_table.__table__.c.Major_Group.label("Major_Group"),
                matrix_table.__table__.c.Eff_Date.label("Eff_Date"),
                matrix_table.__table__.c.Exp_Date.label("Exp_Date"),
                matrix_table.__table__.c.Cost_Net_Factor.label("Cost_Net_Factor"),
                matrix_table.__table__.c.Cost_Plus_Minus.label("Cost_Plus_Minus"),
                matrix_table.__table__.c.Cost_Pcnt_Dollar.label("Cost_Pcnt_Dollar"),
                matrix_table.__table__.c.Cost_CLN.label("Cost_CLN")
            ]
            filter_list = [matrix_table.__table__.c.Cost_Net_Factor.isnot(None)]

        return_query = self.session.query(*column_list)

        for entity in (self.prod_entity, self.cust_entity):
            if entity.unified_atomic_value_list:
                for fact_obj in entity.factor_dict.values():
                    if fact_obj.unit != "Primary_Vend":
                        fact_filter = None
                        if fact_obj.unit != entity.atomic_unit:
                            if fact_obj.expanded_value_list:
                                fact_filter = or_(
                                    matrix_table.__table__.c[fact_obj.unit].in_(fact_obj.expanded_value_list),
                                    matrix_table.__table__.c[fact_obj.unit].is_(None),
                                    matrix_table.__table__.c[fact_obj.unit] == ""
                                )
                            else:
                                fact_filter = or_(
                                    matrix_table.__table__.c[fact_obj.unit].is_(None),
                                    matrix_table.__table__.c[fact_obj.unit] == ""
                                )
                        elif fact_obj.unit == entity.atomic_unit:
                            if entity.atomic_unit == "Cust_Num_ShipTo_Combo":
                                fact_filter = or_(
                                    matrix_table.Cust_Num_ShipTo_Combo.is_(None),
                                    matrix_table.Cust_Num_ShipTo_Combo == "",
                                    matrix_table.Cust_Num_ShipTo_Combo.in_(entity.unified_atomic_value_list)
                                )
                            else:
                                fact_filter = or_(
                                    matrix_table.__table__.c[fact_obj.unit].is_(None),
                                    matrix_table.__table__.c[fact_obj.unit] == "",
                                    matrix_table.__table__.c[entity.atomic_unit].in_(entity.unified_atomic_value_list)
                                )
                        filter_list.append(fact_filter)

        if not self.expired or not self.current or not self.future:
            date_filters = []
            if self.expired:
                date_filters.append(
                    and_(
                        or_(
                            and_(
                                matrix_table.__table__.c.Eff_Date <= datetime.date.today(),
                                matrix_table.__table__.c.Eff_Date != '0000-00-00'
                            ),
                            matrix_table.__table__.c.Eff_Date == '0000-00-00'
                        ),
                        matrix_table.__table__.c.Exp_Date <= datetime.date.today(),
                        matrix_table.__table__.c.Exp_Date != '0000-00-00'
                    )
                )

            if self.current:
                date_filters.append(
                    and_(
                        or_(
                            matrix_table.__table__.c.Eff_Date <= datetime.date.today(),
                            matrix_table.__table__.c.Eff_Date == '0000-00-00'
                        ),
                        or_(
                            matrix_table.__table__.c.Exp_Date >= datetime.date.today(),
                            matrix_table.__table__.c.Exp_Date == '0000-00-00'
                        )
                    )
                )
            if self.future:
                date_filters.append(
                    and_(matrix_table.__table__.c.Eff_Date >= datetime.date.today(),
                         matrix_table.__table__.c.Eff_Date != '0000-00-00',
                         or_(
                             matrix_table.__table__.c.Exp_Date >= datetime.date.today(),
                             matrix_table.__table__.c.Exp_Date == '0000-00-00')
                         )
                )
            if date_filters:
                if len(date_filters) == 1:
                    filter_list.append(*date_filters)
                elif len(date_filters) > 1:
                    filter_list.append(or_(*date_filters))

        if filter_list:
            return_query = return_query.filter(and_(*filter_list))

        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def get_filtered_current_price_matrix(self, price, cost):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return self.get_filtered_price_matrix(ARW_PRF_Mapping.price_matrix_01_current, price, cost)

    @debug(lvl=logging.NOTSET, prefix='')
    def get_filtered_future_price_matrix(self, price, cost):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return self.get_filtered_price_matrix(ARW_PRF_Mapping.price_matrix_future_01_current, price, cost)

    @debug(lvl=logging.NOTSET, prefix='')
    def price_matrix_combo_query(self, lvl_num, price, cost):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return union_all(
            self.get_filtered_current_price_matrix(price, cost).filter(
                ARW_PRF_Mapping.price_matrix_01_current.__table__.c.Level_Num == int(lvl_num)),
            self.get_filtered_future_price_matrix(price, cost).filter(
                ARW_PRF_Mapping.price_matrix_future_01_current.__table__.c.Level_Num == int(lvl_num))
        ).alias("Matrix_Combo")

    @debug(lvl=logging.NOTSET, prefix='')
    def sherpa_level_qry(self, lvl_num, price, cost):
        filtered_matrix_qry = self.price_matrix_combo_query(lvl_num=lvl_num, price=price, cost=cost)

        prod_entity_query, prod_entity_col_keys = self.prod_entity.entity_level_qry(lvl_num)
        prod_entity_subquery = prod_entity_query.subquery()
        self.__class__.logger.log(logging.NOTSET, "Prod Entity Col Keys: {}".format(str(prod_entity_col_keys)))

        prod_join_tuples = []
        for entity_name in prod_entity_col_keys:
            prod_join_tuples.append(prod_entity_subquery.c[entity_name] == filtered_matrix_qry.c[entity_name])

        cust_entity_query, cust_entity_col_keys = self.cust_entity.entity_level_qry(lvl_num)
        cust_entity_subquery = cust_entity_query.subquery()
        self.__class__.logger.log(logging.NOTSET, "Cust Entity Col Keys: {}".format(str(cust_entity_col_keys)))

        cust_join_tuples = []
        for entity_name in cust_entity_col_keys:
            cust_join_tuples.append(cust_entity_subquery.c[entity_name] == filtered_matrix_qry.c[entity_name])

        col_list = []
        for col in filtered_matrix_qry.c:
            col_list.append(col.label(col.name))

        return_query = self.session.query(
            *col_list,
            cust_entity_subquery.c["Cust_Num_ShipTo_Combo"].label(
                "Cust_Num_ShipTo_Combo_Selection"),
            prod_entity_subquery.c["Prod_Num"].label("Prod_Num_Selection"),
            prod_entity_subquery.c.C1_Cost.label("C1_Cost"),
            prod_entity_subquery.c.C2_Cost.label("C2_Cost"),
            prod_entity_subquery.c.C3_Cost.label("C3_Cost"),
            prod_entity_subquery.c.C4_Cost.label("C4_Cost"),
            prod_entity_subquery.c.C5_Cost.label("C5_Cost"),
            prod_entity_subquery.c.C6_Cost.label("C6_Cost"),
            prod_entity_subquery.c.C7_Cost.label("C7_Cost"),
            prod_entity_subquery.c.L1_Price.label("L1_Price"),
            prod_entity_subquery.c.L2_Price.label("L2_Price"),
            prod_entity_subquery.c.L3_Price.label("L3_Price"),
            prod_entity_subquery.c.L4_Price.label("L4_Price"),
            prod_entity_subquery.c.Fut_Price.label("Fut_Price"),
            prod_entity_subquery.c.Fut_Price_Column.label("Fut_Price_Column"),
            prod_entity_subquery.c.Fut_Price_Date.label("Fut_Price_Date")
        )
        if prod_join_tuples:
            self.__class__.logger.log(logging.NOTSET, "Prod Join Tuples Used")
            return_query = return_query.join(
                prod_entity_subquery, and_(
                    *prod_join_tuples
                )
            )
        if cust_join_tuples:
            self.__class__.logger.log(logging.NOTSET, "Cust Join Tuples Used")
            return_query = return_query.join(
                cust_entity_subquery, and_(
                    *cust_join_tuples
                )
            )
        # verbose_query(return_query)
        return return_query

    # noinspection PyUnresolvedReferences
    @debug(lvl=logging.NOTSET, prefix='')
    def get_matrix_query(self, price=False, cost=False):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        start_time = datetime.datetime.now()

        if (price and cost) or (not price and not cost):
            raise ValueError

        query = union_all(*[self.sherpa_level_qry(level, price, cost) for level in list(matrix_logic)]).alias()

        query_list = [
            query.c.Matrix_Combo_ID.label("Matrix_Combo_ID"),
            query.c.Period.label("Period"),
            query.c.Sub_ID.label("Sub_ID"),
            query.c.Level_Num.label("Level_Num"),
            query.c.Cntr_Num.label("Cntr_Num"),
            query.c.Cust_Num.label("Cust_Num"),
            query.c.Ship_To_Code.label("Ship_To_Code"),
            query.c.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
            query.c.Cust_Cat.label("Cust_Cat"),
            query.c.Prod_Num.label("Prod_Num"),
            query.c.Prod_Line.label("Prod_Line"),
            query.c.Price_Group_Code.label("Price_Group_Code"),
            query.c.Vend_Num.label("Vend_Num"),
            query.c.Major_Group.label("Major_Group")
        ]

        if price:
            query_list.extend([
                query.c.Price_Net_Factor.label("Price_Net_Factor"),
                query.c.Price_Plus_Minus.label("Price_Plus_Minus"),
                query.c.Price_Pcnt_Dollar.label("Price_Pcnt_Dollar"),
                query.c.Price_CLN.label("Price_CLN"),
                func.IF(query.c.Price_Net_Factor.is_(None),
                        None,
                        case([(func.trim(query.c.Price_Pcnt_Dollar) == "%",
                               ((1 + (func.IF(query.c.Price_Net_Factor.is_(None),
                                              None,
                                              case([
                                                  (func.trim(query.c.Price_Pcnt_Dollar) == "%",
                                                   (func.IF(query.c.Price_Net_Factor.is_(None),
                                                            None,
                                                            case([
                                                                (func.trim(
                                                                    query.c.Price_Plus_Minus) == "-",
                                                                 (query.c.Price_Net_Factor * -1))],
                                                                else_=query.c.Price_Net_Factor
                                                            ) / 100)))],
                                                  else_=(func.IF(query.c.Price_Net_Factor.is_(None),
                                                                 None,
                                                                 case([
                                                                     (func.trim(
                                                                         query.c.Price_Plus_Minus) == "-",
                                                                      (query.c.Price_Net_Factor * -1))],
                                                                     else_=query.c.Price_Net_Factor
                                                                 ))
                                                         )
                                              )))) * (func.IF(query.c.Price_Net_Factor.is_(None),
                                                              None,
                                                              case([(func.upper(
                                                                  func.trim(query.c.Price_CLN)) == "C1",
                                                                     query.c.C1_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "C2",
                                                                     query.c.C2_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "C3",
                                                                     query.c.C3_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "C4",
                                                                     query.c.C4_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "C5",
                                                                     query.c.C5_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "C6",
                                                                     query.c.C6_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "C7",
                                                                     query.c.C7_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "L1",
                                                                     query.c.L1_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "L2",
                                                                     query.c.L2_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "L3",
                                                                     query.c.L3_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "L4",
                                                                     query.c.L4_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Price_CLN)) == "N", literal(0))],
                                                                   else_=None)))))],
                             else_=((func.IF(query.c.Price_Net_Factor.is_(None),
                                             None,
                                             case([
                                                 (func.trim(query.c.Price_Pcnt_Dollar) == "%",
                                                  (func.IF(query.c.Price_Net_Factor.is_(None),
                                                           None,
                                                           case([
                                                               (func.trim(
                                                                   query.c.Price_Plus_Minus) == "-",
                                                                (query.c.Price_Net_Factor * -1))],
                                                               else_=query.c.Price_Net_Factor
                                                           ) / 100)))],
                                                 else_=(func.IF(query.c.Price_Net_Factor.is_(None),
                                                                None,
                                                                case([
                                                                    (func.trim(
                                                                        query.c.Price_Plus_Minus) == "-",
                                                                     (query.c.Price_Net_Factor * -1))],
                                                                    else_=query.c.Price_Net_Factor
                                                                ))
                                                        )
                                             ))) + (func.IF(query.c.Price_Net_Factor.is_(None),
                                                            None,
                                                            case([(func.upper(
                                                                func.trim(query.c.Price_CLN)) == "C1",
                                                                   query.c.C1_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "C2",
                                                                   query.c.C2_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "C3",
                                                                   query.c.C3_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "C4",
                                                                   query.c.C4_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "C5",
                                                                   query.c.C5_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "C6",
                                                                   query.c.C6_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "C7",
                                                                   query.c.C7_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "L1",
                                                                   query.c.L1_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "L2",
                                                                   query.c.L2_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "L3",
                                                                   query.c.L3_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "L4",
                                                                   query.c.L4_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Price_CLN)) == "N", literal(0))],
                                                                 else_=None)))))
                        ).label("Price_Net")
            ])
        elif cost:
            query_list.extend([
                query.c.Cost_Net_Factor.label("Cost_Net_Factor"),
                query.c.Cost_Plus_Minus.label("Cost_Plus_Minus"),
                query.c.Cost_Pcnt_Dollar.label("Cost_Pcnt_Dollar"),
                query.c.Cost_CLN.label("Cost_CLN"),
                func.IF(query.c.Cost_Net_Factor.is_(None),
                        None,
                        case([(func.trim(query.c.Cost_Pcnt_Dollar) == "%",
                               ((1 + (func.IF(query.c.Cost_Net_Factor.is_(None),
                                              None,
                                              case([
                                                  (func.trim(query.c.Cost_Pcnt_Dollar) == "%",
                                                   (func.IF(query.c.Cost_Net_Factor.is_(None),
                                                            None,
                                                            case([
                                                                (func.trim(
                                                                    query.c.Cost_Plus_Minus) == "-",
                                                                 (query.c.Cost_Net_Factor * -1))],
                                                                else_=query.c.Cost_Net_Factor
                                                            ) / 100)))],
                                                  else_=(func.IF(query.c.Cost_Net_Factor.is_(None),
                                                                 None,
                                                                 case([
                                                                     (func.trim(
                                                                         query.c.Cost_Plus_Minus) == "-",
                                                                      (query.c.Cost_Net_Factor * -1))],
                                                                     else_=query.c.Cost_Net_Factor
                                                                 ))
                                                         )
                                              )))) * (func.IF(query.c.Cost_Net_Factor.is_(None),
                                                              None,
                                                              case([(func.upper(
                                                                  func.trim(query.c.Cost_CLN)) == "C1",
                                                                     query.c.C1_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "C2",
                                                                     query.c.C2_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "C3",
                                                                     query.c.C3_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "C4",
                                                                     query.c.C4_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "C5",
                                                                     query.c.C5_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "C6",
                                                                     query.c.C6_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "C7",
                                                                     query.c.C7_Cost),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "L1",
                                                                     query.c.L1_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "L2",
                                                                     query.c.L2_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "L3",
                                                                     query.c.L3_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "L4",
                                                                     query.c.L4_Price),
                                                                    (func.upper(func.trim(
                                                                        query.c.Cost_CLN)) == "N", literal(0))],
                                                                   else_=None)))))],
                             else_=((func.IF(query.c.Cost_Net_Factor.is_(None),
                                             None,
                                             case([
                                                 (func.trim(query.c.Cost_Pcnt_Dollar) == "%",
                                                  (func.IF(query.c.Cost_Net_Factor.is_(None),
                                                           None,
                                                           case([
                                                               (func.trim(
                                                                   query.c.Cost_Plus_Minus) == "-",
                                                                (query.c.Cost_Net_Factor * -1))],
                                                               else_=query.c.Cost_Net_Factor
                                                           ) / 100)))],
                                                 else_=(func.IF(query.c.Cost_Net_Factor.is_(None),
                                                                None,
                                                                case([
                                                                    (func.trim(
                                                                        query.c.Cost_Plus_Minus) == "-",
                                                                     (query.c.Cost_Net_Factor * -1))],
                                                                    else_=query.c.Cost_Net_Factor
                                                                ))
                                                        )
                                             ))) + (func.IF(query.c.Cost_Net_Factor.is_(None),
                                                            None,
                                                            case([(func.upper(
                                                                func.trim(query.c.Cost_CLN)) == "C1",
                                                                   query.c.C1_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "C2",
                                                                   query.c.C2_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "C3",
                                                                   query.c.C3_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "C4",
                                                                   query.c.C4_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "C5",
                                                                   query.c.C5_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "C6",
                                                                   query.c.C6_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "C7",
                                                                   query.c.C7_Cost),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "L1",
                                                                   query.c.L1_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "L2",
                                                                   query.c.L2_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "L3",
                                                                   query.c.L3_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "L4",
                                                                   query.c.L4_Price),
                                                                  (func.upper(func.trim(
                                                                      query.c.Cost_CLN)) == "N", literal(0))],
                                                                 else_=None)))))
                        ).label("Cost_Net"),
            ])

        query_list.extend([
            query.c.Eff_Date.label("Eff_Date"),
            query.c.Exp_Date.label("Exp_Date"),
            query.c.Cust_Num_ShipTo_Combo_Selection.label("Cust_Num_ShipTo_Combo_Selection"),
            query.c.Prod_Num_Selection.label("Prod_Num_Selection"),
            query.c.C1_Cost.label("C1_Cost"),
            query.c.C2_Cost.label("C2_Cost"),
            query.c.C3_Cost.label("C3_Cost"),
            query.c.C4_Cost.label("C4_Cost"),
            query.c.C5_Cost.label("C5_Cost"),
            query.c.C6_Cost.label("C6_Cost"),
            query.c.C7_Cost.label("C7_Cost"),
            query.c.L1_Price.label("L1_Price"),
            query.c.L2_Price.label("L2_Price"),
            query.c.L3_Price.label("L3_Price"),
            query.c.L4_Price.label("L4_Price"),
            query.c.Fut_Price.label("Fut_Price"),
            query.c.Fut_Price_Column.label("Fut_Price_Column"),
            query.c.Fut_Price_Date.label("Fut_Price_Date")
        ])
        return_query = self.session.query(
            *query_list
        )  # .outerjoin(
        #     ARW_PRF_Mapping.prod_main_01_current.__table__,
        #     ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num ==
        #     query.c.Prod_Num_Selection
        # )
        # for _ in return_query.all():
        #     self.__class__.logger.log(logging.DEBUG, str(_))
        self.__class__.logger.log(logging.DEBUG, "Query Result Time: {}".format(datetime.datetime.now() - start_time))
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def get_cust_prod_crossjoin_query(self):
        if self.cust_entity.factor_dict["Cust_Num_ShipTo_Combo"].unit_value_list:
            cust_subquery = self.session.query(self.cust_entity.entity_expansion_query).filter(
                literal_column("Cust_Expansion.Cust_Num_ShipTo_Combo").in_(
                    self.cust_entity.factor_dict["Cust_Num_ShipTo_Combo"].unit_value_list)
            ).subquery()
            return_query = self.session.query(
                cust_subquery,
                self.prod_entity.entity_expansion_query
            )
        else:
            return_query = self.session.query(
                self.cust_entity.entity_expansion_query,
                self.prod_entity.entity_expansion_query
            )

        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.DEBUG, prefix='')
    def get_price_query(self):
        subquery = self.price_matrix_query.subquery("price_subquery")
        if self.min_level:
            return_query = self.session.query(
                subquery.c.Matrix_Combo_ID.label("Matrix_Combo_ID"),
                subquery.c.Period.label("Period"),
                subquery.c.Sub_ID.label("Sub_ID"),
                func.min(subquery.c.Level_Num).label("Level_Num"),
                subquery.c.Price_Net.label("Price_Net"),
                subquery.c.Eff_Date.label("Eff_Date"),
                subquery.c.Exp_Date.label("Exp_Date"),
                subquery.c.Cust_Num_ShipTo_Combo_Selection.label("Cust_Num_ShipTo_Combo_Selection"),
                subquery.c.Prod_Num_Selection.label("Prod_Num_Selection"),
            ).group_by(
                subquery.c.Cust_Num_ShipTo_Combo_Selection,
                subquery.c.Prod_Num_Selection
            )
        else:
            return_query = self.session.query(
                subquery.c.Matrix_Combo_ID.label("Matrix_Combo_ID"),
                subquery.c.Period.label("Period"),
                subquery.c.Sub_ID.label("Sub_ID"),
                subquery.c.Level_Num.label("Level_Num"),
                subquery.c.Price_Net.label("Price_Net"),
                subquery.c.Eff_Date.label("Eff_Date"),
                subquery.c.Exp_Date.label("Exp_Date"),
                subquery.c.Cust_Num_ShipTo_Combo_Selection.label("Cust_Num_ShipTo_Combo_Selection"),
                subquery.c.Prod_Num_Selection.label("Prod_Num_Selection"),
            )
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.DEBUG, prefix='')
    def get_cost_query(self):
        subquery = self.cost_matrix_query.subquery("cost_subquery")
        if self.min_level:
            return_query = self.session.query(
                subquery.c.Matrix_Combo_ID.label("Matrix_Combo_ID"),
                subquery.c.Period.label("Period"),
                subquery.c.Sub_ID.label("Sub_ID"),
                func.min(subquery.c.Level_Num).label("Level_Num"),
                subquery.c.Cost_Net.label("Cost_Net"),
                subquery.c.Eff_Date.label("Eff_Date"),
                subquery.c.Exp_Date.label("Exp_Date"),
                subquery.c.Cust_Num_ShipTo_Combo_Selection.label("Cust_Num_ShipTo_Combo_Selection"),
                subquery.c.Prod_Num_Selection.label("Prod_Num_Selection"),
            ).group_by(
                subquery.c.Cust_Num_ShipTo_Combo_Selection,
                subquery.c.Prod_Num_Selection
            )
        else:
            return_query = self.session.query(
                subquery.c.Matrix_Combo_ID.label("Matrix_Combo_ID"),
                subquery.c.Period.label("Period"),
                subquery.c.Sub_ID.label("Sub_ID"),
                subquery.c.Level_Num.label("Level_Num"),
                subquery.c.Cost_Net.label("Cost_Net"),
                subquery.c.Eff_Date.label("Eff_Date"),
                subquery.c.Exp_Date.label("Exp_Date"),
                subquery.c.Cust_Num_ShipTo_Combo_Selection.label("Cust_Num_ShipTo_Combo_Selection"),
                subquery.c.Prod_Num_Selection.label("Prod_Num_Selection"),
            )
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.DEBUG, prefix='')
    def get_min_sales_days_subquery(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        cust_prod_crossjoin_subquery = self.get_cust_prod_crossjoin_query().subquery()

        min_sales_days_subquery = self.session.query(
            cust_prod_crossjoin_subquery,
            func.min(ARW_PRF_Mapping.days_since_last_sale_01_current.__table__.c.Days_Since_Last_Purch).label(
                "Days_Since_Last_Purch")
        ).outerjoin(
            ARW_PRF_Mapping.days_since_last_sale_01_current.__table__, and_(
                ARW_PRF_Mapping.days_since_last_sale_01_current.__table__.c.Prod_Num ==
                cust_prod_crossjoin_subquery.c.Prod_Num,
                ARW_PRF_Mapping.days_since_last_sale_01_current.Cust_Num ==
                cust_prod_crossjoin_subquery.c.Cust_Num
            )
        ).group_by(
            cust_prod_crossjoin_subquery.c.Prod_Num,
            cust_prod_crossjoin_subquery.c.Cust_Num_ShipTo_Combo
        ).subquery()
        return min_sales_days_subquery

    @debug(lvl=logging.DEBUG, prefix='')
    def final_return_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        price_subquery = self.get_price_query().subquery("filtered_price_subquery")
        cost_subquery = self.get_cost_query().subquery("filtered_cost_subquery")
        min_sales_days_subquery = self.get_min_sales_days_subquery()

        matrix_filter = or_(
            and_(
                price_subquery.c.Level_Num.isnot(None),
                or_(
                    cost_subquery.c.Level_Num.is_(None),
                    cost_subquery.c.Level_Num.isnot(None)
                )
            ),
            and_(
                price_subquery.c.Level_Num.is_(None),
                cost_subquery.c.Level_Num.isnot(None)
            )
        )
        sales_filter = min_sales_days_subquery.c.Days_Since_Last_Purch.isnot(None)

        filter_obj = None
        if self.return_mode == "matrix":
            filter_obj = matrix_filter
        elif self.return_mode == "sales":
            filter_obj = sales_filter
        elif self.return_mode == "sales_or_matrix":
            filter_obj = or_(matrix_filter, sales_filter)

        dates_query = self.session.query(
            min_sales_days_subquery,
            price_subquery.c.Matrix_Combo_ID.label("Price_Matrix_Combo_ID"),
            price_subquery.c.Level_Num.label("Price_Level_Num"),
            price_subquery.c.Eff_Date.label("Price_Eff_Date"),
            price_subquery.c.Exp_Date.label("Price_Exp_Date"),
            func.coalesce(price_subquery.c.Price_Net,
                          ARW_PRF_Mapping.prod_main_01_current.__table__.c.L1_Price).label("Net_Price"),
            cost_subquery.c.Matrix_Combo_ID.label("Cost_Matrix_Combo_ID"),
            cost_subquery.c.Level_Num.label("Cost_Level_Num"),
            cost_subquery.c.Eff_Date.label("Cost_Eff_Date"),
            cost_subquery.c.Exp_Date.label("Cost_Exp_Date"),
            func.coalesce(cost_subquery.c.Cost_Net,
                          ARW_PRF_Mapping.prod_main_01_current.__table__.c.C1_Cost).label("Net_Cost")
        ).outerjoin(
            ARW_PRF_Mapping.prod_main_01_current.__table__,
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num ==
            min_sales_days_subquery.c.Prod_Num
        ).outerjoin(
            price_subquery, and_(
                min_sales_days_subquery.c.Prod_Num ==
                price_subquery.c.Prod_Num_Selection,
                min_sales_days_subquery.c.Cust_Num_ShipTo_Combo ==
                price_subquery.c.Cust_Num_ShipTo_Combo_Selection,
            )
        ).outerjoin(
            cost_subquery, and_(
                min_sales_days_subquery.c.Prod_Num ==
                cost_subquery.c.Prod_Num_Selection,
                min_sales_days_subquery.c.Cust_Num_ShipTo_Combo ==
                cost_subquery.c.Cust_Num_ShipTo_Combo_Selection,
            )
        )

        if filter_obj is not None:
            dates_query = dates_query.filter(filter_obj)

        # for _ in dates_query.all():
        #     self.__class__.logger.log(logging.DEBUG, str(_))

        return dates_query.order_by(min_sales_days_subquery.c.Cust_Num_ShipTo_Combo,
                                    min_sales_days_subquery.c.Prod_Num,
                                    price_subquery.c.Level_Num,
                                    cost_subquery.c.Level_Num
                                    )


class Entity(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    atomic_unit = None

    @debug(lvl=logging.NOTSET, prefix="")
    def __init__(self, session):
        self.session = session
        self.unified_atomic_value_list = None
        self.entity_expansion_query = None
        self.set_entity_expansion_query()
        self.atomic_unit = self.__class__.atomic_unit
        self.atomic_unit_col = self.entity_expansion_query.c[self.atomic_unit]
        self.factor_dict = {}

    @debug(lvl=logging.NOTSET, prefix='')
    def set_entity_expansion_query(self):
        raise NotImplementedError

    @debug(lvl=logging.NOTSET, prefix="")
    def add_factor(self, fact_class, value_list):
        fact_instance = fact_class(entity=self, session=self.session, value_list=value_list)
        self.factor_dict[fact_instance.unit] = fact_instance

    @debug(lvl=logging.NOTSET, prefix='')
    def set_unified_atomic_value_list(self):
        fact_set = None
        for fact in self.factor_dict.values():
            MatrixFactor.logger.log(logging.DEBUG,
                                    "{} atomic_value_list: {}".format(fact.unit, fact.atomic_value_list))
            if fact.atomic_value_list is not None:
                if fact_set is None:
                    fact_set = set(fact.atomic_value_list)
                else:
                    fact_set = fact_set.intersection(set(fact.atomic_value_list))
                    MatrixFactor.logger.log(logging.DEBUG,
                                            "Fact_set: {}".format(list(fact_set)))
            else:
                MatrixFactor.logger.log(logging.DEBUG,
                                        "Fact_set is None")
        if self.factor_dict.get("Primary_Vend") is not None:
            self.factor_dict.pop("Primary_Vend")

        self.unified_atomic_value_list = None
        if fact_set is not None:
            fact_list = list(fact_set)
            if fact_list:
                self.unified_atomic_value_list = fact_list

        MatrixFactor.logger.log(logging.DEBUG,
                                "{} unified_atomic_value_list: {}".format(
                                    self.atomic_unit, self.unified_atomic_value_list))

        self.set_entity_expansion_query()
        self.atomic_unit_col = self.entity_expansion_query.c[self.atomic_unit]

        for fact in self.factor_dict.values():
            # noinspection PyProtectedMember
            self.__class__.logger.log(logging.NOTSET, "Factor Unit: {}".format(fact.unit))
            # noinspection PyProtectedMember
            fact.expanded_value_list = set([row._asdict()[fact.unit] for row in fact.atomic_to_unit_query().all()])
            # fact.set_atomic_to_unit_subquery()

    @debug(lvl=logging.NOTSET, prefix='')
    def entity_level_qry(self, lvl_num):
        entity_col_dict = {}
        entity_join_list = []
        add_entity_key = False
        for factor in self.factor_dict.values():
            if lvl_num in factor.lvl_list:
                if self.atomic_unit != factor.unit:
                    if factor.unit not in self.entity_expansion_query.c:
                        if factor.unit == "Cntr_Num":
                            cntr_column, cntr_join_tuple = factor.get_join_tuple()
                            entity_col_dict[factor.unit] = cntr_column
                            entity_join_list.append(cntr_join_tuple)
                        else:
                            entity_col_dict[factor.unit] = factor.unit_col
                            entity_join_list.append(factor.get_join_tuple())
                    else:
                        entity_col_dict[factor.unit] = self.entity_expansion_query.c[factor.unit]
                else:
                    add_entity_key = True
        if entity_col_dict.values():
            return_query = self.session.query(
                self.entity_expansion_query,
                *entity_col_dict.values()
            )
        else:
            return_query = self.session.query(
                self.entity_expansion_query
            )

        if entity_join_list:
            for join_tuple in entity_join_list:
                return_query = return_query.join(join_tuple)
        entity_col_keys = list(entity_col_dict.keys())
        if add_entity_key:
            entity_col_keys.append(self.atomic_unit)
        # verbose_query(return_query)
        return return_query, entity_col_keys


class CustEntity(Entity):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    atomic_unit = "Cust_Num_ShipTo_Combo"

    @debug(lvl=logging.NOTSET, prefix='')
    def set_entity_expansion_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        ship_to = self.session.query(
            ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.Cust_Num.label("Cust_Num"),
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.Ship_To_Code.label("Ship_To_Code"),
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.ShipTo_Pricing_Cat.label("Cust_Cat")
        )

        cust_main = self.session.query(
            ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Num.label("Cust_Num"),
            literal("_All").label("Ship_To_Code"),
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Cat.label("Cust_Cat")
        )

        if self.unified_atomic_value_list is not None:
            ship_to = ship_to.filter(
                ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo.in_(self.unified_atomic_value_list))
            cust_main = cust_main.filter(
                ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.in_(self.unified_atomic_value_list))

        self.entity_expansion_query = select([union_all(ship_to, cust_main).alias()]).alias("Cust_Expansion")


class ProdEntity(Entity):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    atomic_unit = "Prod_Num"

    @debug(lvl=logging.NOTSET, prefix='')
    def set_entity_expansion_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return_query = select([
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num.label("Prod_Num"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Line.label("Prod_Line"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Price_Group_Code.label("Price_Group_Code"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C1_Cost.label("C1_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C2_Cost.label("C2_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C3_Cost.label("C3_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C4_Cost.label("C4_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C5_Cost.label("C5_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C6_Cost.label("C6_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.C7_Cost.label("C7_Cost"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.L1_Price.label("L1_Price"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.L2_Price.label("L2_Price"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.L3_Price.label("L3_Price"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.L4_Price.label("L4_Price"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Fut_Price.label("Fut_Price"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Fut_Price_Column.label("Fut_Price_Column"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Fut_Price_Date.label("Fut_Price_Date")
        ])
        if self.unified_atomic_value_list is not None:
            return_query = return_query.where(
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num.in_(self.unified_atomic_value_list)
            )
        self.entity_expansion_query = return_query.alias("Prod_Expansion")


class MatrixFactor(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    combined_fact_dict = {}
    selection_cartesian_subquery = None
    unit = None
    unit_col = None
    lvl_list = None

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 entity,
                 session,
                 value_list,
                 col_set=True):
        self.entity = entity
        self.unit = self.__class__.unit
        self.atomic_unit = self.entity.atomic_unit
        if col_set:
            self.unit_col = self.__class__.unit_col
            # self.atomic_unit_col = self.entity.atomic_unit_col
        self.lvl_list = self.__class__.lvl_list
        self.session = session
        self.expanded_value_list = None
        self.__unit_value_list = None
        self.__atomic_value_list = None
        self.atomic_to_unit_subquery = None
        self.unit_value_list = value_list

    # region unit_value_list ###########################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def unit_value_list(self):
        return self.__unit_value_list

    @unit_value_list.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def unit_value_list(self, value):
        if value:
            self.__unit_value_list = value
            # noinspection PyProtectedMember
            self.__atomic_value_list = [
                row._asdict()[self.atomic_unit] for row in self.unit_to_atomic_query().all()]
            MatrixFactor.logger.log(logging.DEBUG, str(self.__atomic_value_list))
        else:
            self.__unit_value_list = None
            self.__atomic_value_list = None

    # endregion ########################################################################################################

    # region atomic_value_list ####################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def atomic_value_list(self):
        return self.__atomic_value_list

    # endregion ########################################################################################################

    @debug(lvl=logging.NOTSET, prefix='')
    def unit_to_atomic_query(self):
        return_query = self.expansion_query()
        if self.unit_value_list is not None:
            return_query = return_query.filter(
                self.entity.entity_expansion_query.c[self.unit].in_(self.unit_value_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def atomic_to_unit_query(self):
        return_query = self.expansion_query()
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        raise NotImplementedError

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class CntrNumFactor(MatrixFactor):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Cntr_Num"  # Don't know if I need this
    unit_col = None
    lvl_list = ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "63"]

    @debug(lvl=logging.NOTSET, prefix='')
    def unit_to_atomic_query(self):
        return_query = self.expansion_query()
        if self.unit_value_list is not None:
            return_query = return_query.filter(
                literal_column("Cntr_Expansion.Cntr_Num").in_(self.unit_value_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        expansion = union_all(
            self.get_cntr_ship_to_combo(),
            self.get_cntr_null_ship_to_combo(),
            self.get_cntr_all_cust_flag(),
            self.get_cntr_category()
        ).alias("Cntr_Expansion")

        return self.session.query(
            expansion.c.Cntr_Num.label("Cntr_Num"),
            expansion.c.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        expansion_subquery = self.expansion_query().subquery()
        return expansion_subquery.c.Cntr_Num, (
            expansion_subquery,
            expansion_subquery.c.Cust_Num_ShipTo_Combo ==
            self.entity.entity_expansion_query.c.Cust_Num_ShipTo_Combo
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_cntr_ship_to_combo(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        # Step 1: Customer/Ship-To Combos
        # noinspection PyPep8,PyComparisonWithNone
        filter_list = [
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.All_Cust_Flag == 'N',
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Ship_To_Nums.isnot(None),
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Ship_To_Nums != "",
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Cust_Nums.isnot(None),
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Cust_Nums != ""
        ]
        if self.entity.unified_atomic_value_list:
            filter_list.append(
                ARW_PRF_Mapping.cntr_shipto_01_current.Cust_Num_ShipTo_Combo.in_(self.entity.unified_atomic_value_list))

        return_query = self.session.query(
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num.label("Cntr_Num"),
            ARW_PRF_Mapping.cntr_shipto_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        ).outerjoin(
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__,
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num ==
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Cntr_Num
        ).filter(and_(*filter_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def get_cntr_null_ship_to_combo(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        # Step 2: Customers with Null Ship-Tos
        # noinspection PyPep8,PyComparisonWithNone
        filter_list = [
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.All_Cust_Flag == 'N',
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Cust_Nums.isnot(None),
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Cust_Nums != "",
            or_(
                ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Ship_To_Nums.is_(None),
                ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Ship_To_Nums == ""
            )
        ]
        if self.entity.unified_atomic_value_list:
            filter_list.append(
                ARW_PRF_Mapping.cntr_shipto_01_current.Cust_Num_ShipTo_Combo.in_(self.entity.unified_atomic_value_list))

        return_query = self.session.query(
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num.label("Cntr_Num"),
            ARW_PRF_Mapping.cntr_shipto_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        ).outerjoin(
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__,
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num ==
            ARW_PRF_Mapping.cntr_shipto_01_current.__table__.c.Cntr_Num
        ).filter(and_(*filter_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def get_cntr_all_cust_flag(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        # Step 3: All Customer Flags
        filter_list = [ARW_PRF_Mapping.cntr_header_01_current.__table__.c.All_Cust_Flag == 'Y']
        if self.entity.unified_atomic_value_list:
            filter_list.append(
                ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.in_(self.entity.unified_atomic_value_list))

        return_query = self.session.query(
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num.label("Cntr_Num"),
            ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        ).filter(and_(*filter_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def get_cntr_category(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        # Step 2: Contract Categories
        return_query = self.session.query(
            ARW_PRF_Mapping.cntr_category_01_current.__table__.c.Cntr_Num.label("Cntr_Num"),
            ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        ).join(
            ARW_PRF_Mapping.cust_master_01_current.__table__,
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Cat ==
            ARW_PRF_Mapping.cntr_category_01_current.__table__.c.Cust_Cat
        )
        if self.entity.unified_atomic_value_list:
            return_query = return_query.filter(
                ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.in_(self.entity.unified_atomic_value_list))

        # verbose_query(return_query)
        return return_query


class CustShipToFactor(MatrixFactor):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Cust_Num_ShipTo_Combo"
    unit_col = None
    lvl_list = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
                "18", "19", "20", "21", "22", "23", "24", "25", "26", "27"]

    @debug(lvl=logging.NOTSET, prefix='')
    def unit_to_atomic_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        atomic_value_list = list(self.unit_value_list)

        self.__class__.logger.log(logging.DEBUG, "Initial Filter List: {}".format(self.unit_value_list))

        cust_shipto = self.session.query(
            ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        ).join(
            ARW_PRF_Mapping.cust_master_01_current.__table__,
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.Cust_Num ==
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Num
        ).filter(ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.in_(self.unit_value_list))
        # verbose_query(cust_shipto)

        atomic_value_list.extend([row[0] for row in cust_shipto.all()])

        cust_all = self.session.query(
            ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        ).join(
            ARW_PRF_Mapping.shipto_main_01_current.__table__,
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.Cust_Num ==
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Num
        ).filter(ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo.in_(self.unit_value_list))
        # verbose_query(cust_all)

        atomic_value_list.extend([row[0] for row in cust_all.all()])

        return_query = self.expansion_query()

        if atomic_value_list is not None:
            return_query = return_query.filter(
                self.entity.entity_expansion_query.c.Cust_Num_ShipTo_Combo.in_(atomic_value_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        return self.session.query(
            self.entity.entity_expansion_query.c.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class CustCatFactor(MatrixFactor):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Cust_Cat"
    unit_col = None
    lvl_list = ["51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "65"]

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        return self.session.query(
            self.entity.entity_expansion_query.c.Cust_Cat.label("Cust_Cat"),
            self.entity.entity_expansion_query.c.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo")
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class ProdNumFactor(MatrixFactor):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Prod_Num"  # Don't know if I need this
    unit_col = ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num
    lvl_list = ["01", "02", "14", "28", "51"]

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        return self.session.query(
            self.entity.entity_expansion_query.c.Prod_Num.label("Prod_Num")
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class ProdLineFactor(MatrixFactor):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Prod_Line"  # Don't know if I need this
    unit_col = ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Line
    lvl_list = ["03", "04", "09", "10", "15", "16", "21", "22", "29", "34", "35", "52", "53", "58", "59", "66",
                "67", "71", "72"]

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        return self.session.query(
            self.entity.entity_expansion_query.c.Prod_Line.label("Prod_Line"),
            self.entity.entity_expansion_query.c.Prod_Num.label("Prod_Num")
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class PriceGroupFactor(MatrixFactor):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Price_Group_Code"  # Don't know if I need this
    unit_col = ARW_PRF_Mapping.prod_main_01_current.__table__.c.Price_Group_Code
    lvl_list = ["03", "04", "05", "06", "07", "08", "15", "16", "17", "18", "19", "20", "29", "30", "31", "32",
                "33", "52", "53", "54", "55", "56", "57", "66", "67", "68", "69", "70"]

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        return self.session.query(
            self.entity.entity_expansion_query.c.Price_Group_Code.label("Price_Group_Code"),
            self.entity.entity_expansion_query.c.Prod_Num.label("Prod_Num")
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class PrimVendNumFactor(MatrixFactor):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Primary_Vend"  # Don't know if I need this
    unit_col = ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend
    lvl_list = ["03", "05", "07", "10", "11", "13", "15", "17", "19", "22", "23", "25", "30", "32", "35", "36",
                "38", "52", "54", "56", "59", "60", "62", "66", "69", "71", "73", "75"]

    @debug(lvl=logging.NOTSET, prefix='')
    def unit_to_atomic_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return_query = self.session.query(
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend.label("Primary_Vend"),
            ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num.label("Prod_Num")
        )
        if self.unit_value_list is not None:
            return_query = return_query.filter(
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend.in_(self.unit_value_list))
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def atomic_to_unit_query(self):
        raise NotImplementedError

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self, value_list=None):
        raise NotImplementedError

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        raise NotImplementedError


class VendNumFactor(MatrixFactor):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Vend_Num"  # Don't know if I need this
    unit_col = ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num
    lvl_list = ["03", "05", "07", "10", "11", "13", "15", "17", "19", "22", "23", "25", "30", "32", "35", "36",
                "38", "52", "54", "56", "59", "60", "62", "66", "69", "71", "73", "75"]

    @debug(lvl=logging.NOTSET, prefix='')
    def unit_to_atomic_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return_query = self.expansion_query()
        if self.unit_value_list is not None:
            return_query = return_query.filter(
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num.in_(self.unit_value_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return self.session.query(
            ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num.label("Vend_Num"),
            self.entity.entity_expansion_query.c.Prod_Num.label("Prod_Num")
        ).join(
            self.entity.entity_expansion_query,
            self.entity.entity_expansion_query.c.Prod_Num ==
            ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return (
            ARW_PRF_Mapping.prod_vend_01_current.__table__,
            self.entity.entity_expansion_query.c.Prod_Num ==
            ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num
        )


class MajorGroupFactor(MatrixFactor):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    unit = "Major_Group"  # Don't know if I need this
    unit_col = ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Major_Group
    lvl_list = ["05", "06", "11", "12", "17", "18", "23", "24", "30", "31", "36", "37", "54", "55", "60", "61",
                "68", "73", "74"]

    @debug(lvl=logging.NOTSET, prefix='')
    def unit_to_atomic_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return_query = self.expansion_query()
        if self.unit_value_list is not None:
            return_query = return_query.filter(
                ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Major_Group.in_(self.unit_value_list))
        # verbose_query(return_query)
        return return_query

    @debug(lvl=logging.NOTSET, prefix='')
    def expansion_query(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return self.session.query(
            ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Major_Group.label("Major_Group"),
            self.entity.entity_expansion_query.c.Prod_Num.label("Prod_Num")
        ).outerjoin(
            self.entity.entity_expansion_query,
            ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Code ==
            self.entity.entity_expansion_query.c.Prod_Line
        )

    @debug(lvl=logging.NOTSET, prefix='')
    def get_join_tuple(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        return (
            ARW_PRF_Mapping.prod_line_main_01_current.__table__,
            ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Code ==
            self.entity.entity_expansion_query.c.Prod_Line
        )
