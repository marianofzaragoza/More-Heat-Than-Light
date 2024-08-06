#!/usr/bin/env bash
#
# ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no agustina@192.168.178.96
#
set -eux
CMD="ssh -o PubKeyAuthentication=no "
case $1 in

  alice)
    ${CMD}user@10.147.18.197
    ;;

  bob)
    ${CMD}user@10.147.18.60
    ;;

  carol)
     #${CMD}agustina@10.147.18.55
     ${CMD}user@10.147.18.208
     ;;

  *)
    echo -n "unknown"
    ;;
esac

