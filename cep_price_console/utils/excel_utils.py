from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils.utils import is_path_exists_or_creatable
import logging.config
import logging
import os
import datetime
import xlrd
import string
from dateutil.parser import parse


class Workbook(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix="Workbook object instantiated")
    def __init__(self, xl_fullpath_pretty):
        self.__xl_fullpath_useful = None
        self.__xl_filepath = None
        self.__xl_filename = None
        self.__wb = None
        self.__ws_lst = None
        self.__ws_sel = None
        self.__ws_obj = None
        self.__row_count = None
        self.__col_count = None
        self.__header_row = None  # This attribute is specific to upload worksheets.
        self.col_dict = {}
        self.row_dict = {}
        self.cell_lst = []
        self.xl_fullpath_pretty = xl_fullpath_pretty

    # region xl_fullpath_pretty  #######################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def xl_fullpath_pretty(self):
        Workbook.logger.log(logging.NOTSET, "Getter Called: {0}".format(self.__xl_fullpath_pretty))
        return self.__xl_fullpath_pretty

    @xl_fullpath_pretty.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def xl_fullpath_pretty(self, value):
        try:
            str_val = str(value)
        except ValueError:
            Workbook.logger.log(logging.ERROR, "xl_fullpath_pretty Type Error: {0}".format(str(type(value))))
            raise ValueError("Filename must be a string. Value: {0], Type: {1}".format(value, type(value)))
        else:
            if str_val != "":
                if is_path_exists_or_creatable(str_val):
                    Workbook.logger.log(logging.NOTSET, "Valid filepath")
                    self.__xl_fullpath_pretty = value
                    self.__xl_fullpath_useful = \
                        str(value).replace('\\\\', '+-+-+-+-').replace('\\', '\\\\').replace('+-+-+-+-', '\\\\')
                    self.__xl_filepath, self.__xl_filename = os.path.split(self.xl_fullpath_useful)
                    try:
                        # noinspection PyAttributeOutsideInit
                        # self.__wb = xlrd.open_workbook(self.xl_fullpath_useful, on_demand=True)
                        self.open_wb()
                    except FileNotFoundError:
                        raise FileNotFoundError("File not found: {0}.".format(str_val))
                    else:
                        self.__ws_lst = self.wb.sheet_names()
                else:
                    Workbook.logger.log(logging.ERROR, "Invalid filepath")
                    raise ValueError("Pathname does not exist or is not creatable: {0}.".format(str_val))
            else:
                Workbook.logger.log(logging.ERROR, "Setter called with no value. No action taken.")
                raise ValueError("Filename is empty.".format(value, type(value)))
    # endregion ########################################################################################################

    @debug(lvl=logging.NOTSET, prefix='')
    def open_wb(self):
        self.__wb = xlrd.open_workbook(self.xl_fullpath_useful, on_demand=True)

    # region Getters  ##################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def xl_fullpath_useful(self):
        return self.__xl_fullpath_useful

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def xl_filepath(self):
        return self.__xl_filepath

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def xl_filename(self):
        return self.__xl_filename

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def wb(self):
        return self.__wb

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_lst(self):
        return self.__ws_lst

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_obj(self):
        return self.__ws_obj

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def row_count(self):
        return self.__row_count

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def col_count(self):
        return self.__col_count
    # endregion ########################################################################################################

    # region ws_sel  #################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_sel(self):
        return self.__ws_sel

    @ws_sel.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_sel(self, value):
        in_wb = self.ws_in_wb(value)
        if in_wb:
            self.__ws_sel = value
            try:
                self.__ws_obj = self.wb.sheet_by_name(value)
            except Exception as ex:
                self.__row_count = 999
                self.__col_count = 999
                Cell.logger.log(logging.NOTSET, "Exception Title: {0}, Exception Arguments: {1}".format(
                    type(ex).__name__, ex.args))
            else:
                Workbook.logger.log(logging.NOTSET, "Row Count: {0}, Col Count: {1}".
                                    format(self.ws_obj.nrows, self.ws_obj.ncols))
                self.__row_count = self.ws_obj.nrows
                self.__col_count = self.ws_obj.ncols
        elif not in_wb:
            raise ValueError("{0} Worksheet not in workbook.".format(value))
    # endregion ########################################################################################################

    # region header_row  ###############################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def header_row(self):
        return self.__header_row

    @header_row.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def header_row(self, value):
        if value not in (0, ""):
            try:
                int_val = int(value)
            except ValueError:
                Workbook.logger.log(logging.ERROR, "header_row Type Error: {0}".format(str(type(value))))
                raise ValueError("Header row value must be an integer. Current value: {0}, Type: {1}".
                                 format(value, type(value)))
            else:
                # noinspection PyPep8,PyBroadException
                try:
                    self.__header_row = int_val
                    self.populate_col_dict()
                    self.populate_cell_list()
                    for col in self.col_dict.values():
                        col.set_format_suggestion()
                except:
                    self.__header_row = None
                    self.col_dict = {}
                    self.row_dict = {}
                    self.cell_lst = []
                    pass
                else:
                    pass
        else:
            Workbook.logger.log(logging.ERROR, "Setter called with an empty value. No action taken.")
            raise ValueError("Header row called with no value.")

    # endregion ########################################################################################################
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_in_wb(self, ws_str):
        if isinstance(ws_str, str):
            if ws_str in self.ws_lst:
                Workbook.logger.log(logging.NOTSET, "Worksheet is in workbook")
                return True
            else:
                Workbook.logger.log(logging.ERROR, "Worksheet is NOT in workbook")
                return False
        else:
            Workbook.logger.error("Worksheet name is not a string")
            raise AttributeError

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_value(self, row_one_indexed, col_variant):
        if self.ws_obj is not None:
            col_one_indexed = self.fetch_col_int(col_variant)
            col_zero_indexed = col_one_indexed - 1
            row_zero_indexed = row_one_indexed - 1
            Workbook.logger.log(logging.NOTSET, "Row={0}, Col={1}.".format(row_one_indexed, col_one_indexed))
            cell_obj = Cell(
                wb=self,
                row_num_one_indexed=row_one_indexed,
                col_num_one_indexed=col_one_indexed,
                raw_val=self.ws_obj.cell(rowx=row_zero_indexed, colx=col_zero_indexed).value,
                cell_type=self.ws_obj.cell_type(rowx=row_zero_indexed, colx=col_zero_indexed)
            )
            return cell_obj
        else:
            Workbook.logger.error("Worksheet Object not set")

    @staticmethod
    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_col_int(col_variant):
        if isinstance(col_variant, int):
            value = col_variant
            Workbook.logger.log(logging.NOTSET, "Column integer fetch int: {0}".format(value))
            return value
        elif isinstance(col_variant, str):
            expn = 0
            conv = 0
            col_variant = col_variant.upper()
            for char in reversed(col_variant):
                conv += (ord(char) - ord('A') + 1) * (26 ** expn)
                expn += 1
            conv = conv
            value = conv
            Workbook.logger.log(logging.NOTSET, "Column integer fetch str: {0}".format(value))
            return value
        else:
            Workbook.logger.error("Column Conversion Value must be a string or an integer: {0}"
                                  .format(str(type(col_variant))))
            raise ValueError("Column must be a string or an integer.")

    @debug(lvl=logging.NOTSET, prefix='')
    def populate_col_dict(self):
        for col_num in range(1, self.col_count + 1):
            col_obj = MyColumn(
                wb=self,
                col_num_one_indexed=col_num
            )
            self.col_dict[col_num] = col_obj

    @debug(lvl=logging.NOTSET, prefix='')
    def populate_cell_list(self):
        for row_num in range(self.header_row + 1, self.row_count + 1):
            row_obj = Row(
                wb=self.wb,
                row_num_one_indexed=row_num
            )
            for col_num_one_indexed in sorted(self.col_dict.keys()):
                col_obj = self.col_dict[col_num_one_indexed]
                cell_obj = self.fetch_value(row_num, col_obj.col_num_one_indexed)
                self.cell_lst.append(cell_obj)
                col_obj.col_cells.append(cell_obj)
                row_obj.row_cells.append(cell_obj)

            self.row_dict[row_num] = row_obj


