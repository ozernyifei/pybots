
public class WhiteKing
{
    public int X { get; set; }
    public int Y { get; set; }

    public WhiteKing(int x, int y)
    {
        X = x;
        Y = y;
    }

    public bool IsInCheckByBlackRook(BlackRook rook)
    {
        // A king is in check by a rook if the rook can move to the king's position
        return rook.CanMoveTo(X, Y);
    }

    public bool IsInCheckByBlackBishop(BlackBishop bishop)
    {
        // A king is in check by a bishop if the bishop can move to the king's position
        return bishop.CanMoveTo(X, Y);
    }
}

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

public class Program
{
    public static void Main()
    {
        // Set up starting positions for white king, black bishop and black rook
        WhiteKing king = new WhiteKing(4, 4);
        BlackBishop bishop = new BlackBishop(2, 6);
        BlackRook rook = new BlackRook(1, 4);

        // Check if white king is in check by black bishop or black rook
        bool isInCheckByBishop = king.IsInCheckByBlackBishop(bishop);
        bool isInCheckByRook = king.IsInCheckByBlackRook(rook);

        // Print result
        if (isInCheckByBishop)
            System.Console.WriteLine("шах от слона");
        else if (isInCheckByRook)
            System.Console.WriteLine("шах от ладьи");
        else
            System.Console.WriteLine("нет шаха");
    }
}