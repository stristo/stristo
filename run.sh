echo "Starting stristo..."
if [ -n "$(uname -m | grep arm)" ]; then
    echo "ARM architecture found..."
    env HOME="/root"
    export HOME
fi
couchdb &
touch GUNICORN.PID
(gunicorn -w 4 -b 0.0.0.0:5050 stristo:app -p GUNICORN.PID -R --log-syslog &)
echo "Gunicorn pid: $(cat GUNICORN.PID)"
sleep 3
echo "Run testscript..."
python stristo_test.py && echo "OK Started..."
while true; do true; done
