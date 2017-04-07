import java.io.IOException;
import java.text.ParseException;

import controlador.Controlador;

public class Main {
	static public void main (String[] args) throws IOException, ParseException {
		Controlador controlador = new Controlador();
		try {
			controlador.inicializar();			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}