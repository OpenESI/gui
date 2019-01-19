echo ''
echo ''
echo '****************************************'
echo '               Uptime'
echo '----------------------------------------'
echo ''
uptime
echo ''
sleep 2
echo ''
echo '****************************************'
echo '                RAM: '
echo '----------------------------------------'
echo ''
free
echo ''
sleep 2
echo ''
echo '****************************************'
echo '                HDD: '
echo '----------------------------------------'
echo ''
df
echo ''
sleep 2
echo ''
echo '****************************************'
echo '              NETWORK: '
echo '----------------------------------------'
echo ''
netstat | grep tcp
netstat | grep unix
echo ''
ifconfig
echo ''
echo ''

exit 0
