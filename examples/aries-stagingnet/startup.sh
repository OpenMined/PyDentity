aca-py start \
    -it http '0.0.0.0' "$PORT" \
    -ot http \
    -e "$ENDPOINT" "${ENDPOINT/http/ws}" \
    --label "$AGENT_NAME" \
    --auto-accept-requests  \
    --auto-respond-credential-proposal --auto-respond-credential-offer --auto-respond-credential-request --auto-store-credential \
    --auto-respond-presentation-proposal --auto-respond-presentation-request \
    --preserve-exchange-records \
    --genesis-url https://raw.githubusercontent.com/sovrin-foundation/sovrin/master/sovrin/pool_transactions_sandbox_genesis \
    --wallet-type indy \
    --admin 0.0.0.0 $ADMIN_PORT \
    --admin-insecure-mode \
    --debug-connections \
    --debug-credentials \
    --debug-presentations \
    --enable-undelivered-queue \
    --webhook-url $WEBHOOK_URL \
    "$@"