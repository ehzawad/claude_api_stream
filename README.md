# claude_api_stream


asrserver(){
ssh root@192.168.10.98
}

voicebotMTB() {
    ssh -t root@192.168.10.98 "ssh -t appadm@10.45.57.103 'sudo -i'"
}

MTBproj() {
    ssh -t root@192.168.10.98 "ssh -t appadm@10.45.57.103 'sudo -i bash -c \"cd /usr/local/rasa3-main && bash\"'"
}

#!/bin/bash

# SSH and server details
proxy_command="ssh -q -W %h:%p root@192.168.10.98"
remote_user="appadm"
remote_host="10.45.57.103"
remote_directory="/home/appadm"
local_base_directory="/home/ehz/MTBserverSCPed"

# Function to pull files/directories from the remote server
function pullmtb() {
  if [ $# -eq 0 ]; then
    echo "Please provide the absolute path of the file or directory on the remote server."
    return 1
  fi

  remote_path="$1"
  local_path="$local_base_directory/pullmtb/${remote_path##*/}"

  if ssh -o ProxyCommand="$proxy_command" "$remote_user@$remote_host" test -d "$remote_path"; then
    scp -r -o ProxyCommand="$proxy_command" "$remote_user@$remote_host:$remote_path" "$local_path"
  else
    scp -o ProxyCommand="$proxy_command" "$remote_user@$remote_host:$remote_path" "$local_path"
  fi

  echo "Pull operation completed."
}

# Function to push files/directories to the remote server
function pushmtb() {
  if [ $# -eq 0 ]; then
    echo "Please provide the absolute path of the file or directory on your local PC."
    return 1
  fi

  local_path="$1"
  remote_path="$remote_directory/${local_path##*/}"

  if test -d "$local_path"; then
    scp -r -o ProxyCommand="$proxy_command" "$local_path" "$remote_user@$remote_host:$remote_path"
  else
    scp -o ProxyCommand="$proxy_command" "$local_path" "$remote_user@$remote_host:$remote_path"
  fi

  echo "Push operation completed."
}
