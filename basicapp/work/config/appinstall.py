#Location of DB2 Drivers
db2DriverDir = "/opt/IBM/db2drivers"

db2DatabaseName = "SAMPLE"
db2Server = "ec2-3-90-44-194.compute-1.amazonaws.com"
db2Port = "50000"

db2DataSourceName = "DefaultDataSource"
db2jndi = "jdbc/sampleDS"

db2UserAlias = "app_dbuser"
db2UserName = "db2inst1"
db2UserPassword = "zxcASDqwe!@#"

SharedLibraryName = "AppConfigProperties"
SharedLibraryClassPath = "/opt/IBM/config"

ApplicationName = "TestTWASApp"
WebModuleName = "TestTWASAppWeb.war"


Server=AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/Node:' + AdminControl.getNode() + '/Server:server1')
Node=AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/Node:' + AdminControl.getNode() + '/')
Cell=AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/')
NodeName=AdminControl.getNode()

print 'Creating DB2_JCC_DRIVER_PATH '

db2VarName = "UNIVERSAL_JDBC_DRIVER_PATH"
db2Var1Name= "DB2_JCC_DRIVER_PATH"

 
varSubstitutions = AdminConfig.list("VariableSubstitutionEntry",Node).split(java.lang.System.getProperty("line.separator"))
 
for varSubst in varSubstitutions:
   getVarName = AdminConfig.showAttribute(varSubst, "symbolicName")
   if getVarName == db2VarName:
      AdminConfig.modify(varSubst,[["value", db2DriverDir]])
      break
  
for varSubst in varSubstitutions:
   getVarName = AdminConfig.showAttribute(varSubst, "symbolicName")
   if getVarName == db2Var1Name:
      AdminConfig.modify(varSubst,[["value", db2DriverDir]])
      break
   
AdminConfig.save()

print 'Creating JDBC Provider '

# [8/24/20 16:01:07:788 UTC] JDBC providers
AdminTask.createJDBCProvider('[-scope Cell=' + AdminControl.getCell() + ' -databaseType DB2 -providerType "DB2 Using IBM JCC Driver" -implementationType "Connection pool data source" -name "DB2 Using IBM JCC Driver" -description "One-phase commit DB2 JCC provider that supports JDBC 4.0 using the IBM Data Server Driver for JDBC and SQLJ. IBM Data Server Driver is the next generation of the DB2 Universal JCC driver. Data sources created under this provider support only 1-phase commit processing except in the case where JDBC driver type 2 is used under WebSphere Application Server for Z/OS. On WebSphere Application Server for Z/OS, JDBC driver type 2 uses RRS and supports 2-phase commit processing. This provider is configurable in version 7.0 and later nodes." -classpath [${DB2_JCC_DRIVER_PATH}/db2jcc4.jar ${UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar ${DB2_JCC_DRIVER_PATH}/db2jcc_license_cisuz.jar ${PUREQUERY_PATH}/pdq.jar ${PUREQUERY_PATH}/pdqmgmt.jar ] -nativePath [${DB2_JCC_DRIVER_NATIVEPATH} ] ]')
 
# Note that scripting list commands may generate more information than is displayed by the administrative console because the console generally filters with respect to scope, templates, and built-in entries.

# [8/24/20 13:21:12:289 UTC] JDBC providers
AdminConfig.list('JDBCProvider', Cell)

# [8/24/20 13:21:14:835 UTC] JDBC providers
AdminConfig.save()

print 'Creating Auth Alias '
# [8/24/20 13:24:07:521 UTC] Data sources > JAAS - J2C authentication data > New...
AdminTask.createAuthDataEntry('[-alias ' + db2UserAlias + ' -user ' + db2UserName + ' -password ' + db2UserPassword + ' -description  ]')

# [8/24/20 13:24:07:644 UTC] Data sources > JAAS - J2C authentication data > New...
AdminTask.listAuthDataEntries()

# [8/24/20 13:24:09:741 UTC] Data sources > JAAS - J2C authentication data
AdminConfig.save()

print 'Creating Datasource '
myJDBCProviderVariable=AdminConfig.list('JDBCProvider', 'DB2 Using IBM JCC Driver*')
 
# [8/24/20 13:24:58:641 UTC] Data sources
AdminTask.createDatasource(myJDBCProviderVariable, '[-name ' + db2DataSourceName + ' -jndiName ' + db2jndi + ' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias ' + AdminControl.getNode() + '/' + db2UserAlias + ' -configureResourceProperties [[databaseName java.lang.String ' + db2DatabaseName + '] [driverType java.lang.Integer 4] [serverName java.lang.String ' + db2Server + '] [portNumber java.lang.Integer ' + db2Port + ']]]')
 
myDefaultDataSourceVariable=AdminConfig.list('DataSource', db2DataSourceName + '*')
 
# [8/24/20 13:24:58:649 UTC] Data sources
AdminConfig.create('MappingModule', myDefaultDataSourceVariable, '[[authDataAlias ' + AdminControl.getNode() + '/' + db2UserAlias + '] [mappingConfigAlias ""]]')
 
myCMPConnectorFactoryVariable=AdminConfig.list('CMPConnectorFactory')
 
# [8/24/20 13:24:58:651 UTC] Data sources
AdminConfig.modify(myCMPConnectorFactoryVariable, '[[name "DefaultDataSource_CF"] [authDataAlias ' + AdminControl.getNode() + '/' + db2UserAlias + '] [xaRecoveryAuthAlias ""]]')

# [8/24/20 13:24:58:653 UTC] Data sources
AdminConfig.create('MappingModule', myCMPConnectorFactoryVariable, '[[authDataAlias ' + AdminControl.getNode() + '/' + db2UserAlias + '] [mappingConfigAlias ""]]')

# Note that scripting list commands may generate more information than is displayed by the administrative console because the console generally filters with respect to scope, templates, and built-in entries.

# [8/24/20 13:24:58:748 UTC] Data sources
AdminConfig.list('DataSource', Cell)

# [8/24/20 13:25:00:805 UTC] Data sources
AdminConfig.save()

print 'Installing Application '
AdminApp.install('/work/app/TestTWASAppWeb.war', '[  -appname ' + ApplicationName + ' -contextroot /TestServletWebProject  ]' )
 
# Save App
AdminConfig.save()

print 'Successfully Installed Application '

print 'Configuring shared library references  '
AdminConfig.create('Library', Cell, '[[nativePath ""] [name ' + SharedLibraryName + '] [isolatedClassLoader false] [description ""] [classPath ' + SharedLibraryClassPath + ']]')

AdminConfig.save()

# [8/24/20 16:48:27:115 UTC] Enterprise Applications > TestTWASApp > Shared library references
AdminApp.edit(ApplicationName, '[  -MapSharedLibForMod [[ ' + ApplicationName + ' META-INF/application.xml AppConfigProperties ][ ' + WebModuleName + ' ' + WebModuleName + ',WEB-INF/web.xml ' + SharedLibraryName + ' ]]]' )

# [8/24/20 16:48:32:971 UTC] Enterprise Applications > TestTWASApp
AdminConfig.save()

print 'Successfully Installed and Configured Application '
