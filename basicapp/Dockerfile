FROM ibmcom/websphere-traditional:8.5.5.17
# copy property files and jython scripts, using the flag `--chown=was:root` to set the appropriate permission
COPY --chown=was:0 password/adminpassword /tmp/PASSWORD
COPY --chown=was:0 work/app/TestTWASAppWeb.war /work/app/TestTWASAppWeb.war
COPY --chown=was:0 work/config/appinstall.py /work/config/appinstall.py
COPY --chown=was:0 work/db2/ /opt/IBM/db2drivers
COPY --chown=was:0 testconfig.properties /opt/IBM/config/
RUN /work/configure.sh
