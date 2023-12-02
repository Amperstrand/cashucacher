# cashucacher - Hide your nuts

#mkdir -p ~/src

#cd ~/src
#git clone https://github.com/Amperstrand/cashucacher
docker-compose build


#brint up nutshell
docker exec -it nutshell-wallet poetry run cashu info
balance=$(docker exec -it nutshell-wallet poetry run cashu balance | grep "Balance:" | awk '{print $2}')
if [ "$balance" -lt 10 ]; then
    docker exec -it nutshell-wallet poetry run cashu invoice 10
    #todo: make sure that "Invoice paid." is returned
fi

for offset in {0..9}; do
    echo $creating cashu note ${offset}
    docker exec -it nutshell-wallet poetry run cashu send 1 | grep '^cashu' > "cashu_data/1_sat_cashu_note_at_offset_${offset}.txt"
done

docker-compose up -d cashucacher

# clean up and reclaim unspent cashu notes
#docker exec -it nutshell-wallet poetry run cashu selfpay
#rm cashu_data/1_sat_cashu_note_at_offset_?.txt