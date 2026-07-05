using System;
using System.Collections.Generic;

public class Contenedor
{
    private List<string> items;

    public void agregar(string item)
    {
        items.Add(item);
    }

    public void listar()
    {
        foreach (string s in items)
        {
            Console.WriteLine(s);
        }
    }
}
