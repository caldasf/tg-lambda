import java.io.IOException;

import controlador.Controlador;

public class Main {
	static public void main (String[] args) throws IOException {
		Controlador controlador = new Controlador();
		try {
			controlador.inicializar();			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}