#FROM ibmcom/websphere-traditional:8.5.5.17
FROM image-registry.openshift-image-registry.svc:5000/pipelines-tutorial/was855:latest
# copy property files and jython scripts, using the flag `--chown=was:root` to set the appropriate permission
COPY --chown=was:0 basicapp/password/adminpassword /tmp/PASSWORD
COPY --chown=was:0 basicapp/work/app/TestTWASAppWeb.war /work/app/TestTWASAppWeb.war
COPY --chown=was:0 basicapp/work/config/appinstall.py /work/config/appinstall.py
COPY --chown=was:0 basicapp/work/db2/ /opt/IBM/db2drivers
COPY --chown=was:0 basicapp/testconfig.properties /opt/IBM/config/
RUN /work/configure.sh
