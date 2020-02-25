import java.util.HashMap;
import java.util.Map;

public class cracking {

    public static void main(String[] args) {

        String cadena1 = "cadenaprueba";
        Map<Character, Integer> cadenita = new HashMap<Character, Integer>();
        Boolean found = false;
        for (int i = 0; i < cadena1.length(); i++) {
            if (!cadenita.containsKey(cadena1.charAt(i))) {
                cadenita.put(cadena1.charAt(i), 1);
            } else {
                found = true;
                break;
            }
        }
        if (found) {
            System.out.println("Has duplicates");

        } else {
            System.out.println("Has no duplicates");
        }

    }
}