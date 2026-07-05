using System;
using System.Collections.Generic;

public class Hola
{
    private string nombre;

    public Hola(string nombre)
    {
        this.nombre = nombre;
    }

    public void saludar()
    {
        Console.WriteLine("Hola, " + nombre);
    }
}
