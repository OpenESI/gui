if [ -e /tmp/master.zip ]; then
	rm -rf /tmp/master.zip 2>/dev/null
fi
if [ -e /tmp/enigma2-plugin-settings-defaultsatesi-master/ ]; then
	rm -R /tmp/enigma2-plugin-settings-defaultsatesi-master/ 2>/dev/null
fi
cd /tmp/
wget --no-check-certificate https://github.com/OpenESi/enigma2-plugin-settings-defaultsatesi/archive/master.zip
unzip master.zip
cp enigma2-plugin-settings-defaultsatesi-master/etc/enigma2/*.tv /etc/enigma2/
cp enigma2-plugin-settings-defaultsatesi-master/etc/enigma2/*.radio /etc/enigma2/
cp enigma2-plugin-settings-defaultsatesi-master/etc/enigma2/lamedb /etc/enigma2/
cp enigma2-plugin-settings-defaultsatesi-master/etc/enigma2/lamedb5 /etc/enigma2/
cp enigma2-plugin-settings-defaultsatesi-master/etc/enigma2/blacklist /etc/enigma2/
cp enigma2-plugin-settings-defaultsatesi-master/etc/enigma2/whitelist /etc/enigma2/
cd /
cd /tmp/
rm master.zip
rm -R enigma2-plugin-settings-defaultsatesi-master/
sync && sleep 1
wget -qO - http://127.0.0.1/web/servicelistreload?mode=0
sync && sleep 1
wget -q -O - http://127.0.0.1/web/getservices
