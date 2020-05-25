#!/usr/bin/python3

import sys
import tempfile
import re
import subprocess
import argparse

# Linux
TEXT2PCAP_BIN='text2pcap'
WIRESHARK_BIN='wireshark'

# Windows Wireshark Path
#TEXT2PCAP_BIN='D:\\Program Files\\Wireshark\\text2pcap.exe'
#WIRESHARK_BIN='D:\\Program Files\\Wireshark\\Wireshark.exe'

all_decode_type = {
"ip":"IP",
"ranap":"RANAP",
"s1ap":"S1AP",
"x2ap":"X2AP",
"f1ap":"F1AP",
"rlc-lte":"4G RLC",
"mac-lte":"4G MAC",
"rrc.dl.dcch":"3G RRCDL-DCCH-Message",
"rrc.ul.dcch":"3G RRCUL-DCCH-Message",
"rrc.dl.ccch":"3G RRCDL-CCCH-Message",
"rrc.ul.ccch":"3G RRCUL-CCCH-Message",
"rrc.pcch":"3G RRCPCCH-Message",
"rrc.dl.shcch":"3G RRCDL-SHCCH-Message",
"rrc.ul.shcch":"3G RRCUL-SHCCH-Message",
"rrc.bcch.fach":"3G RRCBCCH-FACH-Message",
"rrc.bcch.bch":"3G RRCBCCH-BCH-Message",
"rrc.bcch.bch2":"3G RRCBCCH-BCH2-Message",
"rrc.mcch":"3G RRCMCCH-Message",
"rrc.msch":"3G RRCMSCH-Message",
"rrc.sysinfo":"3G RRCSystemInformation-BCH",
"rrc.sysinfo2":"3G RRCSystemInformation2-BCH",
"rrc.sysinfo.cont":"3G RRCSystem-Information-Container",
"rrc.si.mib":"3G RRCMasterInformationBlock",
"rrc.si.sib1":"3G RRCSysInfoType1",
"rrc.si.sib2":"3G RRCSysInfoType2",
"rrc.si.sib3":"3G RRCSysInfoType3",
"rrc.si.sib4":"3G RRCSysInfoType4",
"rrc.si.sib5":"3G RRCSysInfoType5",
"rrc.si.sib5bis":"3G RRCSysInfoType5bis",
"rrc.si.sib6":"3G RRCSysInfoType6",
"rrc.si.sib7":"3G RRCSysInfoType7",
"rrc.si.sib8":"3G RRCSysInfoType8",
"rrc.si.sib9":"3G RRCSysInfoType9",
"rrc.si.sib10":"3G RRCSysInfoType10",
"rrc.si.sib11":"3G RRCSysInfoType11",
"rrc.si.sib11bis":"3G RRCSysInfoType11bis",
"rrc.si.sib11ter":"3G RRCSysInfoType11ter",
"rrc.si.sib12":"3G RRCSysInfoType12",
"rrc.si.sib13":"3G RRCSysInfoType13",
"rrc.si.sib13-1":"3G RRCSysInfoType13-1",
"rrc.si.sib13-2":"3G RRCSysInfoType13-2",
"rrc.si.sib13-3":"3G RRCSysInfoType13-3",
"rrc.si.sib13-4":"3G RRCSysInfoType13-4",
"rrc.si.sib14":"3G RRCSysInfoType14",
"rrc.si.sib15":"3G RRCSysInfoType15",
"rrc.si.sib15bis":"3G RRCSysInfoType15bis",
"rrc.si.sib15-1":"3G RRCSysInfoType15-1",
"rrc.si.sib15-1bis":"3G RRCSysInfoType15-1bis",
"rrc.si.sib15-1ter":"3G RRCSysInfoType15-1ter",
"rrc.si.sib15-2":"3G RRCSysInfoType15-2",
"rrc.si.sib15-2bis":"3G RRCSysInfoType15-2bis",
"rrc.si.sib15-2ter":"3G RRCSysInfoType15-2ter",
"rrc.si.sib15-3":"3G RRCSysInfoType15-3",
"rrc.si.sib15-3bis":"3G RRCSysInfoType15-3bis",
"rrc.si.sib15-4":"3G RRCSysInfoType15-4",
"rrc.si.sib15-5":"3G RRCSysInfoType15-5",
"rrc.si.sib15-6":"3G RRCSysInfoType15-6",
"rrc.si.sib15-7":"3G RRCSysInfoType15-7",
"rrc.si.sib15-8":"3G RRCSysInfoType15-8",
"rrc.si.sib16":"3G RRCSysInfoType16",
"rrc.si.sib17":"3G RRCSysInfoType17",
"rrc.si.sib18":"3G RRCSysInfoType18",
"rrc.si.sib19":"3G RRCSysInfoType19",
"rrc.si.sib20":"3G RRCSysInfoType20",
"rrc.si.sib21":"3G RRCSysInfoType21",
"rrc.si.sib22":"3G RRCSysInfoType22",
"rrc.si.sib23":"3G RRCSysInfoType23",
"rrc.si.sib24":"3G RRCSysInfoType24",
"rrc.si.sib25":"3G RRCSysInfoType25",
"rrc.si.sb1":"3G RRCSysInfoTypeSB1",
"rrc.si.sb2":"3G RRCSysInfoTypeSB2",
"rrc.si.sb3":"3G RRCSysInfoTypeSB3",
"rrc.irat.ho_to_utran_cmd":"3G RRCHandoverToUTRANCommand",
"rrc.irat.irat_ho_info":"3G RRCInterRATHandoverInfo",
"rrc.ue_radio_access_cap_info":"3G RRCUE-RadioAccessCapabilityInfo",
"rrc.s_to_trnc_cont":"3G RRCToTargetRNC-Container",
"rrc.t_to_srnc_cont":"3G RRCTargetRNC-ToSourceRNC-Container",
"lte-rrc.ue_radio_access_cap_info":"4G UERadioAccessCapabilityInformation",
"lte-rrc.ue_radio_access_cap_info.nb":"4G UERadioAccessCapabilityInformation-NB",
"lte-rrc.ue_radio_paging_info":"4G UERadioPagingInformation",
"lte-rrc.ue_radio_paging_info.nb":"4G UERadioPagingInformation-NB",
"lte-rrc.bcch.bch":"4G BCCH-BCH-Message",
"lte-rrc.bcch.dl.sch":"4G BCCH-DL-SCH-Message",
"lte-rrc.bcch.dl.sch.br":"4G BCCH-DL-SCH-Message-BR",
"lte-rrc.mcch":"4G MCCH-Message",
"lte-rrc.pcch":"4G PCCH-Message",
"lte-rrc.dl.ccch":"4G DL-CCCH-Message",
"lte-rrc.dl.dcch":"4G DL-DCCH-Message",
"lte-rrc.ul.ccch":"4G UL-CCCH-Message",
"lte-rrc.ul.dcch":"4G UL-DCCH-Message",
"lte-rrc.sc.mcch":"4G SC-MCCH-Message-r13",
"lte-rrc.ue_cap_info":"4G UECapabilityInformation",
"lte-rrc.ue_eutra_cap":"4G UE-EUTRA-Capability",
"lte-rrc.sbcch.sl.bch":"4G SBCCH-SL-BCH-Message",
"lte-rrc.sbcch.sl.bch.v2x":" 4GSBCCH-SL-BCH-Message-V2X-r14",
"lte-rrc.bcch.bch.nb":"4G BCCH-BCH-Message-NB",
"lte-rrc.bcch.dl.sch.nb":"4G BCCH-DL-SCH-Message-NB",
"lte-rrc.pcch.nb":"4G PCCH-Message-NB",
"lte-rrc.dl.ccch.nb":"4G DL-CCCH-Message-NB",
"lte-rrc.dl.dcch.nb":"4G DL-DCCH-Message-NB",
"lte-rrc.ul.ccch.nb":"4G UL-CCCH-Message-NB",
"lte-rrc.ul.dcch.nb":"4G UL-DCCH-Message-NB",
"lte-rrc.sc.mcch.nb":"4G SC-MCCH-Message-NB",
"lte-rrc.bcch.bch.mbms":"4G BCCH-BCH-Message-MBMS",
"lte-rrc.bcch.dl.sch.mbms":"4G BCCH-DL-SCH-Message-MBMS",
"nas-eps":"NAS",
"nr-rrc.ue_radio_paging_info":"NR RRC UERadioPagingInformation",
"nr-rrc.ue_radio_access_cap_info":"NR UERadioAccessCapabilityInformation",
"nr-rrc.bcch.bch":"NR BCCH-BCH-Message",
"nr-rrc.bcch.dl.sch":"NR BCCH-DL-SCH-Message",
"nr-rrc.dl.ccch":"NR DL-CCCH-Message",
"nr-rrc.dl.dcch":"NR DL-DCCH-Message",
"nr-rrc.pcch":"NR PCCH-Message",
"nr-rrc.ul.ccch":"NR UL-CCCH-Message",
"nr-rrc.ul.ccch1":"NR UL-CCCH1-Message",
"nr-rrc.ul.dcch":"NR RRC UL-DCCH-Message",
"nr-rrc.rrc_reconf":"NR RRC RRCReconfiguration",
"nr-rrc.ue_mrdc_cap":"NR RRC UE-MRDC-Capability",
"nr-rrc.ue_nr_cap":"NR RRC UE-NR-Capability",
}

