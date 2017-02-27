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
	private List<Classe> listaClasses;
	private DAOProjeto daoProjeto;
	private DAOVersao daoVersao;
	private DAOClasse daoClasse;
	private DAOMetodo daoMetodo;
	private String path = "/home/luna/workspace/static-analysis/";
	
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
		listaClasses = new ArrayList<Classe>();

		
		String inputCsv = path + "input.csv";
		BufferedReader br = lerArquivo(inputCsv);
		String sCurrentLine;
		projeto.setNome("");
		
		//Executa para cada projeto
		while ((sCurrentLine = br.readLine()) != null) {
			String nomePasta = "";
			String array[] = sCurrentLine.split(";");
			nomePasta += array[2] + "-" + array[3];	
			//Popular tabela de Projetos
			if (!projeto.getNome().equals(array[2])) {
				projeto.setNome(array[2]);
				popularProjeto();
			}
			
			//Versao
			versao.setNumVersao(array[3]);
			popularVersao();
			
			//Classes e Metodos
			popularMetodos(nomePasta);
			preencherMetodos(nomePasta);
			
			reset();
		}		
	}

	//Preencher metodos com todas as suas informacoes: qtd lambda expressions, for each, etc.
	private void preencherMetodos(String nomePasta) throws IOException {
		pesquisar(nomePasta, "lambdaExpression.csv", 1);
		pesquisar(nomePasta, "aic.csv", 2);
		pesquisar(nomePasta, "filterPattern.csv", 3);
		pesquisar(nomePasta, "mapPattern.csv", 4);
		// Falta ForEach
		daoClasse.gravarClasse(listaClasses);
		daoMetodo.gravarMetodos(listaMetodos);
	}
	
	private void incrementar(Integer operacao, Metodo met) {
		switch (operacao) {
		case 1:
			met.setQtdLambda(met.getQtdLambda() + 1);
			break;
		case 2:
			met.setQtdAic(met.getQtdAic() + 1);
			break;
		case 3:
			met.setQtdFilter(met.getQtdFilter() + 1);
			break;
		case 4:
			met.setQtdMaps(met.getQtdMaps() + 1);
			break;
		}
	}
	
	private void pesquisar(String nomePasta, String nomeArquivo, Integer operacao) throws IOException { 
		String arquivo = path + "output/" + nomePasta + "/" + nomeArquivo;
		BufferedReader br = lerArquivo(arquivo);
		
		String sCurrentLine;
		while ((sCurrentLine = br.readLine()) != null) {
			if (!sCurrentLine.startsWith("typeProject")) {
				String array[] = sCurrentLine.split(";");
				String nomeClasse = array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0];
				
				Integer linhaInicio = new Integer(array[5]);
				Integer linhaFim = new Integer(array[6]);

				for (Metodo met : listaMetodos) {
					if (nomeClasse.equals(met.getNomeClasse()) && 
						(linhaInicio >= met.getLinhaInicio() && linhaFim <= met.getLinhaFim())) {
						incrementar(operacao, met);
					}
				}
			}
		}
	}

	private void popularMetodos(String nomePasta) throws IOException {
		String arquivoMetodos = path + "output/" + nomePasta + "/methodDeclaration.csv";
		BufferedReader br = lerArquivo(arquivoMetodos);
		
		String sCurrentLine;
		String nomeClasse = "";
		Integer idClasse = 0;
		while ((sCurrentLine = br.readLine()) != null) {
			if (!sCurrentLine.startsWith("typeProject")) {
				String array[] = sCurrentLine.split(";");
				
				Metodo metodo = new Metodo();
				
				if (!nomeClasse.equals(array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0])) {
					Classe classe = new Classe();
					classe.setNome(array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0]);
					classe.setVersao(versao.getId());
					idClasse += 1;
					listaClasses.add(classe);
//					idClasse = daoClasse.gravarClasse(classe);
				}
				nomeClasse = array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0];
				
				metodo.setIdClasse(idClasse);
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
	
	private void reset() {
		projeto = new Projeto();
		projeto.setNome("");
		versao = new Versao();
		versao.setNumVersao("");
		listaMetodos.clear();
		listaClasses.clear();
	}
	
	private void popularProjeto() {
		Integer id = daoProjeto.gravarProjeto(projeto);
		versao.setProjeto(id);
	}

	private void popularVersao() {
		daoVersao.gravarVersao(versao);
	}

}