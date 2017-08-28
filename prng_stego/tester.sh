echo "I was tired of typing everything in all the time. xD"
echo "## prng_stego tester [bash] ##"
echo ""

function do_test() {
    echo "Encrypt test:"
    echo $1
    stdbuf -oL $1 |
        while IFS= read -r line
        do
          echo "$line"
        done
    echo ""
    echo "Decrypt test:"
    echo $2
    stdbuf -oL $2 |
    while IFS= read -r line
        do
          echo "$line"
        done
    echo ""
}

echo "TEST 1 -- normal from file"
do_test "python prng_stego.py -e -p pass -m magic -t file_test.txt test.png " "python prng_stego.py -d -p pass -m magic new_test.png"
echo "TEST 2 -- fail file"
do_test "python prng_stego.py -e -p somelongasspassword12345 -m somelongasspassword12345 -t file_test.txt.incorrect test.png"  "python prng_stego.py -d -p somelongasspassword12345 -m somelongasspassword12345 new_test.png"
echo "TEST 3 -- Long file input"
do_test "python prng_stego.py -e -p ewvdd3830sd12A -m A21ds0383ddvwe -t tester.sh test.png"  "python prng_stego.py -d -p ewvdd3830sd12A -m A21ds0383ddvwe new_test.png"
echo "TEST 4 -- no prng"
do_test "python prng_stego.py -e -p ewvdd3830sd12A -t tester.shksdgf test.png" "python prng_stego.py -d -p ewvdd3830sd12A new_test.png"
echo "TEST 5 -- no opts just stego"
do_test "python prng_stego.py -e -t tester.shksdgf test.png" "python prng_stego.py -d new_test.png"
echo "TEST 6 -- RSA"
do_test "python prng_stego.py -e -r new -t tester.shksdgf test.png" "python prng_stego.py -d --rsa private_key.pem new_test.png"
