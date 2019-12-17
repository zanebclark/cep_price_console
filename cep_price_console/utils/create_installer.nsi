!include ${CFG_LIST}
!define ARCHITECTURE "Unknown"
!define OUTFILE "Installer_v${VERSION_MAJOR}-${VERSION_MINOR}.exe"
!define UNINSTALLER "uninstall_v${VERSION_MAJOR}-${VERSION_MINOR}.exe"
!define SHORTCUT "${APP_TITLE}.lnk"
!define ARP "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANY_NAME} ${APP_TITLE}"

# For removing Start Menu shortcuts in Windows 7
RequestExecutionLevel admin

ManifestSupportedOS Win7

# set the install directory
InstallDir "$PROGRAMFILES\${COMPANY_NAME}\${APP_TITLE}"

# rtf or txt file - remember if it is txt, it must be in the DOS text format (\r\n)
LicenseData "${LICENSE_DATA_DOC}"

# This will be in the installer/uninstaller's title bar
Name "${COMPANY_NAME} - ${APP_TITLE}"
Icon "${MEDIA_DIR}\${FAVICON_FILE}"
UninstallIcon "${MEDIA_DIR}\${FAVICON_FILE}"

# name of the installer
OutFile "${DIST_PATH}\${OUTFILE}"

!define REALMSG "$\nOriginal non-restricted account type: $2"

!include "LogicLib.nsh"
!include "FileFunc.nsh"
!include "x64.nsh"

page license
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
    quit
${EndIf}
!macroend

Function .onInit
	SetShellVarContext all
	!insertmacro VerifyUserIsAdmin
FunctionEnd

Section "install"
	${If} ${RunningX64}
		StrCpy $0 "64"
	${Else}
		StrCpy $0 "32"
	${EndIf}   
	#MessageBox MB_OK "Computer is running $0 bit architecture"
	
	#ReadRegStr $9 "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANY_NAME} ${APP_NAME}"
    #
	#inetc::get /POPUP "" /CAPTION "Something is downloading." \
	#"https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe" \
	#"$INSTDIR\python.exe"
    #Pop $0 # return value = exit code, "OK" if OK
	#StrCmp $0 "OK" dlok
	#MessageBox MB_OK|MB_ICONEXCLAMATION "http upload Error, click OK to abort installation" /SD IDOK
	#Abort
	#dlok:
	#
	#MessageBox MB_OK "Download Status: $0"
	##https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe
	
	# define the output path
	SetOutPath $INSTDIR

	!include  ${INST_LIST} ; the payload of this installer is described in an externally generated list of files
	
	${GetSize} "$INSTDIR" "/S=OK" $0 $1 $2
	IntFmt $0 "0x%08X" $0
	
	# Start Menu
	createDirectory "$SMPROGRAMS\${COMPANY_NAME}"
	
	# create a shortcut in the start menu programs directory
	createShortCut "$SMPROGRAMS\${COMPANY_NAME}\${SHORTCUT}" "$INSTDIR\${APP_NAME}.exe" "" "$INSTDIR\${MEDIA_SUBDIR}\${FAVICON_FILE}"

	# define uninstaller name
	WriteUninstaller "$INSTDIR\${UNINSTALLER}"
	
	WriteRegStr HKLM "${ARP}" "DisplayName" "${APP_TITLE}"
	WriteRegStr HKLM "${ARP}" "UninstallString" "$\"$INSTDIR\${UNINSTALLER}$\""
	WriteRegStr HKLM "${ARP}" "QuietUninstallString" "$\"$INSTDIR\${UNINSTALLER}$\" /S"
	WriteRegStr HKLM "${ARP}" "InstallLocation" "$\"$INSTDIR$\""
	WriteRegStr HKLM "${ARP}" "DisplayIcon" "$\"$INSTDIR\${MEDIA_SUBDIR}\${FAVICON_FILE}$\""
	WriteRegStr HKLM "${ARP}" "Publisher" "${COMPANY_NAME}"
	WriteRegStr HKLM "${ARP}" "DisplayVersion" "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_BUILD}"
	WriteRegDWORD HKLM "${ARP}" "VersionMajor" ${VERSION_MAJOR}
	WriteRegDWORD HKLM "${ARP}" "VersionMinor" ${VERSION_MINOR}
	WriteRegDWORD HKLM "${ARP}" "NoModify" 1
	WriteRegDWORD HKLM "${ARP}" "NoRepair" 1
	WriteRegDWORD HKLM "${ARP}" "EstimatedSize" "$0"
	WriteRegStr HKLM "${ARP}" "Comments" "${COMMENTS}"
	WriteRegStr HKLM "${ARP}" "Readme" "$\"$INSTDIR\${README}$\""

