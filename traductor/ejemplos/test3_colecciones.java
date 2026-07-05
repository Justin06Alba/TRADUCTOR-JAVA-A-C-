import java.util.*;

public class Contenedor {
    private List<String> items;

    public void agregar(String item) {
        items.add(item);
    }

    public void listar() {
        for (String s : items) {
            System.out.println(s);
        }
    }
}
