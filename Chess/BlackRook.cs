using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    public class BlackRook
    {
        public int X { get; set; }
        public int Y { get; set; }

        public BlackRook(int x, int y)
        {
            X = x;
            Y = y;
        }

        public bool CanMoveTo(int x, int y)
        {
            // Rooks can move horizontally or vertically any number of squares
            return (X == x || Y == y);
        }
    }
}
