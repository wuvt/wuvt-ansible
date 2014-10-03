LDAPBK=ldap-directory-backup.ldif
BACKUPDIR=/root
REMOTEDIR=/mnt/mckillican/bak/hyattregency/
/usr/sbin/slapcat -v -b "dc=wuvt,dc=vt,dc=edu" -l $BACKUPDIR/$LDAPBK
gzip -9 $BACKUPDIR/$LDAPBK
rsync -avHK $BACKUPDIR/$LDAPBK.gz mckillican:$REMOTEDIR

