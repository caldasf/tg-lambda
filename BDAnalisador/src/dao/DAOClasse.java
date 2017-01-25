package dao;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import entities.Classe;

public class DAOClasse {
	public Integer gravarClasse (Classe classe) {
		EntityManagerFactory factory = Persistence.createEntityManagerFactory("BDAnalisador");
		EntityManager manager = factory.createEntityManager();
		
		manager.getTransaction().begin();
		manager.persist(classe);
		manager.getTransaction().commit();
		
		manager.close();
		
	    factory.close();
	    return classe.getId();
	}
}
