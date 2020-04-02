###############################################################################
# Generate keys based on black box discovery
###############################################################################

import frida
import sys

def on_message(message, data):
    print("[on_message] message:", message, "data:", data)

# vistatn3270!LicenceCalc@00432CF0
# vistatn3270!SanitizeString@00430830

session = frida.attach("vistatn3270.exe")

script = session.create_script("""

var santitizeString = new NativeFunction(ptr(0x00430830), 'int', ['pointer']);
var strToUpper = new NativeFunction(ptr(0x0044F046), 'void', ['pointer']);
var iLicenseCalc = new NativeFunction(ptr(0x00432CF0), 'uint', ['pointer', 'pointer', 'uint', 'char']);

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

var jst = "  Longhorn 3270";
var jsts = Memory.allocAnsiString(jst);
var buf = Memory.alloc(8);

strToUpper(jsts);
iLicenseCalc(buf, jsts, jst.length, 0x1);

""")

script.on('message', on_message)
script.load()
print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
sys.stdin.read()
session.detach()
