package dao;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Projeto;

public class DAOProjeto {

	public Integer gravarProjeto (Projeto projeto) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		manager.getTransaction().begin();
		
//		if (projeto.getId()!= null) {
//			projeto = manager.merge(projeto);
//		}
		manager.persist(projeto);
		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	    return projeto.getId();
	}
	
}
