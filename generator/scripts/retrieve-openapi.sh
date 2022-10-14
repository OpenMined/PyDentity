#!/bin/bash
#
# This script will build an ACA-py docker image, and fetch the open api file from it
#
##########################################################################################

# Make sure everything is done in our generator directory
cd "$(dirname "$0")/../" || exit


##########################################################################################
# Global Defaults and Constants
##########################################################################################
ACA_PY_DOCKER_IMAGE_VERSION=${1:-"py36-1.16-1_0.7.5-rc0"}
ACA_PY_DOCKER_IMAGE_DEFAULT="bcgovimages/aries-cloudagent:${ACA_PY_DOCKER_IMAGE_VERSION}"

ACA_PY_ADMIN_PORT="8305"
ACA_PY_INBOUND_PORT="8307"
ACA_PY_DOCKER_PORTS="${ACA_PY_INBOUND_PORT}:${ACA_PY_INBOUND_PORT} ${ACA_PY_ADMIN_PORT}:${ACA_PY_ADMIN_PORT}"
ACA_PY_CMD_OPTIONS=" \
  -e http \
  --inbound-transport http 0.0.0.0 ${ACA_PY_INBOUND_PORT} \
  --outbound-transport http \
  --admin 0.0.0.0 ${ACA_PY_ADMIN_PORT} \
  --admin-insecure-mode \
  --log-level info \
  --auto-provision \
  --wallet-type indy \
  --wallet-name gen-openapi \
  --wallet-key gen-openapi-key \
  --multitenant \
  --multitenant-admin \
  --jwt-secret test \
  --no-ledger"

# Print an indication of script reaching a processing 
# milestone in a noticable way
# $1 : Message string to print
function printMilestone() {
  echo -e "\n\n##########################################################################################"
  echo -e "#"
  echo -e "# " ${1}
  echo -e "#"
  echo -e "##########################################################################################\n"
}


# Wait for a web server to provide a funcitoning interface we can use
# $1 : Url to poll that indicates webserver initialsation complete
# $2 : maximum number of seconds to wait
function waitActiveWebInterface() {
  for (( i=1; i < ${2}; i++))
  do
    curl -s -f ${1}
    if [ $? == 0 ]; then
      return 0
    fi
    echo "Waiting for web interface to activate"
    sleep 1
  done
  echo "**** FAIL - Web interface failed to activate in ${2} seconds. ****"
  return 1
}

# Start an ACA-py docker image
# A simplified version of aries-cloudagent-python/scripts/run_docker
# needed to run without tty or interactive.
# $1: The ACA-py docker image to use (i.e either from a repo or local)
# $2: The port mapping from docker to local host in format "docker1:local1 docker2:local2"
# $3: The ACA-py command line arguements
# $4: The name of a variable to return the continer ID to
function runACAPy() { 
  local acaPyImage="${1}" 
  local ports="${2}"
  local acaPyArgs="${3}"
  local result="${4}"

  args=""
  for port in ${ports}; do
    args="${args} -p ${port}"
  done

  acaPyCmd="docker run -d --rm  ${args} \
              ${acaPyImage} start ${acaPyArgs}" 
  printMilestone "Starting ACA-py docker image with command: \n \
        \t ${acaPyCmd}"

  # Return the docker container id for anyone who cares
  containerId=$(${acaPyCmd})
  local returnStatus=$?
  if [[ ${returnStatus} != 0 ]]; then
      echo "**** FAIL - ACA-Py failed to start, exiting. ****"
      exit 1
  fi
  if [[ "${result}" ]]; then
    eval ${result}="'${containerId}'"
  fi
}

##########################################################################################
# Run docker ACA-py image and pull REST API spec file
##########################################################################################  
runACAPy "${ACA_PY_DOCKER_IMAGE_DEFAULT}" "${ACA_PY_DOCKER_PORTS}" "${ACA_PY_CMD_OPTIONS}" ACA_PY_CONTAINER_ID 
# Make sure ACA-py container gets terminated when we do
trap 'docker kill ${ACA_PY_CONTAINER_ID}' EXIT
waitActiveWebInterface "http://localhost:${ACA_PY_ADMIN_PORT}" 20
returnValue=$?
if [ $returnValue != 0 ]; then
  exit
fi
printMilestone "ACA-Py Admin interface active\n\t Docker Id '${ACA_PY_CONTAINER_ID}'"

curl --output ./data/swagger.json http://localhost:${ACA_PY_ADMIN_PORT}/api/docs/swagger.json

printMilestone "Sucessfully wrote ACA-Py open api file to ./data/swagger.json"
