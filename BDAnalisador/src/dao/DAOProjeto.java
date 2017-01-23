package dao;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Classe;
import entities.Metodo;
import entities.Projeto;

public class DAOProjeto {

	public static void main (String[] args) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		Projeto projeto = new Projeto();
		projeto.setNome("Teste3");
		
		Classe classe = new Classe();
		classe.setNome("classeTeste");
		classe.setProjeto(projeto);
		
		Metodo metodo = new Metodo();
		metodo.setNome("metodoTeste");
		metodo.setQtdForEach(5);
		metodo.setClasse(classe);
		
		manager.getTransaction().begin();
		manager.persist(metodo);
		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	}
	
}
