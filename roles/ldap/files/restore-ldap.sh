LDAPBK=ldap-directory-backup.ldif
BACKUPDIR=/root
REMOTEDIR=/mnt/mckillican/bak/hyattregency/
rsync -avHK mckillican:$REMOTEDIR/$LDAPBK.gz $BACKUPDIR/$LDAPBK.gz
gunzip $LDAPBK.gz

slapcat -l /tmp/test.ldif
diff /tmp/test.ldif $BACKUPDIR/$LDAPBK
if [ $? != 0 ] ; then
     slapadd -v -l $BACKUPDIR/$LDAPBK
fi
