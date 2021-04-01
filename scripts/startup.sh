if [ “$MULTITENANT_TUTORIAL” == “MULTITENANT_TUTORIAL” ]; then
    echo $MULTITENANT_TUTORIAL
    python3 ./scripts/parse_yml_env_variables.py -c ./configuration/aries-args-multitenant.yaml;aca-py start --arg-file /tmp/agent_conf.yml
else
    echo "Advanced Args used"
    python3 ./scripts/parse_yml_env_variables.py -c ./configuration/aries-args-advanced.yaml;aca-py start --arg-file /tmp/agent_conf.yml
fi