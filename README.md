# 3gpp_decoder_wireshark

3gpp_decoder_wireshark is a free open source python wrapper to decode 3GPP PDUs(Protocol Data Units) via Wireshark.

You can use 3gpp_decoder_wireshark decode 3GPP LTE, UMTS and GSM messages for RRC, NAS, S1AP, RANAP, X2AP and RLC.

# Installation

Install from the git repository:

git clone https://github.com/marcohuangch/3gpp_decoder_wireshark.git

# Usage

python 3gpp_decoder.py [-h] [-l] decode_type hex_string

positional arguments:
  decode_type  decode type
  hex_string   the hex string to be decoded

optional arguments:
  -h, --help   show this help message and exit
  -l, --list   list decode types

# Example

python 3gpp_decoder.py lte-rrc.dl.dcch 060800C1000426B7B134B634BA3C80
