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
		BufferedReader br = lerArquivo("/home/luna/Projects/static-analysis/output/methodDeclaration.csv");
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
		
		String inputCsv = "/home/luna/Projects/static-analysis/input.csv";
		FileReader fr = new FileReader(inputCsv);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(inputCsv));
		} catch (IOException e) {
			e.printStackTrace();
		}
		String sCurrentLine;
		projeto.setNome("");
		
		//Executa para cada projeto
		while ((sCurrentLine = br.readLine()) != null) {
			String nomePasta = "";
			
			String array[] = sCurrentLine.split(",");
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
		}		
	}

	//Preencher metodos com todas as suas informacoes: qtd lambda expressions, for each, etc.
	private void preencherMetodos(String nomePasta) throws IOException {
		pesquisarLambdas(nomePasta);
		pesquisarAIC(nomePasta);
		pesquisarMapPattern(nomePasta);
		pesquisarFilterPattern(nomePasta);
		// Falta ForEach
		daoMetodo.gravarMetodos(listaMetodos);
	}

	//Identifica quantidade de expressões lambda
	private void pesquisarLambdas(String nomePasta) throws IOException {
		String arquivoLambdas = "/home/luna/Projects/static-analysis/output/" + nomePasta + "/lambdaExpression.csv";
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
					
					if (nomeClasse.equals(met.getNomeClasse()) && 
						(linhaInicio >= met.getLinhaInicio() && linhaInicio <= met.getLinhaFim())) {
						met.setQtdLambda(met.getQtdLambda() + 1);
					}
				}
			}
		}
	}
	
	
	//Identifica quantidade de AIC
	private void pesquisarAIC(String nomePasta) throws IOException {
		String arquivoAic = "/home/luna/Projects/static-analysis/output/" + nomePasta + "/aic.csv";
		FileReader fr = new FileReader(arquivoAic);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(arquivoAic));
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
					
					if (nomeClasse.equals(met.getNomeClasse()) && 
						(linhaInicio >= met.getLinhaInicio() && linhaInicio <= met.getLinhaFim())) {
						met.setQtdAic(met.getQtdAic() + 1);
					}
				}
			}
		}
	}
	
	//Identifica quantidade de filters
	private void pesquisarFilterPattern(String nomePasta) throws IOException {
		String arquivoFilter = "/home/luna/Projects/static-analysis/output/" + nomePasta + "/filterPattern.csv";
		FileReader fr = new FileReader(arquivoFilter);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(arquivoFilter));
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
					
					if (nomeClasse.equals(met.getNomeClasse()) && 
						(linhaInicio >= met.getLinhaInicio() && linhaInicio <= met.getLinhaFim())) {
						met.setQtdFilter(met.getQtdFilter() + 1);
					}
				}
			}
		}
	}

	// Identificação de Map Patterns
	private void pesquisarMapPattern(String nomePasta) throws IOException {
		String arquivoMap = "/home/luna/Projects/static-analysis/output/" + nomePasta + "/mapPattern.csv";
		FileReader fr = new FileReader(arquivoMap);
		BufferedReader br = new BufferedReader(fr);
		try {
			br = new BufferedReader(new FileReader(arquivoMap));
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
					
					if (nomeClasse.equals(met.getNomeClasse()) && 
						(linhaInicio >= met.getLinhaInicio() && linhaInicio <= met.getLinhaFim())) {
						met.setQtdMaps(met.getQtdMaps() + 1);
					}
				}
			}
		}
	}

	private void popularMetodos(String nomePasta) throws IOException {
		String arquivoMetodos = "/home/luna/Projects/static-analysis/output/" + nomePasta + "/methodDeclaration.csv";
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
					idClasse = daoClasse.gravarClasse(classe);		
				}
				nomeClasse = array[4].substring(array[4].lastIndexOf("/")+1).split("\\.")[0];
				
				metodo.setIdClasse(5);
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