#Default section end
SectionEnd

/*
# default section start
Section


	# create a popup box, with an "OK" button and the test "Hello world!"
	MessageBox MB_OK "Now we are creating a Hello_world.txt in the install directory!"

	FileOpen $0 "$\"$INSTDIR\${README}$\"" w

	# write the string "hello world!" to the output file
	FileWrite $0 "hello world!"

	# close the file
	FileClose $0

	MessageBox MB_OK "Hello_world.txt has been created successfully at Desktop!"

	# specify file to go in output path
	#File something.txt


	
	
	
	# read the value from the registry into the $0 register
	ReadRegStr $0 HKLM "SOFTWARE\JavaSoft\Java Runtime Environment" CurrentVersion
	
	# print the results in a popup message box
	MessageBox MB_OK "version: $0"

#Default section end
SectionEnd
*/

/*
Section
	ClearErrors
	UserInfo::GetName
	IfErrors Win9x
	Pop $0
	UserInfo::GetAccountType
	Pop $1
	# GetOriginalAccountType will check the tokens of the original user of the
	# current thread/process. If the user tokens were elevated or limited for
	# this process, GetOriginalAccountType will return the non-restricted
	# account type.
	# On Vista with UAC, for example, this is not the same value when running
	# with `RequestExecutionLevel user`. GetOriginalAccountType will return
	# "admin" while GetAccountType will return "user".
	UserInfo::GetOriginalAccountType
	Pop $2
	StrCmp $1 "Admin" 0 +3
		MessageBox MB_OK 'User "$0" is in the Administrators group${REALMSG}'
		Goto done
	StrCmp $1 "Power" 0 +3
		MessageBox MB_OK 'User "$0" is in the Power Users group${REALMSG}'
		Goto done
	StrCmp $1 "User" 0 +3
		MessageBox MB_OK 'User "$0" is just a regular user${REALMSG}'
		Goto done
	StrCmp $1 "Guest" 0 +3
		MessageBox MB_OK 'User "$0" is a guest${REALMSG}'
		Goto done
	MessageBox MB_OK "Unknown error"
	Goto done

	Win9x:
		# This one means you don't need to care about admin or
		# not admin because Windows 9x doesn't either
		MessageBox MB_OK "Error! This DLL can't run under Windows 9x!"

	done:
SectionEnd
*/

Function un.onInit
	SetShellVarContext all
	
	# verify the uninstaller - last chance to back output
	MessageBox MB_OKCANCEL "Permanantly remove ${APP_TITLE}?" IDOK next
		Abort
	next:
		!insertmacro VerifyUserIsAdmin
FunctionEnd

# create a section to define what the uninstaller does. This section will always be named "uninstall"
Section "Uninstall"
    ; Remove the files (using externally generated file list)
    !include ${UNINST_LIST}
    Delete "$INSTDIR\utils\config.ini"
    Delete "$INSTDIR\utils"
	# delete shortcut
	Delete "$SMPROGRAMS\${COMPANY_NAME}\${SHORTCUT}"
	# Try to remove the Start Menu folder - this will only happen if it is empty
	rmDir "$SMPROGRAMS\${COMPANY_NAME}"

	
	# now delete installed file
	Delete "$INSTDIR\${OUTFILE}"
	Delete "$INSTDIR"

	# always delete the uninstaller last?
	Delete "$INSTDIR\${UNINSTALLER}"
	
	# Try to remove the install directory - this will only happen if it is empty
	rmDir $INSTDIR
	
	DeleteRegKey HKLM "${ARP}"
SectionEnd
