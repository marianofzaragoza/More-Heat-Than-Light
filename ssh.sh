#!/usr/bin/env bash
#
# ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no agustina@192.168.178.96
#
set -eux
CMD="ssh -o PubKeyAuthentication=yes "
case $1 in

  alice)
    ${CMD}user@10.147.18.197
    ;;

  alice-vid)
    #${CMD} user@10.148.228.101
    #ssh user@10.147.18.186
    ssh root@10.147.18.205
  ;;
  bob-vid)
    #${CMD} user@10.148.228.101
    #ssh user@10.147.18.186
    ssh root@10.147.18.4
  ;;
  bob)
    # ${CMD} user@10.148.228.106
    ${CMD}user@100.104.227.113 
    ${CMD}user@10.147.18.60
    ;;

  carol)
     #${CMD} user@10.148.228.105
     #${CMD}agustina@10.147.18.55
     ${CMD}user@10.147.18.208
     ;;

  *)
    echo -n "unknown"
    ;;
esac

