
public class Program
{
    public static void Main()
    {
        // Set up starting positions for white king, black bishop and black rook
        Chess.WhiteKing king = new Chess.WhiteKing(4, 4);
        Chess.BlackBishop bishop = new Chess.BlackBishop(2, 6);
        Chess.BlackRook rook = new Chess.BlackRook(1, 4);

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