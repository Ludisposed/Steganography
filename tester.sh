echo "I was tired of typing everything in all the time. xD"
echo "## prng_stego tester [bash] ##"
echo ""
echo "TEST 1 -- normal from file"
echo "Encrypt test:"
echo "python prng_stego.py -e -m magic test.png file_test.txt"
stdbuf -oL python prng_stego.py -e -m magic test.png file_test.txt |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""
echo "Decrypt test:"
echo "python prng_stego.py -d -m magic new_test.png"
stdbuf -oL python prng_stego.py -d -m magic new_test.png |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""

echo "TEST 2 -- fail file"
echo "Encrypt test:"
echo "python prng_stego.py -e -m magic test.png file_test.txt.incorrect"
stdbuf -oL python prng_stego.py -e -m somelongasspassword12345 test.png file_test.txt.incorrect |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""
echo "Decrypt test:"
echo "python prng_stego.py -d -m magic new_test.png"
stdbuf -oL python prng_stego.py -d -m somelongasspassword12345 new_test.png |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""

echo "TEST 3 -- Long file input"
echo "Encrypt test:"
echo "python prng_stego.py -e -m magic test.png tester.sh"
stdbuf -oL python prng_stego.py -e -m A21ds0383ddvwe test.png tester.sh |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""
echo "Decrypt test:"
echo "python prng_stego.py -d -m magic new_test.png"
stdbuf -oL python prng_stego.py -d -m A21ds0383ddvwe new_test.png |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""