def print_decode_type():
    print("Supported Decoder:")
    for key in all_decode_type.keys():
        print(key + " - " + all_decode_type[key])

class MyAction(argparse._StoreTrueAction):
    def __call__(self, parser, values, namespace, option_string=None):
        print_decode_type()
        parser.exit()

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='3GPP Decoder')
    parser.add_argument('-l', '--list', action=MyAction, help='list decode types')
    parser.add_argument('decode_type', help='decode type')
    parser.add_argument('hex_string', help='the hex string to be decoded')

    args = parser.parse_args()

    if args.list:
        print_decode_type()
        sys.exit()

    decode_type = args.decode_type
    hex_string = args.hex_string

    if decode_type not in all_decode_type.keys():
        print("Decode type not supported")
        sys.exit()

    if hex_string == '':
        print("No hex string input")
        sys.exit()

    re_result, number = re.subn("([a-fA-F0-9][a-fA-F0-9])", " \\1", hex_string)

    re_result = re_result + " "

    print('re_result:', re_result)

    temp1 = tempfile.NamedTemporaryFile(mode="w+t", delete=False)
    temp2 = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
    try:
        print('temp1.name:', temp1.name)
        print('temp2.name:', temp2.name)
        temp1.write("000000")
        temp1.write(re_result)
        temp1.flush()
        
        subprocess.run([TEXT2PCAP_BIN, "-l 147", temp1.name, temp2.name])

        subprocess.run([WIRESHARK_BIN, '-o', 'uat:user_dlts:\"User 0 (DLT=147)\",\"' + decode_type + '\",\"0\",\"\",\"0\",\"\"', temp2.name])
        
    finally:
        temp1.close()
        temp2.close()



