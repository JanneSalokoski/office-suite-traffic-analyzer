#!/usr/bin/env bash
set -e

# rm -rf "$HOME/.config/google-chrome"

# Docs

PCAP_OUT=/captures/traffic-docs-$(date +%Y%m%d_%H%M%S).pcap

tshark -i any -w "$PCAP_OUT" &
TSHARK_PID=$!

sleep 2

python test.py $DOCS_URL $INPUT_FILE -m docs

kill $TSHARK_PID
wait $TSHARK_PID 2>/dev/null || true

# Word

PCAP_OUT=/captures/traffic-word-$(date +%Y%m%d_%H%M%S).pcap

tshark -i any -w "$PCAP_OUT" &
TSHARK_PID=$!

sleep 2
python test.py $WORD_URL $INPUT_FILE -m word

kill $TSHARK_PID
wait $TSHARK_PID 2>/dev/null || true

echo "Saved capture to $PCAP_OUT"
