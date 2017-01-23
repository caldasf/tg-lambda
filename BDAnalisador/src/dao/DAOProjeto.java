package dao;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Projeto;

public class DAOProjeto {

	public static void main (String[] args) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		Projeto projeto = new Projeto();
		
		projeto.setNome("Teste2");
		
		manager.getTransaction().begin();
		manager.persist(projeto);
		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	}
	
}
