import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

import entities.Metodo;
import entities.Projeto;
import entities.Versao;

public class Controlador {
	private Projeto projeto;
	private Versao versao;
	private List<Metodo> listaMetodos;
	
	public void popularMetodos() throws IOException {
		BufferedReader br = lerArquivo("/home/les-07/TCC-Lambda/tg-lambda/guava/20.0/methodDeclaration.csv");
		String sCurrentLine;
		String[] listaProjeto = null;
		while ((sCurrentLine = br.readLine()) != null) {
			if (!sCurrentLine.startsWith("typeProject")) {
				listaProjeto = sCurrentLine.split(";");
				projeto.setNome(listaProjeto[2]);
				versao.setNumVersao(listaProjeto[3]);
				System.out.println(sCurrentLine);
			}
		}
	}
	
	public BufferedReader lerArquivo(String nomeArquivo) {
		BufferedReader br = null;
		FileReader fr = null;
		try {
			fr = new FileReader(nomeArquivo);
			br = new BufferedReader(fr);

			br = new BufferedReader(new FileReader(nomeArquivo));
			
			return br;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public void inicializar() throws IOException {
		projeto = new Projeto();
		popularMetodos();
	}

	public List<Metodo> getListaMetodos() {
		return listaMetodos;
	}

	public void setListaMetodos(List<Metodo> listaMetodos) {
		this.listaMetodos = listaMetodos;
	}
}
