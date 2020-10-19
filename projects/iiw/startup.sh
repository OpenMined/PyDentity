aca-py start \
     --inbound-transport http '0.0.0.0' $HTTP_PORT \
     --outbound-transport http \
     -e "$ENDPOINT" "${ENDPOINT/http/ws}" \
     --webhook-url $WEBHOOK_URL \
     --wallet-type 'indy' \
     --auto-accept-requests  \
     --auto-respond-credential-proposal \
     --auto-respond-credential-offer \
     --auto-respond-credential-request \
     --auto-store-credential \
     --auto-respond-presentation-proposal \
     --auto-respond-presentation-request \
     --admin '0.0.0.0' $ADMIN_PORT \
     --genesis-url https://raw.githubusercontent.com/sovrin-foundation/sovrin/master/sovrin/pool_transactions_sandbox_genesis \
     --admin-api-key $API_KEY \
     --plugin attach_protocol.attachment_protocol \
     --log-level info \
     --label $AGENT_NAME \
     "$@"