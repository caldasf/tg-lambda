package controlador;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import dao.DAOClasse;
import dao.DAOMetodo;
import dao.DAOProjeto;
import dao.DAOVersao;
import entities.Classe;
import entities.Metodo;
import entities.Projeto;
import entities.Versao;

public class Controlador {
	private Projeto projeto;
	private Versao versao;
	private List<Metodo> listaMetodos;
	private DAOProjeto daoProjeto;
	private DAOVersao daoVersao;
	private DAOClasse daoClasse;
	private DAOMetodo daoMetodo;
	
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
		daoClasse = new DAOClasse();
		daoMetodo = new DAOMetodo();
		listaMetodos = new ArrayList<Metodo>();
		
		String inputCsv = "/home/les-02/TGLambda/static-analysis/input.csv";
		FileReader fr = new FileReader(inputCsv);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(inputCsv));
		} catch (IOException e) {
			e.printStackTrace();
		}
		String sCurrentLine;
		projeto.setNome("");
		while ((sCurrentLine = br.readLine()) != null) {
			String nomePasta = "";
			
			String array[] = sCurrentLine.split(";");
			nomePasta += array[2] + "-" + array[3];			
			if (!projeto.getNome().equals(array[2])) {
				projeto.setNome(array[2]);
				popularProjeto();
			}
			versao.setNumVersao(array[3]);
			popularVersao();
			popularMetodos(nomePasta);
			preencherMetodos(nomePasta);
		}		
	}

	private void preencherMetodos(String nomePasta) throws IOException {
		pesquisarLambdas(nomePasta);
		// TODO O RESTO
		daoMetodo.gravarMetodos(listaMetodos);
	}

	private void pesquisarLambdas(String nomePasta) throws IOException {
		String arquivoLambdas = "/home/les-02/TGLambda/static-analysis/output/" + nomePasta + "/lambdaExpression.csv";
		FileReader fr = new FileReader(arquivoLambdas);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(arquivoLambdas));
		} catch (IOException e) {
			e.printStackTrace();
		}
		String sCurrentLine;
		while ((sCurrentLine = br.readLine()) != null) {
			if (!sCurrentLine.startsWith("typeProject")) {
				String array[] = sCurrentLine.split(";");
				String nomeClasse = array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0];
				Integer linhaInicio = new Integer(array[5]);
				Integer linhaFim = new Integer(array[6]);
				
				for (Metodo met : listaMetodos) {
					if (nomeClasse.equals(met.getNomeClasse()) && (linhaInicio >= met.getLinhaInicio() && linhaFim <= met.getLinhaFim())) {
						met.setQtdLambda(met.getQtdLambda() + 1);
					}
				}
			}
		}
	}

	private void popularMetodos(String nomePasta) throws IOException {
		String arquivoMetodos = "/home/les-02/TGLambda/static-analysis/output/" + nomePasta + "/methodDeclaration.csv";
		FileReader fr = new FileReader(arquivoMetodos);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(arquivoMetodos));
		} catch (IOException e) {
			e.printStackTrace();
		}
		String sCurrentLine;
		String nomeClasse = "";
		Integer idClasse = 0;
		while ((sCurrentLine = br.readLine()) != null) {
			if (!sCurrentLine.startsWith("typeProject")) {
				String array[] = sCurrentLine.split(";");
				
				Metodo metodo = new Metodo();
				
				if (!nomeClasse.equals(array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0])) {
					Classe classe = new Classe();
					classe.setNome(nomeClasse);
					classe.setVersao(versao.getId());
//					idClasse = daoClasse.gravarClasse(classe);		
				}
				nomeClasse = array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0];
				
				metodo.setIdClasse(5);
//				metodo.setIdClasse(idClasse);
				metodo.setNomeClasse(nomeClasse);
				
				metodo.setLinhaInicio(new Integer(array[5]));
				metodo.setLinhaFim(new Integer(array[6]));
				metodo.setNome(array[7]);
				metodo.setQtdAic(0);
				metodo.setQtdFilter(0);
				metodo.setQtdForEach(0);
				metodo.setQtdLambda(0);
				metodo.setQtdMaps(0);
				listaMetodos.add(metodo);
			}
		}
	}

	private void popularProjeto() {
		Integer id = daoProjeto.gravarProjeto(projeto);
		versao.setProjeto(id);
	}

	private void popularVersao() {
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

	public DAOClasse getDaoClasse() {
		return daoClasse;
	}

	public void setDaoClasse(DAOClasse daoClasse) {
		this.daoClasse = daoClasse;
	}

	public DAOMetodo getDaoMetodo() {
		return daoMetodo;
	}

	public void setDaoMetodo(DAOMetodo daoMetodo) {
		this.daoMetodo = daoMetodo;
	}
}