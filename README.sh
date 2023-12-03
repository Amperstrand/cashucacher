#!/bin/bash
# cashucacher - Hide your nuts

#mkdir -p ~/src

#cd ~/src
#git clone https://github.com/Amperstrand/cashucacher
docker-compose build

# Bring up nutshell if needed to get fresh cashu notes
get_new_cashu_notes=false

if [ "$get_new_cashu_notes" = true ]; then
    # Start cashucacher
    docker-compose up -d cashucacher

    # Get wallet balance
    balance=$(docker exec -it nutshell-wallet poetry run cashu balance | grep "Balance:" | awk '{print $2}')

    if [ "$balance" -lt 10 ]; then
        # Create an invoice if balance is less than 10
        output=$(docker exec -it nutshell-wallet poetry run cashu invoice 11)

        # TODO: Check if "Invoice paid." is returned in $output
        echo $output | grep "Invoice paid." | awk '{print $2}'
    fi

    for offset in {0..9}; do
        echo "Creating cashu note ${offset}"
        # Send cashu note and save the output to a file
        docker exec -it nutshell-wallet poetry run cashu send 1 | grep '^cashu' > "cashu_data/1_sat_cashu_note_at_offset_${offset}.txt"
    done
fi

# Start cashucacher
docker-compose up -d cashucacher

# clean up and reclaim unspent cashu notes
#docker exec -it nutshell-wallet poetry run cashu selfpay
#rm cashu_data/1_sat_cashu_note_at_offset_?.txt
