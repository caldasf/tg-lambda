package controlador;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

import dao.DAOProjeto;
import dao.DAOVersao;
import entities.Metodo;
import entities.Projeto;
import entities.Versao;

public class Controlador {
	private Projeto projeto;
	private Versao versao;
	private List<Metodo> listaMetodos;
	private DAOProjeto daoProjeto;
	private DAOVersao daoVersao;
	
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
		versao = new Versao();
		daoProjeto = new DAOProjeto();
		daoVersao = new DAOVersao();
		
		String inputCsv = "/home/les-02/TGLambda/static-analysis/input.csv";
		FileReader fr = new FileReader(inputCsv);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(inputCsv));
		} catch (IOException e) {
			e.printStackTrace();
		}
		String sCurrentLine;
		while ((sCurrentLine = br.readLine()) != null) {
			String nomePasta = "";
			
			//TESTAR NOME ANTERIOR
			if () {
				
			}
			
			String array[] = sCurrentLine.split(";");
			nomePasta += array[2] + "-" + array[3];
			projeto.setNome(array[2]);
			versao.setNumVersao(array[3]);
			populaProjeto(nomePasta);
		}		
	}

	private void populaProjeto(String nomePasta) {
		Integer id = daoProjeto.gravarProjeto(projeto);
		versao.setProjeto(id);
		populaVersao(nomePasta);
	}

	private void populaVersao(String nomePasta) {
		daoVersao.gravarVersao(versao);
	}

	public List<Metodo> getListaMetodos() {
		return listaMetodos;
	}

	public void setListaMetodos(List<Metodo> listaMetodos) {
		this.listaMetodos = listaMetodos;
	}

	public DAOProjeto getDaoProjeto() {
		return daoProjeto;
	}

	public void setDaoProjeto(DAOProjeto daoProjeto) {
		this.daoProjeto = daoProjeto;
	}
	
	public Projeto getProjeto() {
		return projeto;
	}

	public void setProjeto(Projeto projeto) {
		this.projeto = projeto;
	}

	public Versao getVersao() {
		return versao;
	}

	public void setVersao(Versao versao) {
		this.versao = versao;
	}
}