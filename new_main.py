from __future__ import print_function
from time import sleep

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.scard import *
from websocket import create_connection
import struct
import smartcard.util
import json


import tkinter as tk

# a simple card observer that prints inserted/removed cards
class PrintObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def __init__(self):
        self.current_uid = 0

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
            uid = self.readCardUid()
            self.current_uid = uid
            print(self.current_uid)
            # self.sendToServer(uid, 'inserted')
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))
            e1.delete(0, tk.END)
            # self.sendToServer(self.current_uid, 'removed')
            self.current_uid = 0

    def readCardUid(self):
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)

        if hresult == SCARD_S_SUCCESS:

            hresult, readers = SCardListReaders(hcontext, [])

            # print(readers)

            if len(readers) > 0:

                reader = readers[1]

                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext,
                    reader,
                    SCARD_SHARE_SHARED,
                    SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)

                if hresult == 0:
                    hresult, response = SCardTransmit(hcard, dwActiveProtocol, [0xFF, 0xCA, 0x00, 0x00, 0x00])

                    #print(smartcard.util.toHexString(response))
                    data = smartcard.util.toHexString(response)
                    data = data[:11].replace(" ", "")
                    #print(data)
                    e1.insert(tk.END, str(int(data, 16)))
                    #print(int(data, 16))
                    tuple = struct.unpack('<i', data.decode('hex'))
                    #print(tuple[0])
                    return tuple[0]
                else:
                    #e1.delete(0, tk.END)
                    print("NO_CARD NEW")
            else:
                print("NO_READER")
        else:
            print("FAILED")

    def sendToServer(self, uid, state):
        # ws = create_connection("ws://localhost:8080")
        # data = {}
        # data["message"] = {}
        # data["message"]["uid"] = uid
        # data["message"]["state"] = state
        # data["action"] = "setcardstate"
        # requestData = json.dumps(data)
        # print(requestData)
        # ws.send(requestData)
        # result =  ws.recv()
        # print("Received '%s'" % result)
        # ws.close()
        return uid


if __name__ == '__main__':
    print("Insert or remove a smartcard in the system.")
    # print("This program will exit in 10 seconds")
    #print("")
    root = tk.Tk()
    root.title('Card Reader')

    e1 = tk.Entry(root, width=60)
    e1.pack(expand=True)
    root.geometry("500x500")

    cardmonitor = CardMonitor()
    cardobserver = PrintObserver()
    cardmonitor.addObserver(cardobserver)

    root.mainloop()

    #input('press Enter to continue')

    # don't forget to remove observer, or the
    # monitor will poll forever...
    cardmonitor.deleteObserver(cardobserver)

    import sys

    #if 'win32' == sys.platform:
        #print('press Enter to continue')
        #sys.stdin.read(1)