class MyColumn(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    def __init__(self,
                 wb,
                 col_num_one_indexed):
        self._hdr_cell = None
        self._hdr_id = None
        self._fmt_suggestion = None
        self._fmt_selection = None
        self.wb = wb
        self.col_num_one_indexed = col_num_one_indexed
        self.col_cells = []
        self.implement()

    # region wb  #######################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def wb(self):
        return self._wb

    @wb.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def wb(self, value):
        self._wb = value
    # endregion ########################################################################################################

    # region col_num_one_indexed  ######################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def col_num_one_indexed(self):
        return self._col_num_one_indexed

    @col_num_one_indexed.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def col_num_one_indexed(self, value):
        self._col_num_one_indexed = value
        self._hdr_cell = self.wb.fetch_value(self.wb.header_row, value)
    # endregion ########################################################################################################

    # region hdr_cell  ##############################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def hdr_cell(self):
        return self._hdr_cell

    @hdr_cell.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def hdr_cell(self, value):
        self._hdr_cell = value
    # endregion ########################################################################################################

    # region hdr_id  ###################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def hdr_id(self):
        return self._hdr_id

    @hdr_id.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def hdr_id(self, value):
        self._hdr_id = value
    # endregion ########################################################################################################

    # region fmt_suggestion  ###########################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_suggestion(self):
        return self._fmt_suggestion

    # noinspection PyAttributeOutsideInit
    @fmt_suggestion.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_suggestion(self, value):
        self._fmt_suggestion = value
        self.fmt_selection = value
    # endregion ########################################################################################################

    # region fmt_selection  ############################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_selection(self):
        return self._fmt_selection

    @fmt_selection.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_selection(self, value):
        self._fmt_selection = value
        if bool(self.col_cells):
            for cell in self.col_cells:
                cell.fmt_selection = value
    # endregion ########################################################################################################

    # noinspection PyAttributeOutsideInit
    @debug(lvl=logging.NOTSET, prefix='')
    def implement(self):
        col_id = str(self.hdr_cell.raw_val).strip().replace(" ", "_")
        cntr = 0
        col_id_len = len(col_id)
        for col in self.wb.col_dict.values():
            if col.hdr_id[:col_id_len] == col_id:
                cntr += 1
        if col_id in (None, ""):
            col_id_unique = "C" + str(self.col_num_one_indexed)
        else:
            if cntr == 0:
                col_id_unique = col_id
            else:
                col_id_unique = col_id + "_" + str(cntr)
        self.hdr_id = col_id_unique

    # noinspection PyAttributeOutsideInit
    @debug(lvl=logging.NOTSET, prefix='')
    def set_format_suggestion(self):
        if bool(self.col_cells):
            has_str = False
            has_int = False
            has_float = False
            has_date = False
            has_boolean = False
            has_error = False
            for cell in self.col_cells:
                cell_fmt = cell.fmt_suggestion
                self.__class__.logger.log(logging.NOTSET, "Cell Formatting: {0}".format(cell_fmt))
                if cell_fmt == 'string':
                    has_str = True
                elif cell_fmt == 'float':
                    has_float = True
                elif cell_fmt == 'date':
                    has_date = True
                elif cell_fmt == 'boolean':
                    has_boolean = True
                elif cell_fmt == 'error':
                    has_error = True
                elif cell_fmt == 'integer':
                    has_int = True
            if has_error:
                self.fmt_suggestion = 'error'
            elif has_date:
                self.fmt_suggestion = 'date'
            elif has_boolean:
                self.fmt_suggestion = 'boolean'
            elif has_float:
                self.fmt_suggestion = 'float'
            elif has_int:
                self.fmt_suggestion = 'integer'
            elif has_str:
                self.fmt_suggestion = 'string'
            else:
                raise AttributeError('Column Title: {0}, No suggestion formulated.'.format(self.hdr_cell.raw_val))
        else:
            raise AttributeError('Column Title: {0}, Suggestion called before cells populated.'
                                 .format(self.hdr_cell.raw_val))


class Row(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 wb,
                 row_num_one_indexed):
        self.wb = wb
        self.row_num_one_indexed = row_num_one_indexed
        self.row_cells = []


class Cell(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # xlrd Ctype Formats:
    # -------------------------------------------------------------------------------------------------------------
    # XL_CELL_EMPTY	    0	empty string u''
    # XL_CELL_TEXT	    1	a Unicode string
    # XL_CELL_NUMBER    2	float
    # XL_CELL_DATE	    3	float
    # XL_CELL_BOOLEAN	4	int; 1 means TRUE, 0 means FALSE
    # XL_CELL_ERROR	    5	int representing internal Excel codes
    # XL_CELL_BLANK	    6	empty string u''.
    #                       Note: this type will appear only when open_workbook(..., formatting_info=True) is used.
    cell_type_dict = {
        '0': 'string',
        '1': 'string',
        '2': 'float',
        '3': 'date',
        '4': 'boolean',
        '5': 'error',
        '6': 'blank'
    }

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 wb,
                 row_num_one_indexed,
                 col_num_one_indexed,
                 raw_val,
                 cell_type
                 ):
        # self._sans_ascii = None
        # self._sans_special_char = None
        self._fmt_suggestion = None
        self._fmt_selection = None
        self._formatted_value = None
        self.wb = wb  # Done
        self.row_num_one_indexed = row_num_one_indexed
        self.col_num_one_indexed = col_num_one_indexed
        self.raw_raw_val = raw_val
        self.raw_val = raw_val
        self.cell_type = cell_type
        self.implement()

    # region wb  #######################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def wb(self):
        return self._wb

    @wb.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def wb(self, value):
        self._wb = value
    # endregion ########################################################################################################

    # region row_num_one_indexed  ######################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def row_num_one_indexed(self):
        return self._row_num_one_indexed

    @row_num_one_indexed.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def row_num_one_indexed(self, value):
        self._row_num_one_indexed = value
    # endregion ########################################################################################################

    # region col_num_one_indexed  ######################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def col_num_one_indexed(self):
        return self._col_num_one_indexed

    @col_num_one_indexed.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def col_num_one_indexed(self, value):
        try:
            int_val = int(value)
        except TypeError:
            self._col_num_one_indexed = 999
            raise ValueError("Column Number One Indexed must be an integer. Value: {0}, Type: {1}"
                             .format(value, str(type(value))))
        except Exception as ex:
            self._col_num_one_indexed = 999
            Cell.logger.log(logging.NOTSET,
                            "Exception Title: {0}, Exception Arguments: {1}".format(type(ex).__name__, ex.args))
        else:
            self._col_num_one_indexed = int_val
    # endregion ########################################################################################################

    # region raw_val  ##################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def raw_val(self):
        return self._raw_val

    @raw_val.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def raw_val(self, value):
        if isinstance(value, str):
            printable = set(string.printable)
            self._raw_val = ''.join(filter(lambda x: x in printable, value)).replace('\r', '').replace('\n', '')
        else:
            self._raw_val = value
        # self.sans_ascii = ascii_scrub(value).rstrip().lstrip()
    # endregion ########################################################################################################

    # # region sans_ascii  #############################################################################################
    # @property
    # @debug(lvl=logging.NOTSET, prefix='')
    # def sans_ascii(self):
    #     return self._sans_ascii
    #
    # @sans_ascii.setter
    # @debug(lvl=logging.NOTSET, prefix='')
    # def sans_ascii(self, value):
    #     self._sans_ascii = value
    #     self.sans_special_char = special_char_scrub(value)
    # # endregion ######################################################################################################

    # # region sans_special_char  ######################################################################################
    # @property
    # @debug(lvl=logging.NOTSET, prefix='')
    # def sans_special_char(self):
    #     return self._sans_special_char
    #
    # @sans_special_char.setter
    # @debug(lvl=logging.NOTSET, prefix='')
    # def sans_special_char(self, value):
    #     self._sans_special_char = value
    # # endregion ######################################################################################################

    # region cell_type  ###############################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def cell_type(self):
        return self._cell_type

    @cell_type.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def cell_type(self, value):
        if str(value) in Cell.cell_type_dict.keys():
            self._cell_type = value
            if value == 2:
                Cell.logger.log(logging.NOTSET, "Row={0}, Col={1}, Raw Value: {2}, Cell Type: {3}.".
                                format(self.row_num_one_indexed,
                                       self.col_num_one_indexed,
                                       self.raw_val,
                                       str(value)))

                try:
                    value = int(self.raw_val)
                    Cell.logger.log(logging.NOTSET, "Integer Value={0}". format(value))
                    str_val = str(self.raw_val)
                    Cell.logger.log(logging.NOTSET, "String Value={0}". format(str_val))
                    if str_val[:1] == "0":
                        Cell.logger.log(logging.NOTSET, "Left-most value is a 0, should be string.")
                        self.fmt_suggestion = 'string'
                        raise ValueError
                    else:
                        Cell.logger.log(logging.NOTSET, "Left-most value is not a 0.")
                        raise_error = False
                        try:
                            flt_value = float(self.raw_val)
                            Cell.logger.log(logging.NOTSET, "Float value={0}". format(value))
                            if flt_value - value == 0:
                                self.fmt_suggestion = 'integer'
                            else:
                                raise_error = True
                        except ValueError:
                            self.fmt_suggestion = 'integer'
                            Cell.logger.log(logging.NOTSET, "Left-most value not a 0, not a float. Value is a string.")
                            raise_error = False
                        except Exception as ex:
                            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            Cell.logger.error(message)
                    Cell.logger.log(logging.NOTSET, "Raise Error={0}". format(raise_error))
                    if raise_error:
                        raise ValueError
                except ValueError:
                    try:
                        value = float(self.raw_val)
                        Cell.logger.log(logging.NOTSET, "Value={0}". format(value))
                        str_val = str(self.raw_val)
                        Cell.logger.log(logging.NOTSET, "String Value={0}". format(str_val))
                        if str_val[:1] == "0":
                            Cell.logger.log(logging.NOTSET, "Left-most value is a 0, should be string.")
                            raise ValueError
                        else:
                            Cell.logger.log(logging.NOTSET, "Left-most value is not a 0. Value is a float")
                            self.fmt_suggestion = 'float'
                    except ValueError:
                        try:
                            value = parse(self.raw_val)
                            self.fmt_suggestion = 'date'
                        except ValueError:
                            try:
                                value = str(self.raw_val)
                                self.fmt_suggestion = 'string'
                            except ValueError:
                                self.fmt_suggestion = 'error'
                            except Exception as ex:
                                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                                message = template.format(type(ex).__name__, ex.args)
                                Cell.logger.error(message)
                        except Exception as ex:
                            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            Cell.logger.error(message)
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    Cell.logger.error(message)
                Cell.logger.log(logging.NOTSET, "Value={0}, Format Suggestion: {1}". format(value, self.fmt_suggestion))
            else:
                self.fmt_suggestion = Cell.cell_type_dict[str(value)]
            Cell.logger.log(logging.NOTSET, "Row={0}, Col={1}, Value: {2}, Datatype: {3}.".
                            format(self.row_num_one_indexed,
                                   self.col_num_one_indexed,
                                   self.raw_val,
                                   self.fmt_suggestion))
        else:
            raise AttributeError("Cell type must be in cell type dictionary. {0} is not a valid type.".format(value))

    # endregion ########################################################################################################

    # region fmt_suggestion  ###########################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_suggestion(self):
        return self._fmt_suggestion

    # noinspection PyAttributeOutsideInit
    @fmt_suggestion.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_suggestion(self, value):
        self._fmt_suggestion = value
        self.fmt_selection = value
    # endregion ########################################################################################################

    # region fmt_selection  ############################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_selection(self):
        return self._fmt_selection

    # noinspection PyAttributeOutsideInit
    @fmt_selection.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def fmt_selection(self, value):
        self._fmt_selection = value

        if self.raw_val == "":
            self.formatted_value = None
        else:
            if value == 'string':
                if isinstance(self.raw_val, (int, float)):
                    try:
                        int_val = int(self.raw_val)
                        str_val = float(self.raw_val)
                        if int_val - str_val == 0:
                            self.formatted_value = str(int(self.raw_val))
                    except ValueError:
                        pass
                else:
                    try:
                        str_raw_val = str(self.raw_val)
                        if len(str_raw_val) > 225:
                            try:
                                self.formatted_value = str_raw_val[:225]
                            except ValueError:
                                self.formatted_value = "~Conversion Error~"
                        else:
                            try:
                                self.formatted_value = str_raw_val
                            except ValueError:
                                self.formatted_value = "~Conversion Error~"
                    except ValueError:
                        self.formatted_value = "~Conversion Error~"

            elif value == 'integer':
                try:
                    self.formatted_value = int(self.raw_val)
                except ValueError:
                    self.formatted_value = "~Conversion Error~"
            elif value == 'float':
                try:
                    self.formatted_value = float(self.raw_val)
                except ValueError:
                    try:
                        val = str(self.raw_val).strip("$").strip("USD")
                        print(val)
                        self.formatted_value = float(val)
                    except ValueError:
                        self.formatted_value = "~Conversion Error~"
            elif value == 'date':
                # noinspection PyBroadException,PyPep8
                try:
                    ms_date_number = self.raw_val
                    year, month, day, hour, minute, nearest_second = xlrd.xldate_as_tuple(ms_date_number,
                                                                                          self.wb.wb.datemode)
                    self.formatted_value = datetime.datetime(year, month, day, hour, minute, nearest_second)
                except:
                    # noinspection PyBroadException,PyPep8
                    try:
                        self.formatted_value = parse(self.raw_val)
                    except:
                        self.formatted_value = "~Conversion Error~"
            elif value == 'boolean':
                try:
                    self.formatted_value = bool(self.raw_val)
                except ValueError:
                    self.formatted_value = "~Conversion Error~"
            elif value == 'error':
                try:
                    self.formatted_value = str(self.raw_val)
                except ValueError:
                    self.formatted_value = "~Conversion Error~"
            elif value == 'blank':
                self.formatted_value = None
    # endregion ########################################################################################################

    # region formatted_value  ##########################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def formatted_value(self):
        Cell.logger.log(logging.NOTSET, "Row={0}, Col={1}, Value: {2}, Datatype: {3}.".
                        format(self.row_num_one_indexed,
                               self.col_num_one_indexed,
                               self._formatted_value,
                               self.fmt_selection))
        return self._formatted_value

    @formatted_value.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def formatted_value(self, value):
        self._formatted_value = value
    # endregion ########################################################################################################

    def implement(self):
        pass
