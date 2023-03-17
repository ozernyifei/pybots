using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    public class WhiteKing
    {
        public int X { get; set; }
        public int Y { get; set; }

        public WhiteKing(int x, int y)
        {
            X = x;
            Y = y;
        }

        public bool IsInCheckByBlackRook(Chess.BlackRook rook)
        {
            // A king is in check by a rook if the rook can move to the king's position
            return rook.CanMoveTo(X, Y);
        }

        public bool IsInCheckByBlackBishop(Chess.BlackBishop bishop)
        {
            // A king is in check by a bishop if the bishop can move to the king's position
            return bishop.CanMoveTo(X, Y);
        }
    }
}
