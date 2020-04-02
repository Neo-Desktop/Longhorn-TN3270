#include <stdio.h>
#include <string.h>
#include <ctype.h>
#pragma GCC diagnostic ignored "-Wwrite-strings"

int LicenseCalc(char *sInput);
int strtoupper(char *sInput);
char input [40];

int main ()
{
	while(true) {
		printf("Please enter a User Name or ^C to cancel:\n  >");
		fgets(input, 40, stdin);
		strtoupper(input);

		if ((strlen(input) > 0) && (input[strlen(input) - 1] == '\n'))
			input[strlen(input) - 1] = '\0';

		int license = LicenseCalc(input);
		printf("Input: %s\tLicense: %05u\tHex: 0x%x\n", input, license, license);
	}
	return 0;
}

int LicenseCalc(char *sInput)
{
	int salt = 0x5217;
	for (int i = 0; i < strlen(sInput); i++) {
		salt += sInput[i] * 0xa3;
	}
	return salt & 0xffff;
}

int strtoupper(char *input)
{
	for (int i = 0; input[i] != 0; i++) {
		input[i] = toupper(input[i]);
	}
}