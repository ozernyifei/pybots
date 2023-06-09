using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    public class BlackBishop
    {
        public int X { get; set; }
        public int Y { get; set; }

        public BlackBishop(int x, int y)
        {
            X = x;
            Y = y;
        }

        public bool CanMoveTo(int x, int y)
        {
            // Bishops can move diagonally any number of squares
            return (System.Math.Abs(X - x) == System.Math.Abs(Y - y));
        }
    }
}
