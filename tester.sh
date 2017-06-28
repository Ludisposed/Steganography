echo "I was tired of typing everything in all the time. xD"
echo "## prng_stego tester [bash] ##"
echo ""
echo "Encrypt test:"
echo "python prng_stego.py -e -m magic test.png file_test.txt"
stdbuf -oL python prng_stego.py -e -m magic test.png file_test.txt |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""
echo "Decrypt test:"
echo "python prng_stego.py -d -m magic new_test.pn"
stdbuf -oL python prng_stego.py -d -m magic new_test.png |
    while IFS= read -r line
    do
      echo "$line"
    done
echo ""
