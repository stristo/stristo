echo "Starting stristo..."
couchdb & 
gunicorn -w 4 -b 127.0.0.1:5050 stristo:app &
sleep 3
echo "Run testscript..."
python stristo_test.py && echo "OK Started..."
while true; do true; done
