# cashucacher - Hide your nuts

#mkdir -p ~/src

#cd ~/src

#git clone https://github.com/cashubtc/nutshell
#cd nutshell
#docker-compose build

#cd ~/src
#git clone https://github.com/Amperstrand/cashucacher
#docker-compose build
#docker-compose up


#make sure the cashu wallet works:
#docker exec -it nutshell-wallet poetry run cashu info

#balance=$(docker exec -it nutshell-wallet poetry run cashu balance | grep -oP 'Balance: \K\d+')

#add some sats
#if [ "$balance" -lt 10 ]; then
#    docker exec -it nutshell-wallet poetry run cashu invoice 10
#fi

#todo: there is no cashu note needed for offset 0 because this is the first offset the merchant will see
#echo "not needed" > cashu_data/1_sat_cashu_note_at_offset_0.txt
#
#for offset in {0..9}; do
#    docker exec -it nutshell-wallet poetry run cashu send 1 | grep '^cashu' > "cashu_data/1_sat_cashu_note_at_offset_${offset}.txt"
#done

# clean up and reclaim unspent cashu notes
#docker exec -it nutshell-wallet poetry run cashu selfpay
#rm cashu_data/1_sat_cashu_note_at_offset_?.txt
