#!/bin/sh
#
# darkice      This shell script takes care of starting and stopping
#              the darkice multimedia streaming systen.
#
# chkconfig: - 85 15
# description: darkice provides alsa sources to icecast.  \
# processname: darkice
# config: /etc/darkice.cfg

# Source function library.
. /etc/rc.d/init.d/functions

[ -x /usr/local/bin/darkice ] || exit 0

# See how we were called.
case "$1" in
  start)
	# Start daemon.
	echo -n $"Starting darkice streaming daemon: "
	daemon "/usr/local/bin/darkice -v5 -c /etc/darkice.cfg 2>&1 >> /var/log/darkice.log &"
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && touch /var/lock/subsys/darkice
	;;
  stop)
	# Stop daemon.
	echo -n $"Shutting down darkice streaming daemon: "
	killproc darkice
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/darkice
	;;
  status)
	status darkice
	RETVAL=$?
	;;
  restart)
	$0 stop
	$0 start
	;;
  condrestart)
        [ -f /var/lock/subsys/darkice ] && restart || :
        ;;
  *)
	echo $"Usage: $0 {start|stop|status|restart}"
	RETVAL=1
	;;
esac

exit $RETVAL

