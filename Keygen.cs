using System;

namespace Longhorn_TN3270
{
    /**
     * This was a fun project, had me racking my brain for about a week
     * Thanks for the puzzle!
     */
    internal class Keygen
    {
        private readonly Random _rnd = new Random();
        public string Generate(string userName)
        {
            // licence much have a total length of 10
            char[] licence = {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '};
            
            // populate every other char with random bytes
            for (var i = 2; i < licence.Length; i += 2)
            {
                licence[i] = Convert.ToBoolean(_rnd.Next() % 2) ? (char)(_rnd.Next() % 10 + '0') : (char)(_rnd.Next() % 10 + 'D');
            }

            // populate every other character with the licence
            var iCalcLicence = LicenseCalc(Sanitize(userName.ToUpper()));
            var sCalcLicence = string.Format("{0:D5}", iCalcLicence);
            for (int i = 0, j = 1; i < sCalcLicence.Length; i++, j += 2)
            {
                licence[j] = sCalcLicence[i];
            }

            // first character must be 0-9
            var sum = 0;
            for (var i = 1; i < licence.Length; i++)
            {
                sum += licence[i] - 48;
            }

            licence[0] = (char)(sum % 10 + 48);

            return new string(licence);
        }

        /**
         * Not gonna lie, this function seems pretty silly
         * but it looks like the origional author (of the C function)
         * seemed to have an off by 2 error and was getting garbage
         * while generating licenses
         */
        private static string Sanitize(string stringIn)
        {
            char[] t = {' '};
            return stringIn.TrimStart(t);
        }

        /**
         * Man oh MAN did I go through a whole LOT
         * for 4 measley lines of code
         * Y'all better appreciate this
         */
        private static int LicenseCalc(string sUserName)
        {
            var sum = 0x5217;
            for (var i = 0; i < sUserName.Length; i++)
            {
                sum += sUserName[i] * 0xa3;
            }

            return sum & 0xffff;
        }

    }
}
