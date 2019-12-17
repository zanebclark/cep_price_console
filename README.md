# cep_price_console
The CEP Price Console supplements the functionality of DDI's Inform ERP software. This tool was developed for a 
DDI Inform client (CEP) to suppliment the software's operations in the following ways: 
1) At the time of the software's creation, Inform lacked a robust price contract upload tool. The tool didn't have 
robust product-matching logic or visibility on product associations prior to committing the upload. The CEP Price 
Console ingests a vendor price contract, appends internal part numbers, and produces a ready-to-import file that can
be reported on and reviewed. 
2) DDI Inform couldn't develop a price list that took into account both sales history and pricing matrix rules. The CEP
Price Console has a robust price list generation tool that can be configured to take these factors into account. 
3) To achieve the above ends, the CEP Price Console performs scheduled ETL operations and regularly archives a snapshot 
of the DDI Inform database. The database definition is persisted in an .xlsx file for ease of alteration. The GUI 
features a tool that will mine this .xlsx file for DDL, translate this DDL into Python scripts that will fuel the 
SQLAlchemy ORM.

## Getting Started
#### [1] System Requirements: 
##### [a] OS: 
* This app was developed on a Windows 10 OS for a Windows 7 or 10 deployment. If you're interested in deploying on a 
different version of Windows or on a different operating system, please reach out and I'll collaborate with you on 
the effort.  <br /> 
##### [b] Programs: 
1) Python 3.7.3 <br /> 
2) [NSIS 3.04](https://nsis.sourceforge.io/Main_Page)

##### [c] Virtual Environment (Recommended): 
* I'd recommend that you perform the following steps in a virtual environment. If you're on a Window's machine, 
I'd recommend [virtualenvwrapper-win](https://pypi.org/project/virtualenvwrapper-win/).  <br /> 
`pip install virtualenvwrapper-win` 
* If you have already created a virtual environment: <br /> 
`workon cep_price_console` <br /> 
* Else, navigate to the `cep_price_console` directory and enter the following commands:  <br /> 
`mkvirtualenv -a . -r requirements.txt cep_price_console` 

#### [2] Configuration: 
Config values can be found in `.\cep_price_console\cep_price_console\utils\config.py`. A few notes on some of the more
useful config values:

##### [a] Required:
* NSIS_PATH - Required: This will need to be the path of your NSIS installation. 
* mssql_dsn - Required: This is one of the few DB config values that can't be changed in the GUI. This should be 
pointed to your DDI Inform `ddidatawarehouse`.
* mysql_host_var - Required: This is one of the few DB config values that can't be changed in the GUI. This value 
points to the DB that will be performing the analysis. This app was developed using MySQL, but the SQLAlchemy library 
offers the flexibility to choose a technology with very few modifications.
* contract_dir - This value should point to your DDI Inform `PriceContracts` directory.
* arw_export_dir - This value should point to your DDI Inform `AUTOARW FILE EXPORTS` directory.

##### [b] GUI Accessible:
The following config values are required, but they can be altered via the GUI.
* mysql_username
* mysql_password
* mysql_user_database
* mssql_username
* mssql_password

##### [c] Development:
The following config values are useful for iterative development efforts, as they are baked into file paths and names
to allow for multiple installed versions. 
* VERSION_MAJOR
* VERSION_MINOR
* VERSION_BUILD

##### [d] Whitelabel:
To whitelabel the application, you will need to change the following values: 
* COMPANY_NAME
* DESCRIPTION - This shows up in the installer/uninstaller GUI
* COMMENTS - This shows up in the installer/uninstaller GUI
* APP_TITLE
* APP_NAME
* LICENSE_DATA_FILE - This shows up in the installer/uninstaller GUI
* FAVICON - This is the icon used on the app, installer and uninstaller
* ICON_FILE - This is the icon used on the app, installer and uninstaller
* README_FILENAME - This shows up in the installer/uninstaller GUI

##### [d] DDI Inform Data Model:
* ARW_PRF_MAPPING_FILE - This points to an Excel spreadsheet that attempts to represent the DDI data model. For more 
information about that process, see "[4] Set up ETL Operations" (below)

#### [3] Build Distributable Installer: 
1) With your new virtual environment activated, run:  <br /> `python ./cep_price_console/utils/build_utils.py` 
    * Log files will be generated in the user's 
`AppData\Local\Controlled Environment Products\cep_price_console_v{major_version}-{minor_version}\Logs` 
repo where `{major_version}` and `{minor_version}` represent the major and minor version config values, respectively, 
of the software.
2) When `build_utils` finishes, the build will be located in `.\cep_price_console\dist\cep_price_console_v{major_version}-{minor_version}`. 
    * Note: A similar folder will be created titled `dist`. That's not the right one. It's a bit of a misnomer.
3) Run the `cep_price_console_v{major_version}-{minor_version}.exe` file to test the distribution on the development computer. It should launch a 
fully-functioning app. 
4) Launch the `Installer_v{major_version}-{minor_version}.exe` to test the installer on the development machine. It should launch a NSIS-powered 
installer. 
    * When you complete the installation process, the application will be available via the toolbar search. 
    * It can also be uninstalled like most Windows programs: in the Control Panel. 
5) If both the app and the installer work on the development computer, the installer should be ready to distribute. 

#### [4] Set up ETL Operations:
##### [a] Configure DDI Inform
Configure DDI Inform's Advanced Report Writer to write hourly exports in csv format.
TODO: Find these configurations and include them in the repo.
TODO: Expand on these instructions
##### [b] Test ETL Operations
The GUI is capable of running all ETL operations. For testing and debugging, these options will suffice. 
##### [c] Schedule ETL Operations
In a production environment, you will want to schedule to ETL operations to run on a regular basis. The 
executable produced in Step 3 (above) can be run with arguments that update the database and skip launching the GUI. 
Windows Scheduler can be configured to run the executable with the required arguments. Recommended configuration: 
* `--schedule_mode=recreate`: This wouldn't be a good thing to schedule, as it will drop the entire database.
* `--schedule_mode=update`: Schedule this to run every hour. It will archive the current snapshot of the DB and pull a 
new one from DDI Inform
* `--schedule_mode=daily`: Schedule this to run daily. It will pull larger tables (invoices, etc,.) that don't warrant 
hourly pulls. 

#### [5] Release History:
* 0.1.1
    * Initial release

#### [6] Authors:
* Zane Clark - hello@zanebclark.com – [https://github.com/zanebclark](https://github.com/zanebclark/)

#### [6] License:
Distributed under the MIT License. See ``LICENSE`` for more information.

#### [7] Contributing:
##### [a] Development Roadmap: 
1) Testing: 'Nuff said
2) Extensibility: This project was written for a single client at the expense of extensibility. I would love to 
collaborate with a company to deploy this tool in a new environment. 
3) Documentation: Further documentation on the setup, configuration, and maintenance of the tool is required. Again, I 
would love to collaborate with a client on this. 
4) Feature Growth: What else is needed to make DDI Inform a seamless experience? Let's develop it. 

##### [b] Contributing 101: 
1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request