@echo off
echo Adding firewall rules for more-focus...
netsh advfirewall firewall delete rule name="MoreFocus HTTP" >nul 2>&1
netsh advfirewall firewall delete rule name="MoreFocus 8080" >nul 2>&1
netsh advfirewall firewall add rule name="MoreFocus HTTP"  dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="MoreFocus 8080" dir=in action=allow protocol=TCP localport=8080
echo Done.
netsh advfirewall firewall show rule name="MoreFocus HTTP"
pause
