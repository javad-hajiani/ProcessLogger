#!/bin/bash
echo "### Initializing ... ### "
if [ ! -d "/opt/pmonitor" ]; then
mkdir /opt/pmonitor/
fi
cp -r ./* /opt/pmonitor/
if [ $? -ne 0 ]; then
echo "### unexpectedly Error ###"
exit 1
fi

echo "### pmonitor script Installed ### "
cp -r ./init.d/* /etc/init.d/
if [ $? -ne 0 ]; then
echo "### unexpectedly Error on Installing Service ###"
exit 1
fi
systemctl daemon-reload
echo "### Service Installed ### "

