###############################################################################
# Hook into Licence related functions for black-box testing
###############################################################################

import frida
import sys

def on_message(message, data):
    print("[on_message] message:", message, "data:", data)

session = frida.attach("vista32.exe")

script = session.create_script("""

var santitizeString = new NativeFunction(ptr(0x00421f90), 'int', ['pointer']);
var sPrepRegCode = new NativeFunction(ptr(0x00421df0), 'void', ['pointer', 'pointer']);
var iLicenseCalc = new NativeFunction(ptr(0x0042a570), 'uint', ['pointer', 'pointer', 'uint', 'char']);

Interceptor.attach(iLicenseCalc, {

    // When function is called, print out its parameters
    onEnter: function (args) {
        this.inptr = args[0];
        this.outptr = args[1];
        this.inint = args[2];
        this.inchar = args[3];
        console.log('');
        console.log('[+] Called iLicenseCalc@' + iLicenseCalc);
        console.log('Input:' + this.inptr.readAnsiString());
        console.log('Output:' + this.outptr.readAnsiString());
        console.log('IntVal:' + this.inint);
        console.log('CharVal:' + this.inchar);
    },

    // When function is finished
    onLeave: function (retval) {
        console.log('Output:' + this.outptr.readAnsiString());
        console.log('[+] Returned from iLicenseCalc: ' + retval);
    }
});

Interceptor.attach(sPrepRegCode, {

    // When function is called, print out its parameters
    onEnter: function (args) {
        this.outptr = args[0]; // Store arg0 in order to see when we leave the function
        this.inptr = args[1]; // Store arg0 in order to see when we leave the function
        console.log('');
        console.log('[+] Called sPrepRegCode@' + sPrepRegCode);
        console.log('Input:' + this.inptr.readAnsiString());
    },

    // When function is finished
    onLeave: function (retval) {
        console.log('Output:' + this.outptr.readAnsiString()); // Print out data array, which will contain some data as output
        console.log('[+] Returned from sPrepRegCode: ' + retval);
    }
});

Interceptor.attach(santitizeString, {

    // When function is called, print out its parameters
    onEnter: function (args) {
        this.outptr = args[0]; // Store arg0 in order to see when we leave the function
        console.log('');
        console.log('[+] Called santitizeString@' + santitizeString);
        console.log('Input:' + this.outptr.readAnsiString());
    },

    // When function is finished
    onLeave: function (retval) {
        console.log('Output:' + this.outptr.readAnsiString()); // Print out data array, which will contain some data as output
        console.log('[+] Returned from santitizeString: ' + retval);
    }
});

""")

script.on('message', on_message)
script.load()
print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
sys.stdin.read()
session.detach()
